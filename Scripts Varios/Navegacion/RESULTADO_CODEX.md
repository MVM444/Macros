# Resultado Codex - Recorrido3D v013 diagnostica

## Resultado v014 - prueba con View3D.viewPosition

Fecha: 2026-08-12
FreeCAD probado: 1.1.3 Windows
Estado: IMPLEMENTADA / COMPILADA / PRUEBA TECNICA FALLIDA / PENDIENTE

Se creo `ElectricCR_Recorrido3D_v014.FCMacro` a partir de v013. La parte de
`ShortcutOverride`, `KeyPress`, `KeyRelease`, filtros, temporizador de 33 ms y
Escape se conserva. Se retiro la manipulacion directa del nodo Inventor y la
version nueva usa exclusivamente `view.viewPosition()` para leer y escribir
`App.Placement`. Se agrego la tecla T para el salto diagnostico de
`X+5000/Y+5000/Z+2000` y registro de la posicion real despues de cada llamada.

### Prueba realizada

1. La macro compilo con `python -m py_compile`.
2. Se inicio una instancia limpia de FreeCAD 1.1.3 sin documento de trabajo y
   se creo un documento temporal vacio.
3. Una prueba aislada de solo lectura con `view.viewPosition()` bloqueo el
   despacho GUI y termino en `GUI dispatch timed out after 90s`.
4. La prueba de escritura con `view.viewPosition(placement, 0, 0)` produjo el
   mismo bloqueo. No se pudo obtener `Camera Placement inicial`, ni ejecutar
   de forma segura T, W, A, S o D.
5. Las instancias de prueba vacias fueron cerradas. No se modifico ni guardo
   ningun FCStd.

### Conclusion provisional

En esta instalacion concreta de FreeCAD 1.1.3, `view.viewPosition()` no es una
API utilizable desde el hilo GUI para esta prueba: incluso la lectura aislada
bloquea el despacho. Por tanto no se puede demostrar que `viewPosition()` mueva
visualmente la camara. Recorrido3D queda **PENDIENTE / NO VIABLE CON ESTA API EN
LA PRUEBA ACTUAL**. No se agregan raton, colisiones, HUD ni otras funciones.

La v013 permanece intacta como referencia de teclado y la v014 se conserva
como prueba reproducible del comportamiento de la API. La tarea no se declara
viable hasta que una version futura de FreeCAD o una ruta oficial alternativa
permita leer y escribir el `App.Placement` de la camara sin bloquear el visor.

Fecha: 2026-08-12

## Hallazgo de la prueba manual v012

La prueba sintetica de `KeyPress W` no reprodujo el flujo real de shortcuts de
Qt. En uso manual, FreeCAD procesaba `ShortcutOverride` antes del `KeyPress` y
activaba sus comandos normales; por ejemplo, S abria el panel o comando de
estilo. Por eso el movimiento sintetico de la v012 fue un falso positivo y no
demostro que el teclado fisico estuviera bajo control del recorrido.

## Alcance v013

`ElectricCR_Recorrido3D_v013.FCMacro` deriva de la v012 y conserva la prueba
minima de teclado para FreeCAD 1.1.3 en Windows.

Mientras el controlador esta activo, el filtro global procesa
`QEvent.ShortcutOverride` para W, A, S, D y Shift, acepta el evento y evita que
los `QShortcut` o `QAction` normales de FreeCAD consuman esas teclas. Despues
se procesa el `KeyPress` y el `KeyRelease` correspondiente. Al ejecutar
`stop()`, el filtro se elimina y los shortcuts normales de FreeCAD quedan
disponibles inmediatamente, sin modificar preferencias del usuario.

Escape conserva su `QShortcut` de contexto de aplicacion como ruta de salida
independiente.

## Alcance historico v012

`ElectricCR_Recorrido3D_v012.FCMacro` es ahora una prueba deliberadamente
minima de teclado para FreeCAD 1.1.3 en Windows. La v011 permanece sin cambios
como referencia del fallo.

## Jerarquia confirmada en FreeCAD 1.1.3

La vista activa expone esta jerarquia real:

- `QMdiSubWindow`
- `Gui::View3DInventorViewer`, con foco y el tamano de la vista activa
- `QOpenGLWidget`, hijo directo de `Gui::View3DInventorViewer`, tambien con foco

La v012 ya no elige el QOpenGLWidget visible de mayor tamano. Parte de la
subventana MDI activa, identifica por nombre de clase el
`Gui::View3DInventorViewer` visible y despues exige su `QOpenGLWidget` hijo
directo. Ambos se describen en la consola antes de instalar filtros.

FreeCAD puede devolver `activeSubWindow() = None` cuando la ventana pierde el
foco aunque el documento y `activeView()` sigan siendo validos. En ese caso se
revisan las subventanas visibles y solo se acepta un viewer con foco o un unico
viewer visible; una situacion ambigua produce error en vez de elegir por tamano.

## Cambios respecto a la v012 anterior

- Se retiro completamente mouse-look.
- Se retiraron `QCursor.setPos`, `BlankCursor`, recentrado y toda manipulacion
  del cursor.
- Se retiro toda llamada a `grabMouse` y `releaseMouse`.
- Se retiraron HUD y punto de mira durante esta etapa diagnostica.
- Se conservaron unicamente W, A, S, D, Shift y Escape.
- El timer cambio de 16 ms a 33 ms.
- El timer retorna inmediatamente si no hay W, A, S o D presionada.
- La orientacion se escribe una sola vez al iniciar; no se reescribe en cada
  tick.
- La posicion se escribe solamente cuando existe movimiento de teclado.
- Cada KeyPress y KeyRelease relevante se registra temporalmente en consola.
- Escape dispone de dos rutas: filtro global de `QApplication` y `QShortcut`
  de contexto de aplicacion en la ventana principal.
- `stop()` detiene timer, limpia teclas, elimina filtros, elimina el shortcut y
  limpia el singleton sin alterar objetos del documento.

## Posicion inicial

- Camara: `(0, 0, 0)`.
- Z global vertical.
- Mirada horizontal hacia `+Y`.

## Funciones excluidas

No existen en el flujo de la v012:

- colisiones, cache de solidos o `isInside`;
- WALK/FLY, Q/E o rueda de velocidad;
- mouse-look o captura del cursor;
- focal point, posicion previa o busqueda del centro del modelo.

## Prueba manual requerida

1. Ejecutar v013 y confirmar Perspective, origen `(0,0,0)` y respuesta normal.
2. Pulsar Escape y confirmar salida inmediata.
3. Ejecutar otra vez y pulsar S. Deben aparecer `ShortcutOverride S` y
   `KeyPress S`, sin abrir el panel de estilo.
4. Soltar S y confirmar `KeyRelease S`.
5. Repetir con W, A y D; confirmar movimiento continuo y Shift.
6. Salir con Escape y pulsar S nuevamente para confirmar que el shortcut normal
   de FreeCAD fue restaurado.

No se debe agregar raton hasta aprobar esta secuencia.

## Limite de la validacion automatizada anterior

- La camara inicio exactamente en `(0, 0, 1700)` en la v012.
- Un tick sin teclas no modifico la posicion.
- Un `KeyPress W` sintetico fue recibido por el receptor confirmado.
- W produjo desplazamiento en `+Y` y `KeyRelease W` detuvo la entrada.
- Escape detuvo timer, retiro ambos filtros y el shortcut, y limpio singleton.
- El conteo de objetos del documento permanecio sin cambios.

Esta validacion no simulo el arbitraje real de shortcuts del teclado fisico.
La aceptacion de v013 requiere la prueba manual descrita arriba.

## Comprobacion no interactiva v013

- La camara inicio exactamente en `(0, 0, 0)`.
- `ShortcutOverride S` fue aceptado y filtrado.
- El `KeyPress S` posterior se registro y `KeyRelease S` limpio la tecla.
- Escape retiro timer, filtros, shortcut y singleton.
- El conteo de objetos del documento no cambio.

Esta comprobacion valida la logica del controlador, pero deliberadamente no se
presenta como sustituto de la prueba con teclado fisico y los shortcuts reales
de FreeCAD.
