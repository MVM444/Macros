# Resultado de limpieza de raiz - 2026-08-08

## Primera pasada segura aplicada

Se realizo una primera limpieza conservadora de la raiz del repositorio `MVM444/Macros`.

### Se mantiene expresamente en raiz

- `AbrirDirectorioElectricCR.FCMacro`

Tambien se mantienen los loaders y macros globales definidos en `README.md`.

### Archivos retirados de la raiz

- Capturas generadas `Puriscal_*.png` revisadas en esta pasada.
- Dos respaldos `Silla_Madera.*.FCBak`.
- La captura `Silla_Madera.png`.
- Copias duplicadas de `dxfColorMap.py`, `dxfImportObjects.py`, `dxfLibrary.py` y `dxfReader.py`.

Las cuatro bibliotecas DXF fueron comparadas con sus copias en `Scripts Varios/DXF` y resultaron identicas antes de retirar las copias de la raiz.

### Prevencion

`.gitignore` ahora excluye:

- `*.FCBak`
- `Puriscal_*.png`

para reducir la posibilidad de que estos resultados generados vuelvan a quedar versionados en la raiz.

## Archivos no movidos en esta pasada

No se movieron ni eliminaron automaticamente:

- macros potencialmente reutilizables creadas durante el trabajo de Puriscal;
- macros especificas de Puriscal que pueden depender de archivos vecinos;
- `Puriscal Depurado.FCStd`;
- `Silla_Madera.FCStd` y `Silla_Madera.step`;
- scripts editoriales, importadores y otras herramientas que requieren revisar dependencias y destino.

Estos elementos constituyen la segunda etapa de la limpieza y deben revisarse con Codex siguiendo `AGENTS.md` y `TAREA_ACTUAL.md`.

## Criterio

La prioridad de esta primera pasada fue reducir ruido evidente sin arriesgar codigo ni dependencias funcionales.