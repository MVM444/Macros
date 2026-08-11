# Analisis de areas desde un muro BIM

## Macro exclusiva

`AnalizarAreasDesdeMuroBIM.FCMacro`

La macro exige seleccionar un unico muro BIM. Para Puriscal, la fuente validada es
`Wall002`, cuya base parametrica es `FA_GridWallTrace`.

## Uso

1. Abrir `Puriscal Flujo Completo Facil Arquitectura.FCStd`.
2. Seleccionar solamente el muro BIM `Wall002`.
3. Ejecutar `AnalizarAreasDesdeMuroBIM.FCMacro`.
4. Revisar el grupo `FA_RectangularAreas` y la hoja
   `Spreadsheet_Analisis_Areas`.

La macro reemplaza el analisis rectangular generado en una ejecucion anterior, pero
no modifica el muro BIM, su Sketch base ni los rotulos de recintos.

## Fuente geometrica y trazabilidad

El muro BIM seleccionado es la fuente principal. La macro sigue su propiedad
`FA_SourceSketch` o `Base` para leer las lineas centrales, y obtiene el espesor real
desde `Width`. De esta forma evita interpretar dos veces las caras laterales del
solido.

El grupo, la hoja y cada rectangulo guardan:

- `FA_SourceBIMWall`: muro BIM analizado.
- `FA_SourceCenterline`: Sketch base del muro.
- `FA_GeneratedBy = FA_RectangularAreaAnalysis`.
- `FA_WallThickness` en el grupo de resultados.

Cada rectangulo conserva tambien las propiedades ElectricCR `ElectricCRTipo = Area`,
`AreaM2`, `AreaID`, `Recinto`, `AreaNombre`, `Habitacion`, `Local`, `Espacio`, `Zona`,
`VirtualClosures` y `Confidence`.

## Metodo

Para cada rotulo con nombre y area programada, la macro busca primero cuatro limites
locales derivados de los centros de pared y desplaza esos limites la mitad del espesor
del muro. Cuando faltan limites fisicos, combina prolongaciones confiables, rectangulos
ya resueltos y mediatrices entre rotulos. Como ultimo respaldo usa el area indicada en
el rotulo.

Los colores indican el metodo:

- Verde: cuatro limites geometricos locales.
- Azul: muros y guias prolongadas.
- Morado: dos guias y area programada.
- Naranja: dimensiones derivadas del area programada.

## Limitaciones

El resultado es un analisis rectangular compatible con ElectricCR; no sustituye una
medicion poligonal cuando un recinto tenga forma irregular. Los espacios abiertos sin
una pared fisica suficiente pueden requerir una guia o ajuste manual.

## Resultado validado en Puriscal

Fuente: `Wall002`, con `FA_GridWallTrace` como Sketch base y 120 mm de espesor.

- 25 recintos.
- Area programada total: 364.310 m2.
- Area rectangular calculada: 360.124 m2.
- Diferencia total: -4.186 m2 (-1.15%).
- 18 recintos verdes con cuatro limites fisicos.
- 6 recintos azules resueltos con muros y guias.
- 1 recinto morado resuelto con dos guias y area programada.
- Ningun recinto dependio exclusivamente del rectangulo programatico naranja.

Mayores diferencias individuales:

- `PASILLO PLATAFORMA`: +1.771 m2 (+9.84%).
- `PASILLO SALIDA TRASERA`: -2.247 m2 (-7.70%).
- `COMEDOR`: -1.220 m2 (-5.03%).
- `ARCHIVO`: -2.407 m2 (-4.27%).

Traslapes restantes para revision:

- `PASILLO A PLATAFORMA` con `DECLARACIONES`: 1.009 m2.
- `PENSIONES` con `SALA DE ESPERA`: 0.121 m2.
- `SALA LACTANCIA` con `SALA DE ESPERA`: 0.028 m2.

Captura:

`Puriscal_Analisis_Areas_Desde_Muro_BIM.png`
