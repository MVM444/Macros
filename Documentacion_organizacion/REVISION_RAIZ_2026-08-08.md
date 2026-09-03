# Revision de la raiz de Macros - 2026-08-08

## Motivo

Se reviso el repositorio `MVM444/Macros` porque la raiz volvio a acumular archivos despues de la limpieza realizada en junio de 2026.

## Hallazgo principal

Al comparar el estado posterior a la limpieza de junio con `main` del 2026-08-08 se identificaron decenas de archivos nuevos directamente en la raiz: macros especializadas, capturas, modelos FreeCAD, respaldos, scripts DXF, herramientas editoriales y documentacion de proyectos.

## Criterio aprobado

La raiz no debe utilizarse como carpeta de trabajo temporal.

Despues de la decision del 2026-08-12, deben mantenerse en raiz solamente los
controladores globales necesarios, incluyendo expresamente:

- `RegistrarLoadersGlobales.FCMacro`
- `MacrosPersonalizadas.FCMacro`
- `VentanadeMacros.FCMacro`

Los cuatro loaders y sus iconos viven en `Loaders/`. `Alias.FCMacro` vive en
`Scripts Varios/Spreadsheet`; los accesos de directorio reemplazados se
conservan bajo `Respaldos/`. `VentanadeMacros.FCMacro` es un punto de entrada
global confirmado y no debe volver a clasificarse como interfaz legacy.

## Puriscal

Puriscal fue utilizado como caso real de desarrollo y prueba. Sus archivos no deben tratarse todos como basura.

Se distinguieron dos grupos principales:

1. Herramientas potencialmente reutilizables para FacilArquitectura/BIM.
2. Archivos especificos del caso Puriscal: macros con indices/objetos concretos, modelos, capturas y resultados.

La limpieza debe conservar esta diferencia.

## Ollama y AutoCorreccion (2026-08-12)

El asistente Ollama existente se recupero del historial Git desde la antigua
ruta de raiz y se reubico, con su SVG exclusivo, en la carpeta `Programacion`
con tilde, sin cambios de interfaz o comportamiento.
`AutoCorreccion_Local.FCMacro`, tras confirmar que solo genera diagnostico
JSON/conteo y no usa Ollama, se archivo intacta en
`Respaldos/Diagnostico_legacy`.

## Seguridad

- No eliminar macros reutilizables sin revision.
- Revisar dependencias antes de cambiar rutas.
- Los resultados generados y capturas pueden excluirse de la raiz y del flujo normal de desarrollo.
- Mantener trazabilidad de cualquier movimiento relevante.

## Flujo GPT-Codex

Codex debe leer `AGENTS.md` y `Documentacion_organizacion/TAREA_ACTUAL.md` antes de continuar esta reorganizacion.

## Decision posterior: diagnostico general (2026-08-12)

Las herramientas generales de reportes, seleccion, propiedades, auditoria Qt,
coordenadas, directorios y captura del arbol se consolidan en `Programación`.
La barra es global e independiente de ElectricCR. El capturador de arbol fue
retirado de `Macros-de-Freecad/Configuracion del proyecto` por decision expresa
del usuario y sustituido por `Programación/CapturarArbolYPrompt.FCMacro`.
Las demas versiones antiguas no se movieron ni eliminaron y quedan pendientes
de validacion.
