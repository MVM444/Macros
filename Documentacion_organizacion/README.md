# Organizacion del directorio Macros

Fecha de referencia inicial: 2026-06-22.
Actualizacion: 2026-08-08.

Este directorio se organiza para que la raiz de `Macros` funcione como punto de entrada de FreeCAD, no como bodega general.

## Regla principal

En la raiz de `Macros` deben quedar solo:

- macros generales que ayudan a administrar otras macros;
- iconos SVG usados directamente por esas macros de raiz;
- archivos minimos de configuracion/documentacion propios de la raiz;

Los loaders y sus iconos se agrupan en `Loaders/`. Los accesos de directorio
reemplazados se conservan bajo `Respaldos/Programacion_reemplazadas/`.

Las macros especializadas, pruebas, ejemplos, importaciones puntuales, modelos de prueba, capturas y utilidades deben vivir en subdirectorios.

## Archivos que deben quedarse en la raiz

- `RegistrarLoadersGlobales.FCMacro`: registra los loaders activos en la barra global de macros.
- `MacrosPersonalizadas.FCMacro`: crea menus de macros personalizadas y recientes.
- `VentanadeMacros.FCMacro`: buscador global de macros; su permanencia en raiz fue confirmada nuevamente por Marco el 2026-08-12.

Los SVG de esas macros pueden quedar junto a los `.FCMacro` porque FreeCAD suele resolver mejor los iconos de barra cuando estan al lado de la macro.

`AGENTS.md` permanece en la raiz como archivo de instrucciones para Codex y otros agentes.

## Directorios importantes

- `Macros-de-Freecad`: proyecto principal con workbenches y macros asociadas.
- `Scripts Varios`: macros y scripts utiles, pero no centrales para el arranque de FreeCAD.
- `Respaldos`: archivos archivados, copias antiguas, recursos duplicados y movimientos conservadores.
- `Reportes`: salidas generadas por herramientas de diagnostico.
- `Documentacion_organizacion`: documentacion de la estructura y de las limpiezas realizadas.
- `Loaders`: cargadores globales de ElectricCR, FacilArquitecturaWB, MEPWorkbenchCR y GameEngineExportWB, con sus SVG.
- `Scripts Varios/Spreadsheet`: herramientas funcionales de Spreadsheet, incluyendo `Alias.FCMacro`.
- `Respaldos/Programacion_reemplazadas`: accesos directos sustituidos por la herramienta general de directorios.
- `Programación`: herramientas generales read-only de diagnostico y desarrollo, con barra global propia y subcarpetas para reportes/auxiliares.

## Barra global Programacion

Desde 2026-08-12, `Mod/DevPathsBootstrap/InitGui.py` carga una barra global
`Programacion`, independiente de ElectricCR y de los demas Workbenches. Su
manifiesto registra solo las siete macros activas ubicadas directamente en
`Programación`; no recorre subcarpetas ni convierte duplicados historicos en
botones.

### Asistente Ollama

La macro historica `Ollama_Asistente_Local.FCMacro` y su icono viven en la
carpeta real `Programacion` con tilde. Aparecen mediante `Macros Personalizadas`
y como boton propio de la barra global `Programacion`.

## Workbenches separados

Los workbenches deben mantenerse conceptualmente separados. La raiz solo proporciona sus loaders globales.

## Nota sobre Puriscal

Los archivos de Puriscal surgieron durante desarrollo y pruebas reales. No deben clasificarse todos de la misma forma.

- Las herramientas reutilizables deben revisarse para su ubicacion definitiva.
- Las macros especificas, modelos, capturas y resultados del caso Puriscal no deben permanecer en la raiz.

Ver `TAREA_ACTUAL.md` y `REVISION_RAIZ_2026-08-08.md`.

## Nota sobre caches

Los directorios `__pycache__` son generados automaticamente por Python/FreeCAD. Si se borran o archivan, normalmente se regeneran. No deben usarse como fuente de verdad para recuperar codigo.

## Segunda etapa 2026-08-08

La segunda etapa movio macros BIM/Puriscal, importadores, scripts editoriales y modelos de prueba fuera de la raiz. Ver `RESULTADO_SEGUNDA_ETAPA_2026-08-08.md`.
