# GeneradorEdificioArchWallPruebas

Macro de prueba para FreeCAD que genera una casa u oficina con sketches base y paredes `Arch Wall`.

Esta version es distinta de `GeneradorEdificioSketchPruebas.FCMacro`: aqui la prioridad es probar flujo BIM paramétrico desde sketches.

## Uso

1. Ejecutar `GeneradorEdificioArchWallPruebas.FCMacro`.
2. Elegir tipo, semilla, niveles, dimensiones y espesores.
3. Mantener activo `Generar Arch Wall con buques parametricos`.
4. Presionar `Generar`.

## Estructura

Por cada nivel crea sketches:

- `SK_ConcretoExterior_Nxx`: ejes de paredes exteriores.
- `SK_ParedesLivianas_Nxx`: ejes de paredes interiores.
- `SK_BuquesPuertas_Nxx`: ejes de buques de puertas.
- `SK_BuquesVentanas_Nxx`: ejes de buques de ventanas.
- `SK_ReferenciaRecintos_Nxx`: referencia constructiva.

Y crea BIM:

- `ArchWall_Paredes_Nxx`
- `ArchWall_Cutters_Buques_Nxx`
- `ArchWall_Elementos_Nxx`

## Logica BIM

- `ArchWall_Paredes_Exteriores_Nxx` se crea con `Arch.makeWall(SK_ConcretoExterior_Nxx)`.
- `ArchWall_Paredes_Livianas_Nxx` se crea con `Arch.makeWall(SK_ParedesLivianas_Nxx)`.
- `Cutter_Buques_Puertas_Nxx` lee el sketch de puertas y genera solidos de corte.
- `Cutter_Buques_Ventanas_Nxx` lee el sketch de ventanas y genera solidos de corte.
- Los cutters se asignan a `Subtractions` de los muros.

Si editas un sketch de pared, el `Arch Wall` mantiene su base vinculada al sketch. Si editas un sketch de buques, el cutter se recalcula y el muro debe actualizar sus huecos al recomputar.

## Nota

Los objetos `ArchWall_Puertas_Nxx` y `ArchWall_Ventanas_Nxx` son representaciones simples para pruebas. Los huecos reales los hacen los cutters en `Subtractions`; no son familias completas de puerta/ventana.
