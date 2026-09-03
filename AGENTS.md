# Reglas del repositorio Macros

Fecha: 2026-08-08

## Alcance

Este repositorio representa el directorio principal de macros de FreeCAD.
No confundirlo con el subproyecto `Macros-de-Freecad/ElectricCR`.

## Regla principal de la raiz

La raiz de `Macros` debe funcionar como punto de entrada de FreeCAD y no como bodega general.

En la raiz pueden permanecer:

- macros globales para administrar otras macros;
- iconos usados directamente por esas macros de raiz;
- archivos minimos de control del repositorio, incluyendo este `AGENTS.md`;

Los loaders de Workbench y sus iconos viven en `Loaders/`. Los accesos de
directorios reemplazados viven en `Respaldos/Programacion_reemplazadas/`.

Las macros especializadas, pruebas, ejemplos, modelos de prueba, capturas, respaldos, importaciones puntuales y herramientas auxiliares deben vivir en subdirectorios.

## Regla de limpieza

Antes de mover o eliminar un archivo:

1. Revisar si es codigo reutilizable, herramienta especifica, resultado generado, respaldo o documentacion.
2. Revisar dependencias y rutas relativas.
3. No eliminar una macro reutilizable solo por haber sido creada durante una prueba.
4. No concluir que un archivo es obsoleto solamente por su nombre o antiguedad.
5. Preferir movimientos conservadores y documentados.
6. Mantener `RegistrarLoadersGlobales.FCMacro`, `MacrosPersonalizadas.FCMacro` y `VentanadeMacros.FCMacro` en la raiz.
7. `VentanadeMacros.FCMacro` es un punto de entrada global confirmado; no clasificarla nuevamente como interfaz legacy ni moverla a `Respaldos`.

## Puriscal

Los archivos creados durante el trabajo de Puriscal no son una sola categoria.

Separar al menos entre:

- herramientas potencialmente reutilizables para FacilArquitectura/BIM;
- macros especificas del modelo de Puriscal;
- modelos y respaldos;
- capturas y resultados generados;
- documentacion de desarrollo.

No borrar automaticamente las herramientas reutilizables.

## Documentacion obligatoria

Antes de continuar una limpieza de la raiz, leer:

- `Documentacion_organizacion/README.md`
- `Documentacion_organizacion/MOVIMIENTOS_2026-06-22.md`
- `Documentacion_organizacion/TAREA_ACTUAL.md`
- `Documentacion_organizacion/REVISION_RAIZ_2026-08-08.md`

Si una reorganizacion cambia la regla de la raiz o el destino de una familia de archivos, actualizar la documentacion correspondiente.
