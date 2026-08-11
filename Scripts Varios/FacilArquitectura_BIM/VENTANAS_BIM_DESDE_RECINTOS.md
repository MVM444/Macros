# Ventanas BIM desde ejes y recintos

## Macro

`InsertarVentanasBIMDesdeRecintos.FCMacro`

La macro convierte los segmentos de `Sketch_Centros_Ventanas` en ventanas nativas
del Workbench BIM, las proyecta sobre el centro de `Wall002` y las asigna como objetos
anfitriones del muro para producir huecos reales.

## Parametros

Los valores se leen de `Spreadsheet_Parametros`:

- `window_sill_mm = 900`: altura de antepecho.
- `window_height_mm = 1200`: altura del buque.
- Profundidad del marco: espesor real de `Wall002`, 120 mm.

Seleccion automatica de preset BIM:

- Anchos menores de 900 mm: `Open 1-pane`.
- Anchos de 900 mm o mayores: `Sliding 2-pane`.

Las ventanas se crean cerradas, con `Opening = 0`, `SymbolPlan = True` e
`IfcType = Window`.

## Metodo

1. Lee cada eje de `Sketch_Centros_Ventanas`.
2. Busca una linea colineal en `FA_GridWallTrace` y proyecta los extremos sobre ella.
3. Agrupa tramos colineales del muro para admitir ventanas que atraviesan divisiones
   internas del Sketch, como el eje de 5470 mm.
4. Rechaza ejes separados mas de 250 mm del muro o fuera de su extension.
5. Muestrea ambos lados para enlazar los rectangulos ElectricCR adyacentes.
6. Crea el preset BIM a Z = 900 mm y le asigna `Hosts = [Wall002]`.

Una nueva ejecucion reemplaza solamente objetos con
`FA_GeneratedBy = FA_InsertWindowsBIM`. No modifica las ventanas manuales, el Sketch
fuente, la cuadricula ni las puertas BIM.

## Trazabilidad

Grupo: `FA_BIMWindows`, dentro de `FA_BIM`.

Hoja: `Spreadsheet_Ventanas_BIM`.

Cada ventana conserva:

- `FA_SourceWall`, `FA_SourceCenterline` y `FA_SourceWindowAxes`.
- `FA_SourceGeometryIndex` y `FA_WallOffset`.
- `FA_SillHeight` y `FA_WindowHeight`.
- `FA_PresetName`.
- `FA_AdjacentRooms` y `FA_AdjacentRoomNames`.
- `FA_InferenceConfidence`.

## Resultado validado en Puriscal

| Eje | Ancho mm | Preset | Desfase mm | Recintos detectados |
|---:|---:|---|---:|---|
| 0 | 1200 | Sliding 2-pane | 0 | JEFATURA / PASILLO A PLATAFORMA |
| 1 | 1200 | Sliding 2-pane | 0 | JEFATURA / PASILLO PLATAFORMA |
| 2 | 600 | Open 1-pane | 0 | INGRESOS / COBROS |
| 3 | 600 | Open 1-pane | 0 | EGRESOS |
| 4 | 1990 | Sliding 2-pane | 0 | DECLARACIONES / SALA DE ESPERA |
| 5 | 5470 | Sliding 2-pane | 10 | SALA DE ESPERA |
| 6 | 1800 | Sliding 2-pane | 10 | SALA DE ESPERA / CAJA |
| 7 | 1200 | Sliding 2-pane | 14 | SALA DE ESPERA / PENSIONES |

Resultado general:

- 8 ejes examinados.
- 8 ventanas BIM creadas y 0 rechazadas.
- Confianza `0.95` en las ocho ventanas.
- Todas ocupan Z = 900..2100 mm.
- Todas tienen `Wall002` como anfitrion.
- `Wall002` sigue valido y con un unico solido.
- Volumen antes de ventanas: 80,483,186,999 mm3.
- Volumen despues de ventanas: 78,366,382,109 mm3.
- Volumen sustraido por ventanas: 2,116,804,890 mm3.

Capturas:

- `Puriscal_Ventanas_BIM_8_Isometrica.png`.
- `Puriscal_Ventanas_BIM_8_Planta.png`.

