# Estado del proyecto de organizacion de Macros

Fecha: 2026-08-08

## Estado

Primera pasada segura completada.

## Confirmado

- La raiz de `Macros` es un punto de entrada de FreeCAD, no una carpeta general de trabajo.
- `AbrirDirectorioElectricCR.FCMacro` permanece en la raiz por decision expresa del usuario.
- Los loaders globales permanecen en raiz.
- Se retiraron capturas generadas de Puriscal y respaldos FCBak detectados en raiz.
- Se retiraron cuatro bibliotecas DXF duplicadas despues de comprobar que existen copias identicas en `Scripts Varios/DXF`.
- Se agregaron reglas de `.gitignore` para evitar que `Puriscal_*.png` y `*.FCBak` vuelvan a incorporarse accidentalmente.

## Pendiente - segunda etapa

Revisar y reubicar, solo despues de analizar dependencias:

- macros reutilizables de FacilArquitectura/BIM;
- macros especificas de Puriscal;
- modelos y recursos de `Silla_Madera`;
- modelo `Puriscal Depurado.FCStd`;
- scripts editoriales;
- importadores IFC/CAD;
- otras utilidades que todavia permanezcan directamente en la raiz.

## Instruccion para Codex

No iniciar la segunda etapa por borrado masivo. Leer `AGENTS.md`, `TAREA_ACTUAL.md`, `REVISION_RAIZ_2026-08-08.md` y `RESULTADO_LIMPIEZA_2026-08-08.md`, reconstruir dependencias y proponer movimientos conservadores.