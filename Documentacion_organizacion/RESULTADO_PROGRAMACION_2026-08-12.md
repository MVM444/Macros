# Resultado - barra global Programacion

Fecha: 2026-08-12 08:17 America/Costa_Rica
FreeCAD objetivo: 1.1.3 en Windows
Estado: IMPLEMENTADA; VALIDACION GUI/FUNCIONAL DE MARCO PENDIENTE

## Arquitectura

`Mod/DevPathsBootstrap/InitGui.py`, que FreeCAD ya carga globalmente, ejecuta
`Programación/programacion_toolbar.py`. El controlador usa siete CommandName
estables, un manifiesto explicito, una sola QToolBar y referencias persistentes
en la ventana principal. La ejecucion de cada macro usa un namespace con
`__file__` y `__name__` para soportar dialogos y clases. Las subcarpetas se
ignoran. `Mod/DevPathsBootstrap/Init.py` tambien fue corregido para cuando
FreeCAD no define `__file__`.

## Matriz definitiva

| Herramienta/version | Clasificacion | Decision |
| --- | --- | --- |
| `CopyReportLast1Min.FCMacro` | Conservar/modernizar | Boton `Copiar ultimo minuto`; Report View robusta y respaldo de log. |
| `CopyLastMinuteLog.FCMacro` | Consolidar | Solo aporto el respaldo por archivo; queda intacta y sin boton. |
| `ConsoleClipboard.FCMacro`, `leer_log_freecad.py` | Reemplazada | Duplicado externo con `pyperclip`; sin boton. Proponer `Antiguas` tras validar. |
| `ExportarArbolModelo.FCMacro` | Consolidar | Aporto rutas y contexto; queda intacta y sin boton. |
| `Capturar_Arbol_Grupos_Documento.FCMacro` | Mover/consolidar | Retirada de ElectricCR por autorizacion; sustituida por `CapturarArbolYPrompt.FCMacro`. |
| `Copiar_Nombres_Seleccion.FCMacro` y macros antiguas de conteo | Conservar/modernizar | Boton de resumen con conteo, rutas y Links. |
| `CopyObjectProperties.FCMacro` | Conservar/modernizar | Boton JSON seguro y limitado. |
| `UI_Audit_FreeCAD.FCMacro` | Consolidar | Adaptada como auditoria read-only en Programacion; original queda para revision. |
| `Capturar_Coordenadas_Click.FCMacro` | Consolidar | Modernizada con callback unico y cancelacion; original queda para revision. |
| `AbrirDirectorioDocumento.FCMacro`, `AbrirDirectorioElectricCR.FCMacro` | Reemplazada | Validadas las rutas de la herramienta general, se movieron a `Respaldos/Programacion_reemplazadas`. |
| Otras macros ElectricCR que modifican objetos | Especializada/excluida | No pertenecen a la barra Programacion. |

## Pruebas

- Compilacion Python de todos los `.py` y `.FCMacro` en `Programación` y de los dos bootstrap: aprobada.
- Casos del ultimo minuto, incluyendo medianoche y lineas sin hora: aprobados.
- Manifiesto de siete comandos, archivos directos, iconos propios y XML SVG: aprobado.
- FreeCADCmd 1.1.3: inicio, documento temporal y cierre sin guardar aprobados.
- El fallo preexistente `__file__` de `DevPathsBootstrap/Init.py` fue reproducido y corregido; ya no reaparecio.
- La instalacion externa de FacilArquitecturaWB en AppData reporta una ruta inexistente; es ajena a esta tarea.
- La prueba GUI automatizada no se pudo completar: el ejecutable abrio otra instancia pero no ejecuto el script. Esa instancia fue cerrada y la sesion previa de Marco quedo intacta.

## Pendiente de Marco

- Reiniciar FreeCAD y confirmar autocarga, una sola barra y persistencia al cambiar de Workbench.
- Ejecutar los siete botones en un documento temporal y validar portapapeles/dialogos.
- Validar Report View y fallback real de `FreeCAD.log`.
- Validar arbol sin seleccion, con uno/varios grupos, anidados y Links; revisar TXT/MD/JSON/prompt.
- Validar captura 3D, Escape y retiro del callback.
- Decidir movimientos a `Programación/Antiguas`; no se movieron otras versiones.

No se modifico ni guardo ningun `.FCStd`. No se hizo commit ni push. La tarea
de Areas permanece implementada y pendiente de validacion de Marco en
`Macros-de-Freecad/TAREA_ACTUAL.md`.

## Limpieza posterior de raiz

Los loaders e iconos se movieron por Git a `Loaders/`; sus rutas internas y el
registrador se adaptaron al nuevo directorio. En FreeCAD 1.1.3 los cuatro
loaders activaron correctamente sus Workbenches y quedaron registrados como
`Loaders/*.FCMacro`, con una sola barra `Macros`. `UI_Audit_FreeCAD.FCMacro` se
movio a `Programación`; `Alias.FCMacro` a `Scripts Varios/Spreadsheet`; la
interfaz legacy y los accesos reemplazados a `Respaldos`.
