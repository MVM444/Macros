# Resultado de segunda etapa de limpieza de raiz - 2026-08-08

## Objetivo

Reducir la raiz de `Macros` para que muestre principalmente loaders, macros globales y archivos de control, sin borrar macros reutilizables.

## Criterio aplicado

- Se mantuvieron en raiz los loaders y macros globales definidos en `README.md`.
- Se mantuvo `AbrirDirectorioElectricCR.FCMacro` en raiz por decision expresa del usuario.
- No se eliminaron macros.
- Las macros relacionadas entre si se movieron juntas para conservar dependencias por directorio.
- Los modelos de prueba se archivaron en `Respaldos/Proyectos_prueba`.

## Movimientos principales

### Facil Arquitectura / BIM reutilizable

Movido a `Scripts Varios/FacilArquitectura_BIM/`:

- `AnalizarAreasDesdeMuroBIM.FCMacro`
- `CrearAnalisisAreasRectangulares.FCMacro`
- `CrearPoligonosRecintosDesdeMurosBIM.FCMacro`
- `CrearPuertasBIMDesdeSketch.FCMacro`
- `CrearVentanasBIMDesdeSketch.FCMacro`
- `InsertarPuertasBIMDesdeRecintos.FCMacro`
- `InsertarVentanasBIMDesdeRecintos.FCMacro`
- `RecopilarRotulosRecintos.FCMacro`
- `ImportarReferenciaCADFacilArquitectura.FCMacro`
- `ImportarReferenciaCADFacilArquitectura.svg`
- documentacion BIM asociada.

### Puriscal

Movido a `Scripts Varios/FacilArquitectura_BIM/Puriscal/`:

- `AgregarPuertasFrentePuriscal.FCMacro`
- `OrganizarPuriscalDepurado.FCMacro`
- `HANDOFF_CODEX_PURISCAL.md`
- `RESUMEN_CONSOLIDADO_PURISCAL_FACIL_ARQUITECTURA.md`

Movido a `Respaldos/Proyectos_prueba/Puriscal/`:

- `Puriscal Depurado.FCStd`

### Importaciones y CAD/DXF

Movido a ubicaciones existentes:

- `ImportarIFCControlado.FCMacro` -> `Scripts Varios/Importaciones_especificas/`
- `dxf_lines_to_compound_fcstd.py` -> `Scripts Varios/DXF/`
- `import_dxf_save_fcstd.py` -> `Scripts Varios/DXF/`
- `pdf_vector_to_dxf.py` -> `Scripts Varios/DXF/`

### Revision editorial

Movido a `Scripts Varios/Revision_editorial/`:

- `apply_editorial_revision.ps1`
- `apply_editorial_revision_word_only.ps1`
- `fix_cap3_numbering.ps1`
- `auditoria_editorial.md`
- `cambios_editoriales.md`
- `pendientes_revision.md`

### Pruebas Silla Madera

Movido a `Respaldos/Proyectos_prueba/Silla_Madera/`:

- `Silla_Madera.FCStd`
- `Silla_Madera.step`

## Ajustes de compatibilidad

Se ajustaron rutas en lanzadores movidos que antes asumian estar en la raiz:

- `CrearPoligonosRecintosDesdeMurosBIM.FCMacro`
- `CrearPuertasBIMDesdeSketch.FCMacro`
- `CrearVentanasBIMDesdeSketch.FCMacro`
- `ImportarReferenciaCADFacilArquitectura.FCMacro`
- `RecopilarRotulosRecintos.FCMacro`
- `InsertarPuertasBIMDesdeRecintos.FCMacro`
- `Puriscal/AgregarPuertasFrentePuriscal.FCMacro`

## Estado esperado de raiz

La raiz debe quedar con loaders, macros globales, iconos directos de esas macros y archivos de control. Las macros especializadas deben aparecer en submenus como `Scripts Varios` en lugar de la lista principal de `MacrosPersonalizadas`.
