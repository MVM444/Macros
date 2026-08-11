# Auditoria de layout de FreeCAD 1.1.3

Fecha: 2026-08-10  
Estado: diagnostico estatico; no se modifico codigo funcional

## 1. Resumen

Se audito el codigo activo de ElectricCR, MEPWorkbenchCR, FacilArquitecturaWB,
GameEngineExportWB y `loader_toolbar.py` que interactua con la interfaz de
FreeCAD. La evidencia mas fuerte esta en
`Conectar/Panel_Conexiones_Endpoints.FCMacro`: el panel busca la Combo View,
la tabula explicitamente con su dock y llama `QMainWindow.resizeDocks()`. Al
reabrir, cierra el dock anterior pero crea inmediatamente otro con el mismo
`objectName`, sin `deleteLater()` ni espera al ciclo de eventos.

Esa combinacion viola la regla deseada de que los workbenches no controlen el
layout global y explica exactamente por que la aparicion de Tasks puede forzar
una redistribucion incorrecta: Tasks pertenece al contenedor de Combo View que
el panel propio acaba de modificar. El estado resultante puede quedar
serializado en `MainWindowState`, lo cual concuerda con la recuperacion temporal
al eliminar ese estado.

No se encontro codigo activo en los cuatro workbenches que llame `saveState()`,
`restoreState()`, `saveGeometry()`, `restoreGeometry()`, `setCentralWidget()`,
`splitDockWidget()` o que manipule directamente Report View o Python Console.
Tampoco se encontro un `QSplitter` propio aplicado a la ventana principal.

## 2. Alcance y archivos revisados

Se hicieron busquedas globales en archivos `.py` y `.FCMacro` y revision
dirigida de:

- `Macros-de-Freecad/loader_toolbar.py`.
- `Macros-de-Freecad/ElectricCR/InitGui.py`, `ui/mode_panel.py`,
  `ui/mode_manager.py`, `ui/mode_combo.py` y dialogs de `commands/`.
- Docks ElectricCR activos en `Areas/AreaPorClick.FCMacro` y `Conectar/`, en
  particular `Conectar_Circuitos_Ramales_Auto.FCMacro`,
  `Conectar_Circuitos_Luminarias_Auto.FCMacro`,
  `Conectar_Cajas_a_Tablero_Auto.FCMacro`,
  `Proponer_Rutas_Guia_Auto.FCMacro` y
  `Panel_Conexiones_Endpoints.FCMacro`.
- `Macros-de-Freecad/MEPWorkbenchCR/InitGui.py` y dialogs de `MEP/hvac/`.
- `Macros-de-Freecad/FacilArquitecturaWB/InitGui.py`, comandos y dialogs de
  `ui/`.
- `Macros-de-Freecad/GameEngineExportWB/commands/cmd_open_panel.py`,
  `cmd_open_config.py`, `cmd_reload_workbench.py` y `ui/panel_export.py`,
  `panel_scene.py`, `panel_config.py`, `panel_info.py`.

Los respaldos se buscaron para detectar antecedentes, pero no se consideran
codigo activo ni candidatos sin demostrar que un loader los ejecute.

## 3. Hallazgos

### A. Panel Conexiones Endpoints: modifica Combo View y el layout global

Archivo: `Macros-de-Freecad/Conectar/Panel_Conexiones_Endpoints.FCMacro`  
Lineas: 3178-3188, 3435-3573  
Funcion: `_find_combo_view_dock()` y rutina de apertura del panel  
Riesgo: **ALTO**

Codigo relevante:

```python
combo_dock = _find_combo_view_dock(mw)
mw.tabifyDockWidget(combo_dock, dock)
mw.resizeDocks([dock], [prefs["dock_width"]], QtCore.Qt.Horizontal)
```

Tambien permite todas las areas, restaura area/ancho/flotacion propios y llama
`setFloating()` despues de tabular y redimensionar.

Por que puede afectar Qt 6 / FreeCAD 1.1.3: cambia la topologia del docking de
la `QMainWindow`, no solo el dock propio. Tasks aparece dentro de la zona de
Combo View; cuando FreeCAD cambia de Model a Tasks, Qt recalcula tamanos de un
grupo de tabs que fue creado externamente y al que se le impuso un ancho. Los
cambios encadenados `addDockWidget -> tabifyDockWidget -> resizeDocks ->
setFloating` en el mismo ciclo son compatibles con un estado geometrico
inconsistente o persistido. Es el unico codigo activo encontrado que toca
directamente Combo View y llama a una operacion global de layout.

Prueba minima:

1. Iniciar con `MainWindowState` limpio.
2. Sin abrir Conexiones Endpoints, alternar Model/Tasks 30 veces, abriendo y
   cerrando Report View y Python Console; registrar geometria.
3. Reiniciar limpio, abrir Conexiones Endpoints una vez y repetir.
4. Repetir una tercera vez desactivando temporalmente solo las llamadas
   `tabifyDockWidget()` y `resizeDocks()` mediante una copia de diagnostico.
5. La hipotesis queda confirmada si el fallo aparece en 3 y desaparece en 2 y
   4 bajo la misma secuencia.

Cambio minimo si se confirma: agregar el dock propio solamente en un area
lateral y eliminar las dos llamadas que controlan Combo View/layout global.
No cambiar contenido ni funcionalidad del panel.

### B. Panel Conexiones Endpoints: posible duplicacion durante reapertura

Archivo: `Macros-de-Freecad/Conectar/Panel_Conexiones_Endpoints.FCMacro`  
Lineas: 3149-3166, 3443-3461  
Funcion: apertura y `_on_panel_destroyed()`  
Riesgo: **ALTO**

Codigo relevante:

```python
old = mw.findChild(QtWidgets.QDockWidget, _PANEL_DOCK_OBJECT)
if old is not None:
    old.close()
dock = QtWidgets.QDockWidget("Conexiones Endpoints", mw)
dock.setObjectName(_PANEL_DOCK_OBJECT)
```

`close()` normalmente oculta un `QDockWidget`; no garantiza destruccion. El
nuevo dock se crea inmediatamente con el mismo `objectName`. La referencia
global se reemplaza y el slot `destroyed` del dock antiguo puede ejecutarse mas
tarde y limpiar referencias que ya apuntan al nuevo panel. Esto da evidencia
directa para H6, H7 y H8, y puede dejar varios docks en el estado interno de la
`QMainWindow`.

Prueba minima: abrir el comando 10 veces y, tras cada apertura y un
`QApplication.processEvents()`, contar todos los `QDockWidget` cuyo
`objectName` sea `ElectricCR_ConexionesEndpointsDock`. Registrar tambien
`isVisible`, parent, area y direccion Python/C++ (`repr`). Debe existir
exactamente uno en todo momento.

Cambio minimo si se confirma: reutilizar el dock existente, como hace
`ElectricCRModePanel`, o destruirlo de forma controlada y esperar su senal
`destroyed` antes de crear el reemplazo.

### C. Docks heredados ElectricCR: cerrar, `deleteLater` y recrear sin espera

Archivos y lineas aproximadas:

- `Areas/AreaPorClick.FCMacro`: 2145-2174; minimo 340 px.
- `Conectar/Conectar_Circuitos_Ramales_Auto.FCMacro`: 1219-1235; minimo
  340 px, maximo 440 px.
- `Conectar/Conectar_Circuitos_Luminarias_Auto.FCMacro`: 3044-3075; minimo
  340 px y controles internos con minimo 220 px.
- `Conectar/Conectar_Cajas_a_Tablero_Auto.FCMacro`: 1253-1276; minimo
  440 px, maximo 540 px.
- `Conectar/Proponer_Rutas_Guia_Auto.FCMacro`: 1115-1131; minimo 360 px,
  maximo 460 px.

Funcion: apertura de panel/configuracion de cada macro  
Riesgo: **MEDIO**

Patron relevante:

```python
old.close()
old.deleteLater()
dock = QtWidgets.QDockWidget(...)
dock.setObjectName(...)
main_window.addDockWidget(..., dock)
```

Los nombres son unicos y estables, lo cual es correcto. El riesgo es temporal:
`deleteLater()` es diferido, por lo que durante la misma vuelta del event loop
pueden coexistir dos docks con el mismo nombre. Los minimos de 340-440 px no son
por si solos excesivos, pero varios docks simultaneos en el lado derecho pueden
reducir significativamente la vista central. El maximo de 540 px no explica por
si solo una zona negra que ocupe gran parte de una pantalla normal.

Prueba minima: para cada macro, abrirla 10 veces seguidas; contar duplicados
antes y despues de `processEvents()`, y alternar Tasks. Probar tambien una vez
con el panel anterior simplemente reutilizado. Confirmar cual secuencia produce
el layout anomalo.

Cambio minimo si se confirma: reutilizacion idempotente o creacion diferida
solo despues de destruccion confirmada.

### D. ElectricCRModePanel

Archivo: `Macros-de-Freecad/ElectricCR/ui/mode_panel.py`  
Lineas: 35-75, 100-199  
Funcion: `_find_panel()`, `_make_content()`, `ensure_panel()`  
Riesgo: **BAJO**

Crea un dock estable `ElectricCRModePanel`, busca y reutiliza el existente y
solo reemplaza su widget interior. No fija ancho/alto, no toca Combo View,
Tasks ni splitters. Es un buen control comparativo. Debe verificarse que el
widget interior anterior sea liberado por `QDockWidget.setWidget()` bajo Qt 6,
pero no hay evidencia estatica de corrupcion global.

Prueba minima: abrir/reconstruir el panel 20 veces y confirmar un solo dock y
un solo contenido vivo; alternar Tasks.

### E. `loader_toolbar.py`

Archivo: `Macros-de-Freecad/loader_toolbar.py`  
Lineas: 122-155, 180-202, 252-299  
Funciones: `_load_qt()`, `_bind_fresh_execution()`, `ensure_runtime()`,
`_install_persistence()`  
Riesgo: **BAJO para layout / MEDIO para ciclo de vida de senales**

Solo busca/crea `QToolBar`; no crea docks ni modifica Combo View, Tasks,
centralWidget o estado global. El warning observado proviene probablemente de:

```python
action.triggered.disconnect()
```

La excepcion se captura, pero Qt/PySide puede emitir `RuntimeWarning` antes de
entregarla a Python. No explica directamente el espacio negro. El controlador
persistente se guarda como atributo de MainWindow y se reutiliza, por lo que no
se encontro acumulacion evidente de controladores.

Prueba minima: ejecutar recarga 20 veces y contar toolbars, actions por
`objectName`, controladores y conexiones efectivas. Debe quedar una instancia
de cada uno. El cambio minimo futuro seria desconectar solo el slot conocido,
pero no debe mezclarse con el parche de layout.

### F. GameEngineExportWB TaskPanels y hot reload

Archivos: `commands/cmd_open_panel.py` (76-96),
`commands/cmd_reload_workbench.py` (20-49), `ui/panel_export.py` (143-167,
2217-2225), `ui/panel_scene.py` (90-102, 372-384)  
Riesgo: **MEDIO**

Usa la API oficial `FreeCADGui.Control.showDialog()/closeDialog()` y no busca
ni redimensiona el dock Tasks. El contenido incluye `QTabWidget`, pero no fija
minimumSize, fixedSize ni geometria global. El riesgo esta en recargar modulos
y re-registrar comandos inmediatamente despues de `closeDialog()`: debe
confirmarse que el TaskPanel anterior desaparezca antes de construir otro.

Prueba minima: abrir/cerrar/recargar 20 veces, comprobar `activeDialog()`,
numero de widgets hijos del dock Tasks y geometria del dock antes/despues. Si
no se acumulan formularios, descartar H8 para este workbench.

Cambio minimo si se confirma acumulacion: diferir la recarga/construccion un
ciclo de eventos tras `closeDialog()`; no modificar los paneles.

### G. MEPWorkbenchCR

Archivos: `MEPWorkbenchCR/InitGui.py`; `MEP/hvac/hvac_space.py`,
`hvac_equipment.py`, `hvac_condensing.py`  
Riesgo: **BAJO**

Los hallazgos de 520-560 px son minimos de `QDialog` independientes, no del
dock Tasks ni de la ventana principal. `InitGui.py` usa MainWindow para
sincronizar recursos de `QAction`, no para docking. No se localizaron TaskPanel
propios, QDockWidget, Combo View, Tasks, resizeDocks ni estado global activos.

Prueba minima: ejecutar cada dialog HVAC y alternar Tasks antes/durante/despues.
Si la geometria de los docks no cambia, descartar H1-H5 para MEPWorkbenchCR.

### H. FacilArquitecturaWB

Archivos: comandos y dialogs bajo `FacilArquitecturaWB/commands`, `core` y
`ui`  
Riesgo: **BAJO**

`FreeCADGui.getMainWindow()` se usa como parent de dialogs y mensajes. Algunos
dialogs tienen ancho minimo de 430-480 px, pero no se encontraron docks,
TaskPanels, acceso a Combo View/Tasks, splitters o estado global.

Prueba minima: abrir los dialogs de recintos, cielos y niveles y comparar la
geometria de todos los docks antes/despues. No se propone parche.

## 4. Evaluacion de hipotesis

- H1/H2/H11: parcialmente plausibles en docks heredados, pero los minimos
  hallados son moderados. Riesgo secundario.
- H3/H10/H12: evidencia fuerte en Conexiones Endpoints porque tabula su dock
  con Combo View, contenedor relacionado con Tasks.
- H4: no se encontro manipulacion directa de QSplitter; puede ser efecto
  interno de `tabifyDockWidget/resizeDocks`, no causa directa demostrada.
- H5: no confirmada; requiere captura de areas/visibilidad en ejecucion.
- H6/H7/H8: evidencia fuerte en Conexiones Endpoints y temporal en macros que
  recrean docks con `deleteLater()`.
- H9: descartada por busqueda estatica en codigo activo auditado.
- H13: los modos ElectricCR cambian visibilidad de toolbars, no docks; baja.
- H14: hay capas de compatibilidad PySide6/PySide2/PySide. No se encontro una
  llamada Qt5 exclusiva que explique por si sola el fallo, pero la semantica
  diferida de destruccion bajo Qt6 agrava los patrones de reapertura.

## 5. Candidato mas probable

El candidato principal es `Panel_Conexiones_Endpoints.FCMacro`, por la
combinacion de cuatro hechos observables:

1. modifica directamente Combo View mediante `tabifyDockWidget()`;
2. llama `resizeDocks()` sobre MainWindow;
3. restaura y vuelve a imponer area/ancho/flotacion;
4. puede crear otro dock con el mismo nombre tras solo cerrar el anterior.

Es el unico candidato que conecta directamente nuestros paneles, la aparicion
de Tasks, la geometria central reducida y la persistencia de un
`MainWindowState` defectuoso.

## 6. Instrumentacion minima propuesta

Antes de cualquier correccion, usar una macro de diagnostico temporal que no
altere layout y registre, con prefijo `[UI-AUDIT]`:

- cada `QDockWidget`: `objectName`, titulo, parent, visible, floating, size,
  minimumSize, maximumSize, geometry y `dockWidgetArea`;
- conteo por `objectName` y advertencia `[UI-DOCK]` si es mayor que uno;
- geometria del `centralWidget` y de Combo View/Tasks;
- instantaneas antes/despues de abrir/cerrar cada candidato y antes/despues de
  `showDialog()`.

La primera prueba A/B debe comparar Conexiones Endpoints intacto contra una
copia diagnostica sin `tabifyDockWidget` ni `resizeDocks`. No conviene cambiar
varios workbenches simultaneamente, porque se perderia la atribucion causal.

## 7. Parche minimo condicionado

Si la prueba A/B confirma el candidato:

- archivo: `Conectar/Panel_Conexiones_Endpoints.FCMacro`;
- comportamiento: el panel se agrega como dock invitado sin tabular Combo View
  ni ordenar el redimensionado global;
- ciclo de vida: reutilizar la instancia existente o esperar destruccion antes
  de crear otra;
- riesgo: bajo a medio; puede cambiar solamente la posicion inicial del panel,
  no sus funciones de conexiones.

No se aplico este parche. Esta auditoria se detiene para revision, segun lo
solicitado.
