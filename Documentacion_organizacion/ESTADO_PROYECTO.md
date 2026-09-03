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

## Complemento externo FreeCAD-HVAC (reverificado 2026-09-02)

Estado: instalado y validado en FreeCAD 1.1.3.

- Instalacion Git independiente en
  `C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC`.
- Repositorio oficial: `https://github.com/Francisco-Rosa/FreeCAD-HVAC.git`.
- Rama `main`, commit `ae8e28464ef4616b7570d22b0464960113086ce5`.
- Arbol fuente limpio y sin modificaciones locales.
- Workbench, menu, barra y comandos cargados correctamente.
- Smoke test aprobado: red, ruta Draft de 2000 mm, un segmento y dos terminales.
- Documento temporal cerrado sin guardar.
- Se mantiene totalmente separado de los Workbenches y macros propios.
- La reverificacion del 2026-09-02 confirmo que el clon sigue limpio y que el
  `main` remoto conserva el mismo commit; no fue necesario reclonar ni actualizar.
- Nuevo smoke GUI aprobado: 16 comandos, menu/barra de 13 acciones, ruta Draft
  de 2000 mm, un segmento circular y dos terminales.
- No hubo errores de HVAC. Persisten avisos ajenos por el enlace roto de
  FacilArquitecturaWB y, en la configuracion aislada de prueba, por MacroPath.

Detalle y procedimiento de actualizacion: `RESULTADO_CODEX.md`.
