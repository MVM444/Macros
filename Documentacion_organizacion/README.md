# Organizacion del directorio Macros

Fecha de referencia inicial: 2026-06-22.
Actualizacion: 2026-08-08.

Este directorio se organiza para que la raiz de `Macros` funcione como punto de entrada de FreeCAD, no como bodega general.

## Regla principal

En la raiz de `Macros` deben quedar solo:

- loaders de workbench;
- macros generales que ayudan a administrar otras macros;
- iconos SVG usados directamente por esas macros de raiz;
- archivos minimos de configuracion/documentacion propios de la raiz;
- `AbrirDirectorioElectricCR.FCMacro`, por decision expresa del usuario del 2026-08-08.

Las macros especializadas, pruebas, ejemplos, importaciones puntuales, modelos de prueba, capturas y utilidades deben vivir en subdirectorios.

## Archivos que deben quedarse en la raiz

- `ElectricCRLoader.FCMacro`: carga y recarga el workbench ElectricCR.
- `FacilArquitecturaLoader.FCMacro`: carga y recarga Facil Arquitectura.
- `MEPWorkbenchCRLoader.FCMacro`: carga y recarga el workbench MEPWorkbenchCR.
- `GameEngineExportLoader.FCMacro`: carga y recarga el workbench GameEngineExportWB.
- `RegistrarLoadersGlobales.FCMacro`: registra los loaders activos en la barra global de macros.
- `Alias.FCMacro`: herramienta general para asignar alias en hojas Spreadsheet.
- `AbrirDirectorioDocumento.FCMacro`: abre la carpeta donde esta guardado el documento activo.
- `AbrirDirectorioElectricCR.FCMacro`: acceso directo al directorio ElectricCR; se mantiene en raiz por decision del usuario.
- `VentanadeMacros.FCMacro`: ventana general para buscar y ejecutar macros.
- `MacrosPersonalizadas.FCMacro`: crea menus de macros personalizadas y recientes.

Los SVG de esas macros pueden quedar junto a los `.FCMacro` porque FreeCAD suele resolver mejor los iconos de barra cuando estan al lado de la macro.

`AGENTS.md` permanece en la raiz como archivo de instrucciones para Codex y otros agentes.

## Directorios importantes

- `Macros-de-Freecad`: proyecto principal con workbenches y macros asociadas.
- `Scripts Varios`: macros y scripts utiles, pero no centrales para el arranque de FreeCAD.
- `Respaldos`: archivos archivados, copias antiguas, recursos duplicados y movimientos conservadores.
- `Reportes`: salidas generadas por herramientas de diagnostico.
- `Documentacion_organizacion`: documentacion de la estructura y de las limpiezas realizadas.

## Workbenches separados

Los workbenches deben mantenerse conceptualmente separados. La raiz solo proporciona sus loaders globales.

## Nota sobre Puriscal

Los archivos de Puriscal surgieron durante desarrollo y pruebas reales. No deben clasificarse todos de la misma forma.

- Las herramientas reutilizables deben revisarse para su ubicacion definitiva.
- Las macros especificas, modelos, capturas y resultados del caso Puriscal no deben permanecer en la raiz.

Ver `TAREA_ACTUAL.md` y `REVISION_RAIZ_2026-08-08.md`.

## Nota sobre caches

Los directorios `__pycache__` son generados automaticamente por Python/FreeCAD. Si se borran o archivan, normalmente se regeneran. No deben usarse como fuente de verdad para recuperar codigo.
