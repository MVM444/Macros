# Revision de la raiz de Macros - 2026-08-08

## Motivo

Se reviso el repositorio `MVM444/Macros` porque la raiz volvio a acumular archivos despues de la limpieza realizada en junio de 2026.

## Hallazgo principal

Al comparar el estado posterior a la limpieza de junio con `main` del 2026-08-08 se identificaron decenas de archivos nuevos directamente en la raiz: macros especializadas, capturas, modelos FreeCAD, respaldos, scripts DXF, herramientas editoriales y documentacion de proyectos.

## Criterio aprobado

La raiz no debe utilizarse como carpeta de trabajo temporal.

Deben mantenerse en raiz los loaders y herramientas globales, incluyendo expresamente:

- `ElectricCRLoader.FCMacro`
- `FacilArquitecturaLoader.FCMacro`
- `GameEngineExportLoader.FCMacro`
- `MEPWorkbenchCRLoader.FCMacro`
- `RegistrarLoadersGlobales.FCMacro`
- `Alias.FCMacro`
- `AbrirDirectorioDocumento.FCMacro`
- `AbrirDirectorioElectricCR.FCMacro`
- `VentanadeMacros.FCMacro`
- `MacrosPersonalizadas.FCMacro`

Sus iconos directos pueden permanecer junto a ellos.

## Puriscal

Puriscal fue utilizado como caso real de desarrollo y prueba. Sus archivos no deben tratarse todos como basura.

Se distinguieron dos grupos principales:

1. Herramientas potencialmente reutilizables para FacilArquitectura/BIM.
2. Archivos especificos del caso Puriscal: macros con indices/objetos concretos, modelos, capturas y resultados.

La limpieza debe conservar esta diferencia.

## Seguridad

- No eliminar macros reutilizables sin revision.
- Revisar dependencias antes de cambiar rutas.
- Los resultados generados y capturas pueden excluirse de la raiz y del flujo normal de desarrollo.
- Mantener trazabilidad de cualquier movimiento relevante.

## Flujo GPT-Codex

Codex debe leer `AGENTS.md` y `Documentacion_organizacion/TAREA_ACTUAL.md` antes de continuar esta reorganizacion.