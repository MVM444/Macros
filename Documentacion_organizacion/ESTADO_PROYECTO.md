# Estado del proyecto de organizacion de Macros

Fecha: 2026-08-08

## Estado

Segunda pasada conservadora aplicada.

## Confirmado

- La raiz de `Macros` es un punto de entrada de FreeCAD, no una carpeta general de trabajo.
- `AbrirDirectorioElectricCR.FCMacro` permanece en la raiz por decision expresa del usuario.
- Los loaders globales permanecen en raiz.
- Se retiraron capturas generadas de Puriscal y respaldos FCBak detectados en raiz.
- Se retiraron cuatro bibliotecas DXF duplicadas despues de comprobar que existen copias identicas en `Scripts Varios/DXF`.
- Se agregaron reglas de `.gitignore` para evitar que `Puriscal_*.png` y `*.FCBak` vuelvan a incorporarse accidentalmente.

## Segunda etapa aplicada

Se movieron fuera de la raiz:

- macros reutilizables de FacilArquitectura/BIM a `Scripts Varios/FacilArquitectura_BIM`;
- macros y documentacion especifica de Puriscal a `Scripts Varios/FacilArquitectura_BIM/Puriscal`;
- `Puriscal Depurado.FCStd` a `Respaldos/Proyectos_prueba/Puriscal`;
- `Silla_Madera.FCStd` y `Silla_Madera.step` a `Respaldos/Proyectos_prueba/Silla_Madera`;
- scripts editoriales a `Scripts Varios/Revision_editorial`;
- importadores y ayudantes CAD/DXF a `Scripts Varios/Importaciones_especificas` y `Scripts Varios/DXF`.

Ver `RESULTADO_SEGUNDA_ETAPA_2026-08-08.md`.

## Pendiente

Revisar si conviene convertir algunas macros movidas en comandos nativos de `FacilArquitecturaWB` o integrarlas formalmente en `Macros-de-Freecad`. No eliminar en bloque.

## Instruccion para Codex

No iniciar la segunda etapa por borrado masivo. Leer `AGENTS.md`, `TAREA_ACTUAL.md`, `REVISION_RAIZ_2026-08-08.md` y `RESULTADO_LIMPIEZA_2026-08-08.md`, reconstruir dependencias y proponer movimientos conservadores.
