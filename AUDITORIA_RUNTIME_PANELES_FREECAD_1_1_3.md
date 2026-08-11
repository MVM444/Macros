# Auditoria runtime de paneles de FreeCAD 1.1.3

Fecha: 2026-08-10  
Entorno observado: FreeCAD 1.1.x, Python 3.11, Qt/PySide6 6.8.3, Windows 11  
Estado: medicion runtime parcial y auditoria estatica; sin parches funcionales

## 1. Resumen ejecutivo

La medicion confirma que no existe solamente un riesgo teorico. Se observaron
tres ciclos de vida diferentes:

1. `ElectricCRModePanel` reutiliza correctamente un unico dock: 10 llamadas,
   conteo constante de 1.
2. `AreaPorClick` usa `close() + deleteLater() + crear`: en una secuencia
   ejecutada dentro de la misma vuelta del event loop acumulo 1 a 10 docks. Los
   objetos se liberaron al entregar explicitamente eventos `DeferredDelete` y
   al regresar al event loop. Es acumulacion transitoria, relevante durante
   recargas o secuencias automatizadas.
3. `Conexiones Endpoints` usa `close() + crear` sin destruir: acumulo de forma
   persistente 1 a 10 docks ocultos con el mismo `objectName`. `processEvents()`
   no redujo el conteo. Solo la destruccion explicita devolvio la sesion a la
   linea base.
4. GameEngineExportWB cerro correctamente `activeDialog()`, pero dentro de una
   secuencia cerrada en el mismo callback quedaron 7 widgets adicionales por
   ciclo dentro de Tasks. Al regresar al event loop, el conteo volvio de 84 a
   la base de 14. No se demostro acumulacion persistente durante uso humano
   normal; si existe una ventana transitoria durante hot reload.

Conclusion: **existen varios patrones independientes y un problema
arquitectonico comun de ciclo de vida**, pero la evidencia runtime distingue un
culpable persistente (`Conexiones Endpoints`) de patrones transitorios. La
hipotesis acumulativa queda confirmada en parte: varios componentes pueden
coexistir transitoriamente, pero no todos dejan residuos permanentes.

## 2. Instrumentacion creada

Se creo `UI_Audit_FreeCAD.FCMacro`, independiente de los workbenches. La macro:

- usa `FreeCADGui.getMainWindow()`;
- enumera `QDockWidget` y widgets relacionados con Combo/Tasks/Model/Report/
  Python Console;
- registra MainWindow y `centralWidget()`;
- informa `objectName`, titulo, tipo, parent, visibilidad, enabled, floating,
  area, size, min/max, geometry, widget interior, `repr`, direccion Python y,
  cuando Shiboken esta disponible, validez/direccion C++;
- cuenta docks, invisibles y duplicados;
- consulta `FreeCADGui.Control.activeDialog()`;
- no crea, muestra, oculta, cierra, redimensiona ni reparenta widgets;
- solo ejecuta `processEvents()` si se solicita explicitamente.

Prefijos usados: `[UI-AUDIT][DOCK]`, `[UI-AUDIT][COUNT]`,
`[UI-AUDIT][DUPLICATE]`, `[UI-AUDIT][WARNING]`,
`[UI-AUDIT][TASKPANEL]`, `[UI-AUDIT][CENTRAL]`.

## 3. Linea base de la sesion disponible

No era un arranque limpio: FreeCAD ya estaba abierto, ElectricCR activo y un
documento tenia cambios sin guardar. Por seguridad no se cerro FreeCAD ni se
limpio `MainWindowState`. Este snapshot se denomina `RUNTIME_CURRENT`, no A0.

### Conteos

| Snapshot | QDockWidget total | Visibles | Ocultos | Duplicados | Active dialog |
|---|---:|---:|---:|---:|---|
| Antes de `processEvents()` | 6 | 3 | 3 | 0 | false |
| Despues de `processEvents()` | 6 | 3 | 3 | 0 | false |
| Final, despues de limpiar exclusivamente objetos creados por las pruebas | 6 | 3 | 3 | 0 | false |

### Docks iniciales

| objectName | Titulo | Visible | Area | Tamano | Minimo | Observacion |
|---|---|---:|---|---|---|---|
| `Report view` | Report View | si | Bottom | 2560x93 | 74x92 | Geometria fuera de pantalla; probablemente tab no activo del grupo inferior |
| `Selection view` | Vista de Seleccion | no | Left | 100x30 | 0x0 | Dock nativo oculto |
| `Model` | Modelo | si | Left | 416x1109 | 150x185 | Dock nativo |
| `Python console` | Consola de Python | si | Bottom | 2560x93 | 74x92 | Dock nativo |
| `ElectricCRModePanel` | ElectricCR Modos | no | Right | 751x430 | 183x430 | Unica instancia |
| `Tasks` | Tareas | no | Right | 751x1109 | 216x82 | Dock nativo oculto |

MainWindow: 2560x1369.  
Central widget: `QMdiArea`, 2138x1109, geometria x=422, y=99, minimo 0x0.  

En esta linea base la vista central no estaba reducida a una fraccion anomala.
El ancho de 751 px almacenado en Tasks y ElectricCRModePanel merece seguimiento
en el momento exacto del fallo, pero al estar ocultos no reducia el central.

## 4. Prueba runtime: Conexiones Endpoints

Objeto: `ElectricCR_ConexionesEndpointsDock`  
Archivo: `Macros-de-Freecad/Conectar/Panel_Conexiones_Endpoints.FCMacro`

Se ejecutaron 10 ciclos. Despues de cada apertura se proceso eventos, se cerro
el dock y se proceso eventos nuevamente.

| Ciclo | Inmediato al abrir | Tras eventos | Tras `close()` | Tras eventos de cierre |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 3 | 3 | 3 | 3 |
| 4 | 4 | 4 | 4 | 4 |
| 5 | 5 | 5 | 5 | 5 |
| 6 | 6 | 6 | 6 | 6 |
| 7 | 7 | 7 | 7 | 7 |
| 8 | 8 | 8 | 8 | 8 |
| 9 | 9 | 9 | 9 | 9 |
| 10 | 10 | 10 | 10 | 10 |

Resultado final antes de limpieza: 16 docks totales; 10 Endpoints ocultos,
todos hijos de MainWindow, todos registrados en un dock area y con direcciones
Python diferentes. El `objectName` estaba duplicado diez veces.

Evidencia: **acumulacion persistente confirmada**. `close()` oculto, pero no
destruyo. `processEvents()` no cambio el resultado.

Responsabilidad estatica:

```python
old = mw.findChild(QtWidgets.QDockWidget, _PANEL_DOCK_OBJECT)
old.close()
dock = QtWidgets.QDockWidget("Conexiones Endpoints", mw)
dock.setObjectName(_PANEL_DOCK_OBJECT)
```

Ademas, `findChild()` solo devuelve una instancia cuando ya hay duplicados; las
restantes dejan de ser administradas por ese flujo. El slot
`_on_panel_destroyed()` limpia `_PANEL_DOCK` y `_PANEL_WIDGET` sin verificar que
el emisor destruido siga siendo el dock vigente. Si un dock viejo se destruye
tarde, puede borrar las referencias del nuevo.

Limpieza de la prueba: los 10 docks creados por la prueba recibieron
`close()`, `deleteLater()` y entrega de `DeferredDelete`; resultado 10 -> 0 y
total global 16 -> 6. No se tocaron objetos del documento.

## 5. Prueba runtime: AreaPorClick

Objeto: `ElectricCR_AreaPorClickDock`  
Archivo: `Macros-de-Freecad/Areas/AreaPorClick.FCMacro`

En 10 ciclos ejecutados dentro de una sola llamada al hilo GUI, los conteos
fueron identicos a 1, 2, 3, ... 10, incluso despues de `processEvents()` y
`close()`.

El codigo si llama `old.deleteLater()`. La diferencia se comprobo al regresar
al event loop: en la siguiente llamada ya habia desaparecido uno de los diez;
la entrega explicita de eventos `DeferredDelete` elimino los restantes y dejo
el total global nuevamente en 6.

Evidencia: **acumulacion transitoria confirmada**, no acumulacion persistente
en el uso humano normal demostrado. En Qt6/PySide6, `processEvents()` dentro
del callback actual no garantiza procesar los `DeferredDelete` creados en el
mismo nivel de event loop. Una recarga que crea varias instancias sin devolver
control a Qt puede exponer duplicados temporales a MainWindow.

El mismo patron estatico existe en:

- `Conectar_Circuitos_Ramales_Auto.FCMacro`;
- `Conectar_Circuitos_Luminarias_Auto.FCMacro`;
- `Conectar_Cajas_a_Tablero_Auto.FCMacro`;
- `Proponer_Rutas_Guia_Auto.FCMacro`.

No se ejecutaron todos porque comparten el mismo patron y algunos pueden iniciar
logica dependiente de seleccion/documento. Cada uno queda pendiente de prueba
individual en una sesion de ensayo.

## 6. Prueba runtime: ElectricCRModePanel

Se llamo `ensure_panel(show=False)` diez veces.

Resultado: `1, 1, 1, 1, 1, 1, 1, 1, 1, 1`; total global constante en 6.

Evidencia: **reutilizacion correcta confirmada** para el contenedor dock. Sirve
como control positivo y patron A. Esta prueba no midio aun si los widgets
interiores reemplazados por `setWidget()` quedan temporalmente pendientes.

## 7. Prueba runtime: GameEngineExportWB TaskPanel

Comando: `GameEngineExport_Export_Current`  
Secuencia: abrir, medir Tasks, `processEvents()`, `closeDialog()`, medir,
`processEvents()`, repetir diez veces.

`activeDialog()` fue true al abrir y false despues de cada cierre. El numero de
widgets descendientes dentro de Tasks despues del cierre fue:

```text
21, 28, 35, 42, 49, 56, 63, 70, 77, 84
```

Incremento: 7 widgets por ciclo dentro del mismo callback. Tras finalizar la
llamada y regresar al event loop, una nueva medicion dio 14; `processEvents()`
y entrega de `DeferredDelete` mantuvieron 14.

Evidencia: **residuos transitorios confirmados; acumulacion persistente no
observada**. `FreeCADGui.Control.closeDialog()` deja limpieza diferida, normal
en Qt, pero el hot reload inmediato puede operar antes de que esa limpieza
termine. Se requiere una prueba separada de 10 hot reloads, retornando al event
loop entre cada accion, para clasificar definitivamente ese comando.

## 8. Widgets que permanecieron

### Despues de `close()`

- Endpoints: todos; 10 de 10, persistentes.
- AreaPorClick: todos dentro del callback; el anterior empezo a desaparecer al
  volver al event loop.

### Despues de `deleteLater()` y `processEvents()`

- AreaPorClick: siguieron temporalmente dentro del mismo callback.
- Con entrega explicita de `QEvent.DeferredDelete`: desaparecieron.

### Despues de `closeDialog()`

- GameExport: `activeDialog()` quedo false, pero quedaron 7 descendientes
  adicionales de Tasks por ciclo dentro del callback.
- Al regresar al event loop: Tasks volvio a su base de 14 descendientes.

## 9. Clasificacion A/B/C/D/E

Las letras no son excluyentes; E describe ademas una interferencia de layout.

| Archivo / funcion | Tipo | Patron | Riesgo | Evidencia runtime | Duplicacion | Acumulacion |
|---|---|---|---|---|---|---|
| `ElectricCR/ui/mode_panel.py::ensure_panel` | QDockWidget | A | Bajo | 10 llamadas = 1 | no | no |
| `Areas/AreaPorClick.FCMacro` apertura | QDockWidget | C | Medio | 1->10 dentro del callback | si, transitoria | transitoria |
| `Conectar_Circuitos_Ramales_Auto.FCMacro` apertura | QDockWidget | C | Medio | pendiente individual; mismo codigo | potencial | potencial transitoria |
| `Conectar_Circuitos_Luminarias_Auto.FCMacro` apertura | QDockWidget | C | Medio | pendiente individual; mismo codigo | potencial | potencial transitoria |
| `Conectar_Cajas_a_Tablero_Auto.FCMacro` apertura | QDockWidget | C | Medio | pendiente individual; mismo codigo | potencial | potencial transitoria |
| `Proponer_Rutas_Guia_Auto.FCMacro` apertura | QDockWidget | C | Medio | pendiente individual; mismo codigo | potencial | potencial transitoria |
| `Panel_Conexiones_Endpoints.FCMacro` apertura | QDockWidget | D + E | Alto | 1->10 persistente | si | si |
| GameExport `showDialog/closeDialog` | TaskPanel | B diferido | Medio | +7/ciclo, vuelve a base | transitoria | no persistente observada |
| GameExport hot reload | TaskPanel/comandos | Candidato C | Medio | pendiente aislada | desconocida | desconocida |
| `loader_toolbar.py` | QToolBar/QAction | A parcial | Bajo layout / medio senales | no probado runtime | desconocida | desconocida |
| MEPWorkbenchCR dialogs | QDialog | Fuera A-E | Bajo | no probado | sin evidencia | sin evidencia |
| FacilArquitecturaWB dialogs | QDialog | Fuera A-E | Bajo | no probado | sin evidencia | sin evidencia |

## 10. Referencias Python vivas

`Panel_Conexiones_Endpoints.FCMacro` declara:

```python
_PANEL_DOCK = None
_PANEL_WIDGET = None
```

Cada ejecucion de macro puede tener su propio diccionario global, mientras los
docks quedan parentados a la MainWindow C++. Aunque la referencia del namespace
anterior se pierda o sea reemplazada, el parent Qt mantiene vivo el QWidget.
Esto explica la coexistencia observada de diez wrappers/docks C++.

El callback `destroyed` actual no identifica al objeto emisor antes de poner
ambos globals en `None`. Es una carrera de referencias potencial confirmada
por estructura, aunque no se provoco una perdida funcional durante la prueba.

AreaPorClick conserva `parent._ElectricCR_AreaPorClick_panel = panel`. Esa
referencia se sobrescribe al crear el nuevo panel; el dock viejo sigue vivo
hasta `DeferredDelete` porque tambien pertenece a MainWindow.

## 11. Candidatos principales

1. **Conexiones Endpoints**: culpable runtime confirmado de duplicacion y
   acumulacion persistente, ademas de modificar Combo View con
   `tabifyDockWidget()` y MainWindow con `resizeDocks()`.
2. **Familia de docks con `deleteLater()` y recreacion inmediata**: riesgo
   arquitectonico comun confirmado como acumulacion transitoria. Puede ser
   importante durante loaders, recargas o secuencias que no devuelven control
   al event loop.
3. **GameEngineExport hot reload**: candidato secundario. El TaskPanel normal
   se limpia al regresar al event loop; falta comprobar si la recarga inmediata
   ocurre dentro de la ventana de limpieza diferida.

La respuesta solicitada es: **B y C**. Hay al menos un culpable persistente y
otros patrones independientes; tambien existe un problema arquitectonico comun
de manejo heterogeneo de paneles. No hay evidencia para declarar que todos los
workbenches contribuyen por igual.

## 12. Relacion con la pantalla negra

La prueba demostro acumulacion, pero no reprodujo visualmente la zona negra.
Por tanto no se afirma aun causalidad completa. La cadena tecnicamente
plausible y ahora parcialmente medida es:

```text
docks duplicados/ocultos registrados en MainWindow
    + tabificacion automatica con Combo View
    + resizeDocks
    -> apertura de Tasks fuerza recalculo Qt
    -> posible geometria central inconsistente
    -> MainWindowState persiste la consecuencia
```

Para cerrar la causalidad falta capturar un snapshot inmediatamente antes y
despues del fallo visual en una computadora donde se reproduzca.

## 13. Pruebas no ejecutadas y motivo

- A0 de FreeCAD limpio: la instancia disponible ya tenia ElectricCR activo y
  un documento modificado. No se cerro ni reinicio para evitar perdida o
  interferencia.
- Activacion A0 -> B0: no habia linea base limpia valida.
- Tasks nativo con Crear Sketch: no se inicio sobre el documento modificado.
- Secuencia real completa y varias rondas: debe ejecutarse en una sesion de
  ensayo, porque cambia visibilidad/distribucion de docks y requiere acciones
  GUI nativas.
- MEP/Facil dialogs: no hay evidencia estatica de que toquen docks; quedan como
  controles de descarte.

Estas limitaciones impiden llamar a esta auditoria reproduccion completa de la
pantalla negra, pero no invalidan las acumulaciones observadas.

## 14. Politica comun propuesta, no implementada

- `objectName` unico, estable y validado antes/despues de crear.
- Una sola instancia viva por herramienta.
- Preferir reutilizacion; actualizar solo el contenido necesario.
- Si se requiere recrear, esperar `destroyed` o una entrega real de
  `DeferredDelete` antes de crear el reemplazo.
- Un slot `destroyed` debe limpiar globals solo si el objeto destruido es la
  instancia que esos globals representan.
- No tabular automaticamente docks propios con Combo View o Tasks.
- No llamar `resizeDocks()` sobre MainWindow desde workbenches.
- No modificar `centralWidget`, splitters ni estado global.
- TaskPanels: cerrar mediante `Gui.Control`, devolver control al event loop y
  solo despues recargar/recrear.
- Pruebas Qt6 obligatorias: 10 ciclos, conteo por `objectName`, wrappers
  Shiboken validos, Tasks descendants y retorno a linea base.

No se implemento esta politica ni se modifico ningun panel funcional.

## Correcciones implementadas y validacion

Fecha: 2026-08-10.

Se agrego `ElectricCR/ui/dock_manager.py` como utilidad pequena de ciclo de
vida. Busca todas las instancias por `objectName`, conserva una valida, programa
la eliminacion de duplicados historicos y nunca altera Combo View, Tasks,
centralWidget o el layout global.

Cambios aplicados:

- `Panel_Conexiones_Endpoints.FCMacro`: reutiliza dock y panel; se eliminaron
  del flujo `tabifyDockWidget()` contra Combo View y `resizeDocks()`; el
  callback `destroyed` verifica identidad.
- `AreaPorClick.FCMacro`: reutiliza dock y panel completo.
- Ramales, Luminarias, Cajas a Tablero y Proponer Rutas Guia: reutilizan el
  `QDockWidget` y reemplazan solamente el contenido que necesita closures
  nuevos para la ejecucion actual.

Resultados runtime:

| Prueba | Ciclos | Conteo por objectName | Resultado |
|---|---:|---|---|
| Conexiones Endpoints | 20 | siempre 1 | PASS |
| AreaPorClick | 10 | siempre 1 | PASS |
| Circuitos Ramales | 10 | siempre 1 | PASS |
| Circuitos Luminarias | 10 | siempre 1 | PASS |
| Cajas a Tablero | 10 | siempre 1 | PASS |
| Proponer Rutas Guia | 10 | siempre 1 | PASS |

Tasks nativo (`PartDesign_NewSketch`) se abrio/cancelo diez veces sobre un
documento temporal. Los docks permanecieron en 12, centralWidget en
1527x1109 y Tasks en 460x1109 durante la prueba. Los widgets internos
`DeferredDelete` volvieron a su base de 14 al retornar al event loop.

La secuencia combinada se repitio cinco veces. El total permanecio en 12 docks,
cada `objectName` ElectricCR tuvo exactamente una instancia, centralWidget
permanecio en 1547x1109 y Tasks en 440x1109. El cambio ElectricCR -> Part
Design -> ElectricCR no creo duplicados.

GameEngineExportWB se probo en diez ciclos separados de abrir, cerrar y hot
reload. Cada ciclo siguiente inicio con Tasks en su base de 14 widgets y el
total permanecio en 12 docks. No se modifico GameEngineExportWB.

Estado:

- BUG DE ACUMULACION DE DOCKS: corregido en los seis paneles ElectricCR del
  alcance y probado tecnicamente.
- PANTALLA NEGRA: no reproducida; relacion causal completa pendiente de
  validacion durante uso normal.
