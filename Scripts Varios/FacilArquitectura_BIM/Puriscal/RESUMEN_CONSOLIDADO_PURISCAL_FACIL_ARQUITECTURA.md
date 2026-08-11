# Resumen consolidado: Puriscal y Facil Arquitectura

Actualizado: 2026-07-26, zona horaria America/Costa_Rica.

## Resultado actual

Se reconstruyo el modelo arquitectonico de Puriscal a partir del DXF, se corrigio la
losa, se consolidaron los rotulos, se creo una cuadricula BIM y un Sketch autoritativo
de centros de pared, se genero un muro BIM continuo y se agregaron analisis de areas,
puertas y ventanas con trazabilidad.

Estado cuantitativo guardado:

- 25 recintos con rotulo y propiedades ElectricCR.
- 1 muro BIM principal: `Wall002`, 120 mm de espesor y 3000 mm de altura.
- 16 puertas nativas BIM alojadas en `Wall002`.
- 8 ventanas nativas BIM alojadas en `Wall002`.
- 0..3000 mm como limites verticales del muro.
- Geometria de muro valida y un unico solido.
- Volumen final del muro, despues de puertas y ventanas: 78,366,382,109 mm3.

## Archivos principales

- DXF fuente:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal.dxf`
- Modelo FreeCAD:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\2026\07-Julio-2026\Puriscal\Puriscal Flujo Completo Facil Arquitectura.FCStd`
- Workbench:
  `C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\Macros-de-Freecad\FacilArquitecturaWB`
- Documento de traspaso detallado:
  `HANDOFF_CODEX_PURISCAL.md`.

## Escala y fuente DXF

El DXF se interpreta en milimetros:

`1 unidad DXF = 1 mm`.

Las dimensiones generales y los espesores medidos son coherentes con esa escala. El
Sketch de muros detecto aproximadamente 120 mm de espesor.

## Losa corregida

La losa inicial quedo excesivamente grande porque el flujo incorporaba
`Sketch_Centros_P4`, que pertenece al sistema de columnas y no a la huella
arquitectonica. Se excluyo ese Sketch.

Dimensiones corregidas aproximadas:

- Ancho: 26,061 mm.
- Largo: 30,245 mm.
- Espesor: 150 mm.

## Rotulos de recintos

Se integro `RecopilarRotulosRecintos.FCMacro` con el comando nativo
`FA Recopilar rotulos de recintos`.

Resultado:

- Hoja: `Spreadsheet_Rotulos_Recintos`.
- 25 nombres consolidados.
- Datos: nombre, area, tipo, ocupacion, XYZ, fuente y cantidad.
- `FA_GeneratedBy = FA_CollectRoomLabels`.

El nombre de cada recinto proviene del texto importado del DXF y queda asociado a su
posicion. Esos nombres alimentan el analisis de areas y la trazabilidad de puertas y
ventanas.

## Cuadricula BIM y reconstruccion de paredes

Se reemplazo el enfoque incorrecto basado en multiples `Arch Axis/AxisSystem` por una
cuadricula BIM nativa creada con `Arch.makeGrid()`.

Objetos principales:

- `Grid`: ArchGrid BIM nativo, conservado oculto para compatibilidad.
- `FA_GridWallTrace`: Sketch editable que representa solamente los centros reales de
  pared, sin prolongaciones sobrantes.
- `Wall002`: muro BIM generado desde el Sketch anterior.

`FA_GridWallTrace` fue completado manualmente por el usuario y es la fuente
**autoritativa** del modelo:

- 67 geometrías.
- 148 restricciones.
- `FA_CenterlineKind = walls`.
- `FA_WallThickness = 120 mm`.
- `FA_WallHeight = 3000 mm`.

No se debe volver a ejecutar la generacion automatica de cuadricula sin guardar o
preservar primero esta version manual. El comando podria reemplazar el Sketch.

`Wall002` sigue parametricamente el Sketch, tiene espesor 120 mm, altura 3000 mm,
geometria valida y un solo solido. Es el muro anfitrion autoritativo para puertas y
ventanas.

## Analisis de areas

Macro:

`AnalizarAreasDesdeMuroBIM.FCMacro`.

La macro usa `Wall002`, su centro `FA_GridWallTrace`, los nombres de recintos y las
areas programadas. Produce rectangulos compatibles con ElectricCR.

Resultado:

- Grupo: `FA_RectangularAreas`.
- Hoja: `Spreadsheet_Analisis_Areas`.
- 25 recintos.
- Area programada: 364.310 m2.
- Area rectangular calculada: 360.124 m2.
- Diferencia: -4.186 m2, equivalente a -1.15%.
- 18 recintos resueltos con cuatro limites geometricos.
- 6 resueltos con muros y guias confiables.
- 1 resuelto con dos guias y area programada.
- Ninguno dependio unicamente del rectangulo programatico naranja.

Traslapes pequenos pendientes de revision:

- `PASILLO A PLATAFORMA` / `DECLARACIONES`: 1.009 m2.
- `PENSIONES` / `SALA DE ESPERA`: 0.121 m2.
- `SALA LACTANCIA` / `SALA DE ESPERA`: 0.028 m2.

Propiedades ElectricCR incluidas:

`ElectricCRTipo`, `AreaM2`, `AreaID`, `Recinto`, `AreaNombre`, `Habitacion`, `Local`,
`Espacio`, `Zona`, `VirtualClosures` y `Confidence`.

## Puertas BIM

Macro:

`InsertarPuertasBIMDesdeRecintos.FCMacro`.

Fuentes:

- `Sketch_Centros_Puertas`.
- `FA_GridWallTrace`.
- Rectangulos de `FA_RectangularAreas`.
- Muro anfitrion `Wall002`.

Metodo:

1. Proyecta cada eje de puerta sobre un tramo paralelo del muro.
2. Determina los recintos de ambos lados.
3. Favorece el recinto frente al espacio de circulacion.
4. Escoge como bisagra el extremo mas cercano a una esquina.
5. Orienta la hoja abierta hacia el interior del recinto.
6. Crea el preset BIM `Simple door`, con `Opening = 100` y `SymbolPlan = True`.
7. Asigna `Hosts = [Wall002]` para abrir el hueco real.

Resultado:

- Sketch fuente: 17 geometrías y 17 restricciones.
- 16 puertas BIM creadas.
- 1 eje original rechazado por estar a unos 3143 mm del muro.
- 15 puertas con bisagra entre 62 y 117 mm de una esquina.
- Puerta de geometria 8: abre hacia `PASILLO PRINCIPAL`, esta a 1437 mm de una
  esquina y conserva confianza `0.62` para revision.
- Grupo: `FA_BIMDoors`.
- Hoja: `Spreadsheet_Puertas_BIM`.

Puerta de `PENSIONES`:

- Faltaba en el Sketch original de puertas.
- Se detecto un hueco inferior de unos 1110 mm en la pared original; el hueco superior
  de 1200 mm corresponde a una ventana.
- Se agrego el eje inferido como geometria 16, con restriccion vertical.
- Ancho BIM: 944.5 mm.
- Bisagra a 116.7 mm de la esquina.
- Apertura hacia el interior de `PENSIONES`.

Volumen de muro:

- Antes de puertas: 84,355,183,826 mm3.
- Despues de 16 puertas: 80,483,186,999 mm3.

## Ventanas BIM

Macro:

`InsertarVentanasBIMDesdeRecintos.FCMacro`.

Fuentes:

- `Sketch_Centros_Ventanas`: 8 geometrías y 8 restricciones.
- `FA_GridWallTrace`.
- `FA_RectangularAreas`.
- `Wall002`.

Parametros tomados de `Spreadsheet_Parametros`:

- Antepecho: 900 mm.
- Altura: 1200 mm.
- Profundidad: espesor real del muro, 120 mm.

Presets:

- Dos ventanas de 600 mm: `Open 1-pane`.
- Seis ventanas de 1200, 1800, 1990 y 5470 mm: `Sliding 2-pane`.

Resultado:

- 8 ventanas BIM creadas.
- 0 ejes rechazados.
- Todas con `IfcType = Window`, `Opening = 0`, `SymbolPlan = True` y
  `Hosts = [Wall002]`.
- Todas ocupan Z = 900..2100 mm.
- Confianza `0.95` en las ocho.
- Grupo: `FA_BIMWindows`.
- Hoja: `Spreadsheet_Ventanas_BIM`.

La ventana de 5470 mm se conserva como un paño continuo porque asi aparece en el
Sketch fuente. El algoritmo permite que su muro anfitrion este dividido en varios
tramos colineales.

Volumen de muro:

- Antes de ventanas: 80,483,186,999 mm3.
- Despues de ventanas: 78,366,382,109 mm3.

## Trazabilidad y repeticion de macros

Las macros de areas, puertas y ventanas reemplazan solamente sus propios resultados,
identificados mediante `FA_GeneratedBy`. No eliminan objetos manuales ni regeneran la
cuadricula.

Identificadores principales:

- Areas: `FA_RectangularAreaAnalysis`.
- Puertas: `FA_InsertDoorsBIM`.
- Ventanas: `FA_InsertWindowsBIM`.

Cada puerta y ventana conserva enlaces al muro, centro del muro, Sketch fuente, indice
geometrico, medidas, recintos relacionados y confianza de inferencia.

## Workbench y validacion

Facil Arquitectura:

- Version: `0.4.9`.
- Build: `2026.07.26.11`.
- 12 comandos registrados.
- Ultima ejecucion de pruebas: 78 pruebas aprobadas.

Macros de trabajo principales:

- `FacilArquitecturaLoader.FCMacro`: recarga en vivo sin cerrar FreeCAD.
- `RecopilarRotulosRecintos.FCMacro`.
- `AnalizarAreasDesdeMuroBIM.FCMacro`.
- `InsertarPuertasBIMDesdeRecintos.FCMacro`.
- `InsertarVentanasBIMDesdeRecintos.FCMacro`.

Documentacion especializada:

- `ANALISIS_AREAS_DESDE_MURO_BIM.md`.
- `PUERTAS_BIM_ORIENTADAS_POR_RECINTOS.md`.
- `VENTANAS_BIM_DESDE_RECINTOS.md`.
- `HANDOFF_CODEX_PURISCAL.md`.

## Capturas principales

- `Puriscal_Muros_BIM_desde_Cuadricula_Manual.png`.
- `Puriscal_Analisis_Areas_Desde_Muro_BIM.png`.
- `Puriscal_Puertas_BIM_Planta.png`.
- `Puriscal_Puertas_BIM_16_Isometrica.png`.
- `Puriscal_Puerta_BIM_Pensiones.png`.
- `Puriscal_Ventanas_BIM_8_Planta.png`.
- `Puriscal_Ventanas_BIM_8_Isometrica.png`.

## Estado visual guardado

- Vista isometrica.
- `Wall002` visible con 48% de transparencia.
- 16 puertas visibles.
- 8 ventanas azules visibles.
- Areas, anotaciones de revision y sketches fuente ocultos temporalmente.

## Puntos pendientes o recomendados

1. Revisar la puerta de geometria 8 por su distancia de 1437 mm a la esquina.
2. Confirmar si la ventana de 5470 mm debe permanecer como un solo paño o dividirse en
   modulos.
3. Revisar los tres traslapes pequenos del analisis rectangular.
4. No regenerar `FA_GridWallTrace` sin preservar las modificaciones manuales.
5. Guardar el FCStd despues de cualquier ajuste aceptado.

