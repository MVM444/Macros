# Resultado Codex - Puerta doble BIM Puriscal v001

Fecha: 2026-08-12  
FreeCAD: 1.1.3, compilacion 20260725

## Resultado

Se creo `ElectricCR_PuertaDobleBIM_Puriscal_v001.FCMacro` como macro
independiente. Al ejecutarse crea un documento nuevo y aislado, con la puerta
centrada en el origen inferior, sin muro anfitrion y sin modificar el documento
arquitectonico que estuviera activo.

La puerta se implemento con `Arch.makeWindow(...)` y cumple:

- `IfcType = Door`;
- ancho 2000 mm y alto 2100 mm;
- plano vertical XZ, profundidad en Y y normal explicita `(0, -1, 0)`;
- dos hojas simetricas con separacion central de 10 mm;
- marco exterior, marco de cada hoja, dos travesanos por hoja, panel inferior,
  vidrio intermedio y vidrio superior;
- sistema Europa, aluminio gris satinado y vidrio laminado de 6 mm;
- `Opening`, `SymbolPlan` y `SymbolElevation` disponibles;
- perfil auxiliar oculto y enlazado con una propiedad inversa oculta para no
  crear ciclos en el grafo del documento.

## Arbol y objetos

El grupo `PuertaDobleBIM_Puriscal_v001` contiene:

1. `PerfilBase_PuertaDoble`, objeto `Part::Feature` con 16 wires cerrados;
2. `Window`, objeto `Part::FeaturePython` con proxy `ArchWindow`, rotulado
   `Puerta doble BIM Puriscal - Europa`.

FreeCAD crea adicionalmente el contenedor nativo de materiales, con:

- `Aluminio gris satinado`;
- `Panel inferior gris`;
- `Vidrio laminado 6 mm`;
- multimaterial `Materiales puerta doble Puriscal v001`.

`WindowParts` contiene 13 componentes BIM, organizados en 65 valores: marco
exterior, seis componentes de la hoja izquierda y seis de la hoja derecha.

## Consola

La ejecucion confirmo el prefijo `[ElectricCR][PuertaDobleBIM]` y los mensajes
solicitados: documento creado, objeto BIM creado, `IfcType = Door`, ancho,
alto, 13 componentes y puerta lista para revision.

## Pruebas

El ensayo automatizado comprobo:

- 13 solidos en `Opening = 0`, 25, 50, 100 y nuevamente 0;
- hoja izquierda completa gobernada por `Edge12,Mode1`;
- hoja derecha completa gobernada por `Edge18,Mode2`;
- en 25 %, ambas hojas giran hacia el mismo lado interior y cada panel sigue a
  su hoja; el desplazamiento Y medido fue 182.720933 mm en cada hoja;
- marco exterior fijo durante la apertura;
- guardado, cierre, reapertura y dos recomputaciones sin cambiar la cantidad de
  objetos ni solidos;
- materiales persistentes y tres apariencias distinguibles en la interfaz:
  marco, panel inferior y vidrio transparente.

El archivo de prueba generado es
`.codex_tmp/ElectricCR_PuertaDobleBIM_Puriscal_v001.FCStd`. No se abrio ni se
sobrescribio ningun modelo arquitectonico existente.

## Errores y correcciones

1. La primera prueba produjo una forma nula porque un `Part::Feature` dibujado
   directamente en XZ no suministraba la normal esperada a `ArchWindow`. Se
   corrigio definiendo `Normal = (0, -1, 0)`.
2. El FCStd de ensayo se genero con `FreeCADCmd`, que no instala proveedores de
   vista. La geometria y materiales eran correctos, pero la primera captura se
   veia toda gris. El guion de captura ahora instala el proveedor
   `_ViewProviderWindow` al abrir ese archivo headless y verifica 90 apariencias
   de cara distribuidas en tres materiales. La macro ejecutada dentro de la GUI
   ya recibe este proveedor de forma nativa.
3. Las vistas estandar usan una transicion animada en este perfil de FreeCAD.
   El guion visual espera que finalice antes de ajustar la camara, evitando
   capturas intermedias o recortadas.
4. La conexion MCP no despacho comandos a la GUI durante esta sesion: incluso
   una operacion minima agoto el tiempo de 90 segundos. Por eso las pruebas se
   ejecutaron con `FreeCADCmd` y con una instancia GUI aislada de la misma
   instalacion FreeCAD 1.1.3.
5. FreeCAD muestra un aviso de inicio ajeno a esta macro por una ruta de addon
   inexistente bajo `Mod/FacilArquitecturaWB/FacilArquitecturaWB`. El aviso no
   impidio las pruebas y no se modifico esa configuracion en esta tarea.

## Capturas

- `capturas/PuertaDobleBIM_v001_frontal_cerrada.png`
- `capturas/PuertaDobleBIM_v001_axonometrica_apertura25.png`
- `capturas/PuertaDobleBIM_v001_planta_apertura25.png`

## Recomendacion para v002

Mantener v001 congelada hasta la aprobacion visual de Marco. Solo despues
preparar v002 con controlador parametrico, insercion y abertura en muro,
Placement, hoja activa/semifija, jaladeras simplificadas y propiedades de
integracion ElectricCR/FacilArquitectura.

## Integracion posterior en Facil Arquitectura

Marco aprobo visualmente la v001. El 2026-08-12 la geometria reusable se traslado
conceptualmente, sin borrar esta macro historica, a
`FacilArquitecturaWB/core/double_door_bim.py`. El comando estable
`FA_InsertDoubleDoorBIM` aparece en la barra `FA Aberturas BIM` y crea una puerta
Arch/BIM generica libre o alojada en muro. La referencia Puriscal permanece aqui
como evidencia del origen dimensional; el Workbench ya no depende de esta ruta ni
del nombre del proyecto.

---

# Correccion Facil Arquitectura 0.11.1 - Puerta doble BIM normal

Fecha/hora: 2026-08-12 17:18:46 -06:00  
Equipo: DESKTOP-5586S7P  
FreeCAD: 1.1.3, Python 3.11.14, PySide6/Qt 6.8.3  
Estado: `PROGRAMADO / COMPILADO / PROBADO / VERIFICADO_MCP / VERIFICADO_VISUAL`

## Objetivo aprobado

Se corrigio `FA Insertar puerta doble BIM` para crear una puerta ArchWindow nativa
libre o alojada, con hueco BIM real, `IfcType = Door`, materiales diferenciados,
apertura de las dos hojas y movimiento correcto con el muro. Se conservaron sin
cambios funcionales las cinco barras de Facil Arquitectura.

Version final: `0.11.1` | build `2026.08.12.2`.

## Archivos leidos

- `AGENTS.md` y los contratos completos de `freecad-project-memory` y
  `freecad-cr-workbench-architecture`.
- `FacilArquitecturaWB/TAREA_ACTUAL.md`.
- `FacilArquitecturaWB/core/double_door_bim.py`.
- `FacilArquitecturaWB/commands/cmd_insert_double_door_bim.py`.
- `FacilArquitecturaWB/ui/dialog_double_door_bim.py`.
- `FacilArquitecturaWB/InitGui.py`.
- `FacilArquitecturaWB/DOCUMENTACION_WORKBENCH.md`.
- `FacilArquitecturaWB/tests/freecad_double_door_bim_smoke.py`.
- `FacilArquitecturaWB/tests/freecad_double_door_toolbar_smoke.py`.
- este `RESULTADO_CODEX.md`.
- fuentes nativas de FreeCAD 1.1.3: `ArchWindow.py`, `ArchComponent.py`,
  `ArchMaterial.py`, `ArchWall.py` y la fabrica `Arch.makeMaterial`.

## Archivos modificados por esta correccion

- `FacilArquitecturaWB/core/double_door_bim.py`.
- `FacilArquitecturaWB/commands/cmd_insert_double_door_bim.py`.
- `FacilArquitecturaWB/tests/freecad_double_door_bim_smoke.py`.
- `FacilArquitecturaWB/tests/freecad_double_door_toolbar_smoke.py`.
- `FacilArquitecturaWB/core/constants.py`.
- `FacilArquitecturaWB/Init.py`.
- `FacilArquitecturaWB/InitGui.py`.
- `FacilArquitecturaWB/__init__.py`.
- `FacilArquitecturaWB/package.xml`.
- `FacilArquitecturaWB/README.md`.
- `FacilArquitecturaWB/DOCUMENTACION_WORKBENCH.md`.
- `FacilArquitecturaWB/TAREA_ACTUAL.md`.
- este informe.

No se modificaron loaders globales, ElectricCR, GameEngineExport, MEPWorkbenchCR
ni el FCStd original de La Cruz.

## Causa real de `color[3]`

`ArchWindow._ViewProviderWindow.colorize()` de FreeCAD 1.1.3 espera que el color
resuelto sea RGBA y accede a `color[3]`. `Arch.makeMaterial` escribe
`Transparency` solo cuando el argumento es verdadero. Para aluminio y panel se
pasaba cero; sus tarjetas quedaron con `DiffuseColor` RGB y sin la clave
`Transparency`. Por eso `getSolidMaterial()` devolvia tres valores y se producia
`IndexError`.

La solucion conserva los tres materiales y escribe siempre en cada tarjeta:

- `DiffuseColor` RGB;
- `Transparency = 0` para aluminio;
- `Transparency = 0` para panel inferior;
- `Transparency = 70` para vidrio.

Tambien repara materiales reutilizados que ya existan en el documento. La prueba
GUI llamo directamente a `door.ViewObject.Proxy.colorize(door)` sin excepcion y
confirmo 54 apariencias de aluminio, 12 de panel y 24 de vidrio transparente.

## Causa real del alojamiento y movimiento

El corte BIM simple ya existia: `ArchWindow.getSubVolume()` generaba un volumen de
840 000 000 mm3 y ArchWall lo restaba correctamente. El fallo del comando era el
criterio incompleto: solo aceptaba interseccion con la Shape actual del muro y
disminucion de volumen. Eso rechaza una puerta colocada sobre un hueco que ya fue
reconstruido en la pared, aunque su Subvolume nativo coincida con el tramo nominal.

Ademas se encontro un defecto no cubierto por la prueba anterior: la puerta creaba
tres enlaces inversos al mismo muro (`Hosts`, `Host` y `FA_HostWall`).
`ArchComponent.getMovableChildren()` no elimina duplicados; al mover el muro,
FreeCAD 1.1.3 movia la puerta tres veces.

La solucion aplicada es:

- `Hosts = [wall]` como unica relacion BIM autoritativa;
- `MoveWithHost = True`;
- `HoleWire = 1`, `HoleDepth = 0` y Subvolume automatico de ArchWindow;
- `FA_HostWallName` como clave estable sin enlace inverso adicional;
- proyeccion al segmento finito mas cercano, orientacion y normal registradas;
- validacion de corte nuevo mediante Subvolume antes/despues;
- validacion de hueco preexistente contra un soporte nominal del mismo tramo;
- propiedades `FA_CutStatus`, `FA_CutVolume_mm3` y metricas de interseccion;
- mensajes breves de host, punto, normal, Hosts, MoveWithHost, Hole/Subvolume,
  interseccion y confirmacion del corte.

No se introdujeron cortes booleanos permanentes manuales.

## Pruebas ejecutadas

1. `python -m compileall -q FacilArquitecturaWB`: aprobado.
2. `python -m unittest discover -s FacilArquitecturaWB/tests -p test_*.py`:
   **139 pruebas aprobadas**, 0 fallos.
3. Smoke integral dentro de FreeCAD 1.1.3 por MCP: aprobado.
4. Puerta libre 2000 x 2100 mm: aprobada, 13 solidos, sin host y
   `MoveWithHost = False`.
5. Puerta alojada en muro 5000 x 200 x 3000 mm: aprobada, corte nuevo de
   840 000 000 mm3 y volumen residual cero dentro del Subvolume.
6. Hueco preexistente: aprobado con `FA_CutStatus = preexisting_opening`.
7. Movimiento del muro `(350, -125, 40)` mm: la puerta se desplazo exactamente
   una vez el mismo vector.
8. Eliminacion de la puerta y recomputacion: el muro temporal recupero su volumen.
9. Persistencia: guardar copia temporal, cerrar, reabrir y recomputar dos veces
   sin cambiar objetos ni solidos.
10. `Opening = 0, 25, 50, 100, 0`: aprobado. Las seis piezas de cada hoja se
    mantuvieron unidas, las bisagras quedaron en lados opuestos y el marco exterior
    no cambio.
11. Ruta real del comando con seleccion GUI simulada y dialogo aceptado: aprobada,
    sin errores y con los ocho mensajes de diagnostico requeridos.
12. Dos hot restarts consecutivos: aprobados. Cada una de las cinco barras aparece
    exactamente una vez y la barra heredada aparece cero veces.
13. Captura isometrica MCP: aprobada visualmente; marco gris satinado, panel opaco,
    vidrio azul transparente y hueco del muro distinguibles.

Total automatico de la suite: **139/139 pruebas unitarias aprobadas**, mas los
smokes integrales MCP de puerta, comando, persistencia, vista y hot restart.

## Resultado real en FreeCAD

- `FA_InsertDoubleDoorBIM` registrado y contenido en `FA Aberturas BIM`.
- Modulos cargados desde la copia de `Macros-de-Freecad` solicitada.
- `IfcType = Door`.
- una relacion `Hosts` al muro y `MoveWithHost = True`.
- `Opening` operativo en ambas hojas.
- materiales diferenciados y `ArchWindow.colorize()` sin excepciones.
- cinco barras con conteo exacto uno despues de dos recargas.
- documento temporal visual y todos los documentos temporales cerrados.
- FreeCAD permanece abierto con solo `La_Cruz_Version_2_1`.

## Proteccion del FCStd original

`La Cruz Version 2.1.FCStd` no fue guardado ni modificado. Antes y despues:

- tamano: 4 568 346 bytes;
- mtime: `2026-08-12T15:09:24.6116772-06:00`;
- SHA-256: `383B114507245A809C3F1E36F1DF5E74488698BBC84B314CCE2A076FC3741A72`.

## Pendiente externo

Existe una copia duplicada en
`C:/Users/marco/AppData/Roaming/FreeCAD/v1-1/Mod/FacilArquitecturaWB` cuya ruta
interna falta. Esa configuracion impide inicializar `FreeCADCmd` por separado.
No se modifico porque esta fuera del alcance. No afecta la prueba MCP ni el
Workbench activo, que cargan desde el repositorio correcto.

## Prueba manual final para Marco

1. Mantener abierto FreeCAD y ejecutar `FacilArquitecturaLoader.FCMacro`.
2. Activar Facil Arquitectura y localizar `FA Aberturas BIM`.
3. Seleccionar un solo muro BIM y pulsar aproximadamente el punto deseado.
4. Ejecutar `FA Insertar puerta doble BIM` y aceptar `Alojar y cortar`.
5. Confirmar visualmente el hueco real, vidrio transparente y panel inferior.
6. Cambiar `Opening` a 25, 50, 100 y nuevamente 0.
7. Mover temporalmente el muro mediante Undo/Redo o en una copia y confirmar que
   la puerta lo acompana una sola vez.
8. Si ocurre un error, copiar solo las lineas entre `Host seleccionado` y
   `Corte BIM confirmado` de la Vista de reportes.

No continuar con nuevas funciones de puertas hasta completar esta comprobacion
manual en el modelo de trabajo.
