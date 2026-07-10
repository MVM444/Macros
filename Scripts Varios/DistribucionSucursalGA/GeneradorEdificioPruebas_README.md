# GeneradorEdificioPruebas

Macro para FreeCAD que genera edificios sinteticos aleatorios para probar otras macros.

## Uso

1. Ejecutar `GeneradorEdificioPruebas.FCMacro`.
2. En el panel elegir:
   - `Tipo`: `Aleatorio`, `Casa` u `Oficina`.
   - `Semilla`: `0` usa una semilla nueva; un numero fijo repite el mismo edificio.
   - `Niveles`: cantidad de plantas.
   - `Ancho mm` y `Fondo mm`: `0` usa medidas automaticas.
   - `Muro mm` y `Texto mm`.
   - `Borrar edificios de prueba anteriores`.
   - `Copiar contexto IA al portapapeles`.
3. Presionar `Generar`.

La macro crea un grupo `TEST_Edificio_<timestamp>`.

## Objetos generados

- `Contorno`: perimetro del nivel.
- `Recintos`: areas con propiedades `RoomName`, `RoomKind`, `Area_m2`, `Width_mm`, `Depth_mm`, `Level`.
- `Muros`: caras rectangulares delgadas con `Role=muro`.
- `Puertas`: objetos con `Role=puerta` o `Role=salida`.
- `Ventanas`: objetos con `Role=ventana`.
- `Frente`: objeto con `Role=frente`.
- `Etiquetas`: textos centrados por recinto.
- `AI_Contexto_Edificio`: texto JSON para copiar y pegar en una IA externa.

## Integracion manual con IA

No usa API. Para trabajar con una IA externa:

1. Generar el edificio.
2. Abrir el objeto `AI_Contexto_Edificio`.
3. Copiar el JSON o activar `Copiar contexto IA al portapapeles`.
4. Pegar el contexto en la IA y pedir recomendaciones o modificaciones.

Una iteracion futura puede agregar un campo para pegar JSON de respuesta y reconstruir el edificio desde esa descripcion.
