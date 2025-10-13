Notas del proyecto (ElectricCR)

Historial breve
- Se partió de una macro suelta y se convirtió en un workbench tipo paquete Python dentro de la carpeta `Macros`.
- Se añadió un macro cargador `ElectricCRLoader.FCMacro` para registrar el workbench sin moverlo a `Mod/`.
- Se agregaron iconos y lógica de búsqueda por nombre base (`.svg`/`.png`).
- Integración: inicialmente con Arch, luego reemplazada por Draft. Se filtran comandos con `Gui.listCommands()` para evitar “Unknown command”.

Estructura actual
- `ElectricCR/InitGui.py`: registra el workbench, menús y toolbars (Draft + Electric).
- `ElectricCR/commands/insert_outlet.py`: comando “Insertar Tomacorriente”.
- `ElectricCR/icons/`: iconos del WB y comandos.
- `ElectricCRLoader.FCMacro`: cargador del workbench desde `Macros`.

Puntos técnicos
- El loader añade la ruta del paquete al `sys.path` y hace `import ElectricCR.InitGui` (esto registra el WB en FreeCAD).
- La lista de comandos Draft se filtra contra `Gui.listCommands()` para mostrar solo los existentes.
- Iconos: función `icon_path()` busca `Rayo.svg/png` y `tomacorriente.svg/png` dentro de `icons/`.

VS Code y análisis estático
- `.vscode/settings.json` asocia `*.FCMacro` a Python y suaviza alertas de imports faltantes (FreeCAD no está en el entorno de VS Code por defecto).

Pruebas rápidas
1) Ejecutar `ElectricCRLoader.FCMacro`.
2) Cambiar al WB “Eléctrico CR”.
3) Usar “Insertar Tomacorriente” y comprobar iconos/menús.

Pendientes / ideas
- Añadir más comandos (luminarias, interruptores, canalizaciones).
- Preferencias del WB para mostrar/ocultar toolbars Draft.
- Scripts de utilidades (selección, alineación en muros, cotas específicas).

