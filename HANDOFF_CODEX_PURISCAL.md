# Traspaso para Codex: Puriscal y Facil Arquitectura

Actualizado: 2026-07-26, zona horaria America/Costa_Rica.

## Instruccion para una futura tarea de Codex

Leer este archivo completo antes de modificar el modelo de Puriscal o el workbench
`FacilArquitecturaWB`. La sesion anterior trabajo directamente sobre FreeCAD mediante
la conexion MCP. Confirmar primero el documento activo, la version cargada del
workbench y la existencia de cambios del usuario antes de editar archivos.

No volver a crear una reticula arquitectonica con `Arch Axis` o `AxisSystem`. El usuario
pidio especificamente la herramienta BIM **Grid / ArchGrid**, creada con
`Arch.makeGrid()`, y aclaro que sus divisiones deben provenir de los centros de paredes.

## Archivos principales

- Resumen consolidado para lectura rapida:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\RESUMEN_CONSOLIDADO_PURISCAL_FACIL_ARQUITECTURA.md`

- DXF fuente:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal.dxf`
- FCStd de trabajo y resultado:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd`
- Carpeta del workbench:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad\FacilArquitecturaWB`
- Macro de recarga en vivo:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\FacilArquitecturaLoader.FCMacro`
- Macro compatible de rotulos:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\RecopilarRotulosRecintos.FCMacro`
- Macro de areas rectangulares:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\CrearAnalisisAreasRectangulares.FCMacro`
- Macro exclusiva desde muro BIM:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\AnalizarAreasDesdeMuroBIM.FCMacro`
- Documentacion de esa macro:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\ANALISIS_AREAS_DESDE_MURO_BIM.md`
- Macro de puertas BIM orientadas por recintos:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\InsertarPuertasBIMDesdeRecintos.FCMacro`
- Documentacion de puertas:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\PUERTAS_BIM_ORIENTADAS_POR_RECINTOS.md`
- Macro de ventanas BIM:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\InsertarVentanasBIMDesdeRecintos.FCMacro`
- Documentacion de ventanas:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\VENTANAS_BIM_DESDE_RECINTOS.md`

## Estado de FreeCAD al cerrar esta etapa

- Documento activo esperado: `Puriscal_Flujo_Completo_Facil_Arquitectura`.
- Archivo guardado en la ruta FCStd indicada arriba.
- Facil Arquitectura cargado como version `0.4.9`, build `2026.07.26.11`.
- Hay 12 comandos registrados en el workbench.
- La vista guardada es isometrica y muestra `Wall002` semitransparente, 16 puertas BIM
  y 8 ventanas BIM azules; las areas, anotaciones de revision y sketches fuente estan
  ocultos temporalmente para facilitar la revision tridimensional.
- El grupo `FA_MasterSketches` tambien esta oculto temporalmente.
- El ArchGrid BIM se conserva oculto y `FA_GridWallTrace` muestra solo los centros reales
  de paredes, sin prolongaciones fuera de sus tramos.
- Los objetos estructurales `Axis`, `Axis001`, `AxisSystem` y `Structure` pertenecen al
  flujo de columnas `P4`; siguen en el documento pero quedaron ocultos para esta revision.
  No confundirlos con la reticula arquitectonica.

## Objetos fuente importantes del modelo

- Centros de paredes medidos:
  `Sketch_Centros_Pared_Muro_Seco_Espesor_120mm`
  - `FA_CenterlineKind = walls`
  - `FA_ThicknessDetected = True`
  - `FA_WallThickness` aproximado: 120 mm
  - 49 segmentos en la ultima revision
- Centros de puertas: `Sketch_Centros_Puertas`
- Centros de ventanas: `Sketch_Centros_Ventanas`
- Centros/columnas de P4: `Sketch_Centros_P4_Columnas`
- Sketch `Sketch_Centros_P4` no debe usarse para la losa arquitectonica.

## Cuadricula ArchGrid actual

Comando visible del workbench:

`FA Cuadricula ArchGrid para reconstruir paredes`

Objeto creado:

- Nombre interno: `Grid`
- Etiqueta: comienza con `Cuadricula arquitectonica - paredes reconstruidas`; FreeCAD
  puede agregar un sufijo numerico al reemplazarla repetidamente durante una sesion.
- Tipo: `Part::FeaturePython`
- `Proxy.Type = Grid`
- Creado mediante `Arch.makeGrid()`
- `FA_GeneratedBy = FA_CreateBuildingGrid`
- `FA_Role = arch_grid`
- 6 filas, 5 columnas y 30 caras/celdas
- 10 lineas de cuadricula sostenidas por centros de paredes reconstruidos
- Cuatro objetos generados por `FA_CreateBuildingGrid`: `Grid` BIM nativo oculto,
  `FA_GridWallTrace` visible, `FA_ReconstructedWallBase` oculto y el muro reconstruido.
- `FA_GridWallTrace` es un `Sketcher::SketchObject` editable a Z = 0. El usuario lo
  completo manualmente y esa version debe considerarse autoritativa: contiene 67
  geometrias y 147 restricciones. No volver a ejecutar la generacion de cuadricula
  sin preservar primero estas modificaciones manuales.
- El Sketch tiene `FA_CenterlineKind = walls`, `FA_WallThickness = 120 mm`,
  `FA_WallHeight = 3000 mm` y es compatible directamente con
  `FA Muros BIM desde centros`.
- El muro reconstruido actual tiene nombre interno `Wall001`, rol `reconstructed_wall`,
  120 mm de espesor, 3000 mm de altura y 24 solidos. El `Wall` original se conserva
  oculto y no fue eliminado.
- Tras completar manualmente la cuadricula se ejecuto `FA Muros BIM desde centros`.
  Creo `Wall002`, enlazado parametricamente a `FA_GridWallTrace`, con 120 mm de espesor,
  3000 mm de altura, limites Z = 0..3000 mm, geometria valida y un unico solido. El
  muro reconstruido anterior `Wall001` queda oculto para evitar duplicidad visual.
- Captura del resultado:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Puriscal_Muros_BIM_desde_Cuadricula_Manual.png`
- Fuente de pared preferida: `Sketch_Cerrado_Sketch_Centros_Pared_Muro_Seco_Espesor_120mm`
- Fuentes de aberturas enlazadas: `Sketch_Centros_Puertas` y `Sketch_Centros_Ventanas`
- La fuente cerrada tiene `FA_ClosedGapCount = 12` y utiliza los sketches de puertas y ventanas para justificar esos cierres.

Posiciones locales usadas en la ultima ejecucion:

- X: 950.5, 14410.5, 15960.5, 22995.5, 24345.5, 26805.5 mm
- Y: 2818.4, 2906.9, 15496.9, 16852.6, 21042.6, 30749.4, 32863.9 mm

Tamanos ArchGrid:

- Extension total: 25855.0 x 30045.5 mm
- `ColumnSize`: 13460.0, 1550.0, 7035.0, 1350.0, 2460.0 mm
- `RowSize`: 2114.5, 9706.7, 4190.0, 1355.8, 12590.0, 88.5 mm
- La caja envolvente coincide exactamente con la del sketch cerrado: diferencia 0.0 mm
  en los cuatro limites.
- `FA_ExtentBoundaryCount = 4`.

Parametros activos relevantes en `Spreadsheet_Parametros`:

- `grid_cluster_tolerance_mm = 80`
- `grid_primary_support_mm = 5000`
- `grid_max_lines_per_direction = 8`

El criterio actual conserva siempre los dos limites extremos de cada direccion y agrega
alineamientos cuyo soporte acumulado de pared alcanza 5000 mm. Bajar
`grid_primary_support_mm` incorporara paredes mas cortas y aumentara la cantidad de
filas/columnas.

Comportamiento propio de ArchGrid: cada division atraviesa el rectangulo completo de la
cuadricula, aunque el muro fuente exista solo en una parte. Para evitar esas lineas de
mas, la version 0.4.9 mantiene el ArchGrid nativo oculto para compatibilidad y crea
`FA_GridWallTrace`, un `Sketcher::SketchObject` visible compuesto por los segmentos del
sketch de paredes reconstruidas y cierres ajustados desde puertas y ventanas. La red
se divide en sus cruces y las esquinas comparten vertices mediante restricciones
`Coincident`, ademas de restricciones `Horizontal` y `Vertical`. Ademas crea un muro
BIM nuevo desde ese trazado; no modifica ni elimina el muro original.

Los bordes exteriores del ArchGrid deben coincidir con la extension completa del sketch
cerrado, no solamente con las posiciones de paredes largas. El algoritmo 0.4.9 agrega o
ajusta esos limites usando los extremos globales de todos los segmentos fuente.

Puertas y ventanas no agregan divisiones a la cuadricula. Se usan en la etapa anterior
`FA Cerrar huecos de paredes` para reconstruir centros continuos. La finalidad expresada
por el usuario es que ArchGrid ayude a reconstruir las paredes sin los huecos de puertas
y ventanas.

La primera implementacion incorrecta creo seis objetos `Arch Axis/AxisSystem` con
`FA_GeneratedBy = FA_CreateBuildingGrid`. Esos seis objetos fueron eliminados. El codigo
actual reemplaza unicamente objetos con esa etiqueta y genera un solo ArchGrid.

## Codigo de la cuadricula

- Nucleo:
  `FacilArquitecturaWB/core/building_grid_utils.py`
- Comando:
  `FacilArquitecturaWB/commands/cmd_create_building_grid.py`
- Icono:
  `FacilArquitecturaWB/resources/icons/building_grid.svg`
- Pruebas:
  `FacilArquitecturaWB/tests/test_building_grid_utils.py`

El comando esta importado y registrado en `FacilArquitecturaWB/InitGui.py`. La macro de
recarga incluye `FA_CreateBuildingGrid` entre sus candidatos.

## Parametros y correccion no destructiva

Se corrigio `FacilArquitecturaWB/core/parameters.py`. Antes, al agregar un parametro
nuevo, podia reutilizar una fila ocupada. Ahora calcula la siguiente fila como
`max(existing.values()) + 1` y conserva parametros desconocidos o del usuario.

Se agrego la prueba de regresion:

`FacilArquitecturaWB/tests/test_parameters.py`

Durante la reparacion se restauraron los valores BIM:

- `column_width_mm = 400`
- `column_depth_mm = 400`
- `column_height_mm = 3000`

Las filas heredadas `grid_opening_tolerance_mm` y `grid_extension_mm` pueden permanecer
en la hoja por compatibilidad, pero la cuadricula 0.4.2 no las utiliza.

## Rotulos de recintos

Se integro la macro de rotulos como comando nativo:

`FA Recopilar rotulos de recintos`

Archivos:

- `FacilArquitecturaWB/core/room_label_utils.py`
- `FacilArquitecturaWB/commands/cmd_collect_room_labels.py`
- `FacilArquitecturaWB/resources/icons/room_labels.svg`
- `FacilArquitecturaWB/tests/test_room_label_utils.py`

Resultado en Puriscal:

- Hoja `Spreadsheet_Rotulos_Recintos`
- 25 nombres consolidados
- Columnas: nombre, area, tipo, ocupacion, XYZ, fuente y cantidad
- `FA_GeneratedBy = FA_CollectRoomLabels`

La macro `RecopilarRotulosRecintos.FCMacro` quedo como lanzador compatible del mismo
nucleo para evitar dos implementaciones divergentes.

## Analisis de areas y ElectricCR

La macro exclusiva `AnalizarAreasDesdeMuroBIM.FCMacro` exige seleccionar un unico muro
BIM. En Puriscal se valido con `Wall002`; sigue su enlace a `FA_GridWallTrace`, lee los
120 mm desde `Width` y crea 25 rectangulos con trazabilidad completa:

- 18 verdes: cuatro limites geometricos locales
- 6 azules: paredes mas limites confiables prolongados
- 1 morado: dos guias mas area objetivo
- 0 naranjas: ninguno depende solo del area programada

Totales de la ultima prueba: 360.124 m2 rectangulares frente a 364.310 m2 de programa;
diferencia -4.186 m2 (-1.15%). Desviacion relativa maxima: 9.84% en
`PASILLO PLATAFORMA`.

Quedan tres traslapes pequenos para revision: `PASILLO A PLATAFORMA` con
`DECLARACIONES` (1.009 m2), `PENSIONES` con `SALA DE ESPERA` (0.121 m2) y
`SALA LACTANCIA` con `SALA DE ESPERA` (0.028 m2).

Hoja: `Spreadsheet_Analisis_Areas`.

Propiedades de compatibilidad ElectricCR incluidas en los rectangulos:

- `ElectricCRTipo = Area`
- `AreaM2`
- `AreaID`
- `Recinto`
- `AreaNombre`
- `Habitacion`
- `Local`
- `Espacio`
- `Zona`
- `VirtualClosures`
- `Confidence`

El grupo de areas se conserva, pero quedo oculto temporalmente durante la revision de
puertas. Los 25 rectangulos contienen las propiedades ElectricCR completas y enlaces
`FA_SourceBIMWall = Wall002` y `FA_SourceCenterline = FA_GridWallTrace`. La hoja incluye
fila TOTAL y datos de fuente.

## Puertas BIM orientadas hacia los recintos

Se creo y ejecuto la macro independiente `InsertarPuertasBIMDesdeRecintos.FCMacro`.
Usa `Sketch_Centros_Puertas`, proyecta cada eje paralelo sobre `FA_GridWallTrace`,
identifica los recintos de ambos lados mediante `FA_RectangularAreas`, coloca la
bisagra en el extremo mas cercano a una esquina y orienta la apertura hacia el recinto.

Resultado actual:

- Grupo: `FA_BIMDoors`, dentro de `FA_BIM`.
- Hoja de informe: `Spreadsheet_Puertas_BIM`.
- 16 puertas nativas BIM `Simple door`, todas con `Wall002` como `Host`.
- 1 eje original rechazado por estar a unos 3143 mm del muro.
- 15 bisagras quedaron entre 62 y 117 mm de una esquina.
- La geometria de puerta 8 requiere revision: abre hacia `PASILLO PRINCIPAL`, esta a
  1437 mm de una esquina y tiene `FA_InferenceConfidence = 0.62`.
- Cada puerta conserva enlace al muro, eje fuente, indice geometrico, recinto destino,
  punto de bisagra, distancia a esquina, sentido de apertura y confianza.
- `Wall002` sigue valido y con un unico solido. Los huecos redujeron su volumen de
  84,355,183,826 a 80,483,186,999 mm3.
- El FCStd se guardo con las puertas y la vista limpia en planta.
- Capturas: `Puriscal_Puertas_BIM_Planta.png` y `Puriscal_Puertas_BIM_3D.png`.
- Revision posterior: se comprobo usando el centro de masa de la hoja abierta que las
  15 hojas quedan dentro del rectangulo del recinto enlazado. Se dejo el grupo temporal
  `FA_DoorReview`, con las areas visibles y una anotacion roja sobre la geometria 8.
  Captura: `Puriscal_Revision_Puertas_BIM.png`.
- Se detecto despues la puerta faltante de `PENSIONES`. No estaba en
  `Sketch_Centros_Puertas`, pero el Sketch original de paredes conservaba un hueco
  inferior de unos 1110 mm en su limite con `SALA DE ESPERA`; el hueco superior de
  1200 mm coincide con la ventana 7. Se agrego al Sketch un eje vertical inferido como
  geometria 16, ancho 944.5 mm, con restriccion `Vertical` y propiedades
  `FA_InferredDoorGeometryIndex`, `FA_InferredDoorCount` y `FA_InferredDoorReason`.
  La macro se volvio a ejecutar y creo la puerta BIM hacia `PENSIONES`, con bisagra a
  116.7 mm de la esquina. Captura: `Puriscal_Puerta_BIM_Pensiones.png`.

## Ventanas BIM desde ejes y recintos

Se creo y ejecuto `InsertarVentanasBIMDesdeRecintos.FCMacro` sobre `Wall002`. La macro
lee `Sketch_Centros_Ventanas`, proyecta sus ejes sobre lineas colineales completas de
`FA_GridWallTrace`, enlaza los recintos de ambos lados y crea presets nativos BIM.

Resultado actual:

- Grupo: `FA_BIMWindows`, dentro de `FA_BIM`.
- Hoja: `Spreadsheet_Ventanas_BIM`.
- 8 ventanas creadas y 0 ejes rechazados.
- Anchos: 600, 1200, 1800, 1990 y 5470 mm.
- Dos ventanas de 600 mm usan `Open 1-pane`; las seis restantes usan
  `Sliding 2-pane`.
- Antepecho 900 mm y altura 1200 mm, tomados de `Spreadsheet_Parametros`.
- Todas tienen `IfcType = Window`, `Opening = 0` y `Wall002` como `Host`.
- La linea de 5470 mm se conserva como un paño continuo; el algoritmo admite que el
  centro del muro este dividido en varios tramos colineales.
- `Wall002` conserva geometria valida y un unico solido. Su volumen paso de
  80,483,186,999 a 78,366,382,109 mm3 al abrir los ocho huecos.
- Capturas: `Puriscal_Ventanas_BIM_8_Isometrica.png` y
  `Puriscal_Ventanas_BIM_8_Planta.png`.

## Losa corregida

La losa habia quedado enorme porque el flujo incorporaba `Sketch_Centros_P4`. Se
corrigio excluyendo ese sketch de la huella arquitectonica.

Dimensiones aproximadas verificadas:

- 26061 mm de ancho
- 30245 mm de largo
- 150 mm de espesor

El DXF se esta tratando como geometria en milimetros, aproximadamente
`1 unidad DXF = 1 mm`.

## Pruebas y verificacion

Ultimo resultado local: 78 pruebas aprobadas.

Ejecutar desde:

`C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad`

Comando:

```powershell
python -m unittest discover -s 'FacilArquitecturaWB\tests' -p 'test_*.py'
```

Compilacion rapida:

```powershell
python -m compileall -q 'FacilArquitecturaWB'
```

## Como recargar sin cerrar FreeCAD

Ejecutar desde FreeCAD la macro:

`FacilArquitecturaLoader.FCMacro`

La macro purga modulos `FacilArquitecturaWB`, elimina comandos dinamicos antiguos,
recarga `InitGui`, activa el workbench y conserva visible el boton global de recarga.

Los nombres internos de comandos incluyen un sufijo temporal. Para localizarlos desde
Python usar el prefijo, por ejemplo:

```python
command = [
    name for name in FacilArquitecturaWB.InitGui.REGISTERED_COMMANDS
    if name.startswith("FA_CreateBuildingGrid_")
][-1]
```

## Punto recomendado para continuar

1. Revisar visualmente las 8 ventanas, especialmente el paño continuo de 5470 mm.
2. Revisar tambien la puerta de geometria 8, que conserva confianza `0.62`.
3. Si una abertura no corresponde, corregir su eje sin volver a generar la cuadricula
   autoritativa.
4. Mantener el conjunto generado: `Grid`, `FA_GridWallTrace`, `Wall002`, areas, puertas
   y ventanas.
5. Restaurar la visibilidad de `FA_RectangularAreas` solo cuando se necesite comprobar
   el recinto destino.
6. Guardar el FCStd despues de cada ajuste aceptado.
