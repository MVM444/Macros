# GeneradorEdificioSketchPruebas

Macro para FreeCAD que genera edificios sinteticos usando `Sketcher::SketchObject`.

Esta version deja intacta `GeneradorEdificioPruebas.FCMacro` y crea una alternativa orientada a probar macros que leen sketches.

## Uso

1. Ejecutar `GeneradorEdificioSketchPruebas.FCMacro`.
2. Elegir:
   - `Tipo`: `Aleatorio`, `Casa` u `Oficina`.
   - `Semilla`: `0` genera una semilla nueva; otro numero repite el resultado.
   - `Niveles`: 1 a 5.
   - `Ancho mm` y `Fondo mm`: `0` usa dimensiones automaticas.
   - `Muro exterior mm`.
   - `Pared liviana mm`.
   - `Generar BIM de muros y buques`.
   - Alturas de muro, puerta, antepecho y ventana.
   - `Borrar edificios Sketch anteriores`.
   - `Copiar contexto IA al portapapeles`.
3. Presionar `Generar`.

## Grupo generado

La macro crea un grupo `TEST_SketchEdificio_<timestamp>`.

Por cada nivel crea:

- `SK_ConcretoExterior_Nxx`: lineas de centro de paredes exteriores/concreto.
- `SK_ParedesLivianas_Nxx`: lineas de centro de paredes interiores/livianas.
- `SK_BuquesPuertas_Nxx`: lineas de centro de buques de puertas.
- `SK_BuquesVentanas_Nxx`: lineas de centro de buques de ventanas.
- `SK_ReferenciaRecintos_Nxx`: lineas constructivas de referencia de recintos.

Si `Generar BIM de muros y buques` esta activo, tambien crea:

- `BIM_Nivel_Nxx`
- `BIM_Paredes_Nxx`
- `BIM_Buques_Nxx`
- `BIM_Puertas_Ventanas_Nxx`
- `BIM_EjesBase_Nxx`

Los muros se crean desde los mismos ejes de sketch y se agrupan por categoria:

- `BIM_Paredes_Exteriores_Nxx`
- `BIM_Paredes_Livianas_Nxx`

Los buques se crean desde sus sketches y se usan para cortar las paredes:

- `BIM_Buques_Puertas_Nxx`
- `BIM_Buques_Ventanas_Nxx`

Tambien se generan elementos simples:

- `BIM_Puertas_Nxx`
- `BIM_Ventanas_Nxx`

Los buques quedan visibles como solidos transparentes para auditoria, pero ya fueron restados de las paredes mediante booleanos. Por eso las paredes resultantes tienen orificios reales.

Las paredes interiores se calculan por solape parcial entre recintos, no solo por bordes completos identicos. Esto evita perder paredes cuando un recinto largo colinda con dos recintos mas pequenos.

Las puertas y ventanas se calculan desde el mismo eje que la pared donde se ubican. Por eso los segmentos de `SK_BuquesPuertas_Nxx` y `SK_BuquesVentanas_Nxx` quedan colineales con `SK_ConcretoExterior_Nxx` o `SK_ParedesLivianas_Nxx`.

Reglas actuales:

- Solo se genera una puerta principal en el frente.
- Las ventanas solo se generan sobre el perimetro exterior real.
- No se genera una ventana sobre el mismo tramo de la puerta principal.
- Las puertas interiores se generan donde un recinto comparte tramo con una circulacion.

## Propiedades

Cada sketch recibe propiedades:

- `Role`
- `GA_Role`
- `SketchPurpose`
- `Level`
- `BuildingType`
- `Width_mm`
- `Depth_mm`

Esto permite que otras macros detecten rapidamente que sketch contiene muros, puertas, ventanas o referencias.

Los objetos BIM reciben propiedades como:

- `Role`
- `GA_Role`
- `WallKind`
- `OpeningKind`
- `OpeningId`
- `OpeningsCut`
- `Thickness_mm`
- `Width_mm`
- `Depth_mm`
- `Height_mm`
- `Level`

## Integracion manual con IA

No usa API. Genera un objeto `AI_Contexto_SketchEdificio` con JSON del edificio, niveles, sketches, recintos, puertas y ventanas. En puertas y ventanas el JSON incluye `centerline`, con los extremos exactos del segmento dibujado.

Ese texto se puede copiar y pegar en una IA externa para pedir ajustes o documentacion.

## Nota tecnica

Sketcher no es un buen contenedor para etiquetas de texto. Por eso los nombres de recintos se guardan en el JSON y el sketch de referencia dibuja rectangulos constructivos, pero no textos.
