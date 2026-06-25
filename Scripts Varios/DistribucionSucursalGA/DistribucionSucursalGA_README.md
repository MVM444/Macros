# DistribucionSucursalGA (MVP)

Macro para FreeCAD que genera propuestas de distribucion arquitectonica (2D) usando algoritmo genetico.

## Archivos

- `DistribucionSucursalGA.FCMacro`
- `programa_sucursal_template.csv`

## Preparacion en FreeCAD

1. Dibuja el local vacio como `Sketch`, `Wire` o `Face` cerrada.
2. Seleccionalo primero.
3. Opcional: selecciona objetos auxiliares con etiquetas:
   - `FRENTE_*`: linea/objeto lineal de fachada o frente.
   - `PUERTA_*`: puerta/acceso principal.
   - `SALIDA_*`: salida de emergencia.
4. Recomendado por propiedades:
   - define propiedad booleana `IsFixed`/`Fija` para marcar zonas fijas,
   - opcionalmente define propiedad de rol (`Role`/`Rol`/`GA_Role`) con valores `frente`, `puerta`, `salida`, `fijo`.

## Ejecucion

1. Ejecuta `DistribucionSucursalGA.FCMacro` (abre un panel persistente).
2. En el panel:
   - define `Objeto base`,
   - define `Spreadsheet` (o deja `<Auto>`),
   - opcionalmente define archivo `CSV/XLSX`,
   - usa `Capturar seleccion` si quieres tomar base/sheet desde la seleccion actual.
3. Ajusta parametros:
   - `Propuestas`,
   - `Corridas GA` (mas corridas = mas diversidad),
   - `Generaciones`,
   - `Poblacion`,
   - `Texto (100..200 mm)`,
   - `Borrar propuestas anteriores`,
   - `Acomodo realista`.
4. En el panel puedes marcar la seleccion actual con botones:
   - `Marcar Frente`
   - `Marcar Puerta`
   - `Marcar Salida`
   - `Marcar Fijo`
   - `Limpiar Marca`
5. Recomendacion geometrica:
   - `Frente/Puerta/Salida`: usar lineas o puntos.
   - `Fijo`: usar areas (caras/contornos cerrados) para bloquear superficie.
6. Presiona `Ejecutar`. El panel no se cierra y recuerda la configuracion para la proxima ejecucion.
7. Se crea un grupo `GA_Sucursal_<timestamp>` con las propuestas.

## Formato de tabla funcional

Columnas reconocidas (sin acentos, mayusculas o guiones tambien funcionan):

- nombre: `nombre`, `recinto`, `ambiente`, `espacio`
- area objetivo: `area_m2`, `area`, `m2`, `superficie`
- area minima (opcional): `min_m2`, `area_min`
- area maxima (opcional): `max_m2`, `area_max`
- tipo (opcional): `tipo`, `categoria`
- preferir frente (opcional): `prefer_frente`, `frente` (`si/no`)
- adyacencias (opcional): `adyacente_a` (separadores `|`, `,`, `;`)
- prioridad (opcional): `prioridad`, `peso`

## Alcance actual (MVP)

- Planta 2D con recintos rectangulares.
- Penaliza traslapes fuertes, falta de separacion minima, salida del contorno, invadir zonas fijas, mala cercania a frente/puerta/salida y adyacencias incumplidas.
- Penaliza ubicaciones fuera de zona funcional esperada (frente/publico, intermedio/administrativo, fondo/logistica-servicios) para mejorar realismo.
- Genera diversidad entre propuestas para no mostrar solo variantes casi iguales.
- Si una fila viene con `tipo=circulacion`, se toma como area reservada y no se dibuja como recinto solido (evita resultados apilados).
- Los recintos generados incluyen propiedades (`RoomName`, `RoomKind`, `TargetArea_m2`, `Priority`, `IsFixed`, `IsCirculation`) para flujos posteriores.
- Cada propuesta crea subgrupos `Recintos`, `Etiquetas` y `Vinculos Etiquetas`.
- Las etiquetas se reposicionan al centro del recinto en cada recompute del documento (si mueves rectangulos, recomputa para actualizar texto).

## Siguiente iteracion sugerida

- Soporte de recintos poligonales.
- Regla de corredores y conectividad.
- Multi-piso (`piso` en tabla).
- Optimizacion multiobjetivo (Pareto) y comparador de propuestas.
