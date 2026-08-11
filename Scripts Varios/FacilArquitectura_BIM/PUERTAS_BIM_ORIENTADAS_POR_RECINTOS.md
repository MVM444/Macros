# Puertas BIM orientadas por recintos

## Macro

`InsertarPuertasBIMDesdeRecintos.FCMacro`

La macro inserta puertas batientes nativas de BIM mediante el preset `Simple door`.
Las puertas quedan alojadas en el muro BIM, abren huecos reales y muestran su simbolo
de apertura en planta.

## Fuentes utilizadas

- Muro anfitrion: `Wall002`.
- Centro parametrico del muro: `FA_GridWallTrace`.
- Ejes originales de puertas: `Sketch_Centros_Puertas`.
- Recintos: rectangulos ElectricCR del grupo `FA_RectangularAreas`.

La cuadricula manual, el Sketch de paredes y los ejes originales no se modifican.

## Metodo de inferencia

Para cada segmento de `Sketch_Centros_Puertas`, la macro:

1. Busca un tramo paralelo en el Sketch central del muro y proyecta sobre el sus dos
   extremos.
2. Rechaza el eje si esta a mas de 250 mm del muro o si su ancho no es plausible.
3. Muestrea ambos lados del muro para identificar los recintos conectados.
4. Cuando hay un recinto y un espacio de circulacion, favorece el recinto. Entre dos
   recintos favorece el de menor area.
5. Usa como bisagra el extremo proyectado mas cercano a una esquina del rectangulo del
   recinto escogido.
6. Orienta la hoja abierta hacia el interior de ese recinto.
7. Crea una puerta BIM de 2100 mm de altura, con el ancho medido en el eje y profundidad
   igual al espesor real del muro.
8. Asigna `Hosts = [Wall002]`, con lo que BIM sustrae el hueco del muro.

Las puertas se crean con `Opening = 100` y `SymbolPlan = True`.

## Uso

1. Abrir `Puriscal Flujo Completo Facil Arquitectura.FCStd`.
2. Mantener disponible el analisis de areas `FA_RectangularAreas`.
3. Seleccionar `Wall002` (recomendado) y ejecutar
   `InsertarPuertasBIMDesdeRecintos.FCMacro`.
4. Revisar el grupo `FA_BIMDoors` y la hoja `Spreadsheet_Puertas_BIM`.

Una nueva ejecucion reemplaza solamente las puertas, bases, grupo y hoja que tengan
`FA_GeneratedBy = FA_InsertDoorsBIM`. No reemplaza puertas creadas manualmente.

## Trazabilidad

Cada puerta contiene, entre otras, las propiedades:

- `FA_SourceWall` y `FA_SourceDoorAxes`.
- `FA_SourceGeometryIndex`.
- `FA_TargetRoom` y `FA_TargetRoomName`.
- `FA_HingeEndpoint` y `FA_HingePoint`.
- `FA_CornerDistance` y `FA_WallOffset`.
- `FA_OpensInward`, `FA_OpeningSide` y `FA_InferenceConfidence`.

## Resultado validado en Puriscal

- 17 ejes examinados: 16 originales y 1 eje inferido agregado al Sketch.
- 16 puertas BIM creadas.
- 1 eje rechazado: geometria 0, aislada a unos 3143 mm del muro mas cercano.
- 15 puertas con bisagra entre 62 y 117 mm de una esquina del recinto.
- 1 puerta para revision: geometria 8, orientada hacia `PASILLO PRINCIPAL`, con
  distancia de 1437 mm a la esquina y confianza `0.62`.
- La puerta de `PENSIONES` es la geometria 16. Su eje se infirio del hueco inferior de
  1110 mm observado en el Sketch original de paredes; el hueco superior corresponde a
  la ventana 7 de 1200 mm. Tiene 944.5 mm de ancho, bisagra a 116.7 mm de la esquina y
  abre hacia el interior de `PENSIONES`.
- Las 16 puertas tienen `Wall002` como anfitrion y apertura del 100%.
- `Wall002` permanece valido y con un unico solido.
- Volumen antes de abrir huecos: 84,355,183,826 mm3.
- Volumen despues de abrir huecos: 80,483,186,999 mm3.
- Volumen sustraido: 3,871,996,827 mm3.

Capturas:

- `Puriscal_Puertas_BIM_Planta.png`.
- `Puriscal_Puertas_BIM_3D.png`.
- `Puriscal_Puerta_BIM_Pensiones.png`.
