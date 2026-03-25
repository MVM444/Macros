ElectricCR — Workbench para FreeCAD (carpeta de macros)

Descripción
- Workbench ligero para instalaciones eléctricas dentro de la carpeta `Macros` de FreeCAD.
- Incluye un comando inicial: “Insertar Tomacorriente” (cilindro simple) y una integración con comandos de Draft (filtrados según disponibilidad).

Estructura
- `ElectricCR/` → paquete del workbench
  - `Init.py` / `InitGui.py` → registro del WB y barras/menús
  - `commands/` → comandos Python del WB
  - `icons/` → iconos (`.svg`/`.png`)
- `ElectricCRLoader.FCMacro` → macro cargador para registrar el WB desde `Macros`

Instalación y carga
1) Copia `ElectricCR/` y `ElectricCRLoader.FCMacro` a tu carpeta de macros de FreeCAD.
2) En FreeCAD: `Macro` → `Macros...` → selecciona `ElectricCRLoader.FCMacro` → `Ejecutar`.
3) Cambia al workbench “Eléctrico CR” desde el selector de WB.

Autocarga (opcional)
- Marca el loader para ejecutarse al inicio (Preferencias → Macros), o usa una carpeta `Autoload` si tu versión lo soporta.

Uso
- Barra/menú “Electric” → “Insertar Tomacorriente”: crea un cilindro “Tomacorriente” en el documento.
- Barra/menú “Herramientas Draft”: se muestran los comandos de Draft que existan en tu instalación (se filtran automáticamente).

Íconos
- Coloca `Rayo.svg` (icono del WB) y `tomacorriente.svg` (comando) en `ElectricCR/icons/`. La carga busca `.svg` o `.png` por nombre base.

Desarrollo
- Añade nuevos comandos en `ElectricCR/commands/` y regístralos con `Gui.addCommand` (ver `insert_outlet.py`).
- Si agregas comandos Draft/otros, usa `Gui.listCommands()` para filtrar los disponibles y evitar “Unknown command”.
- Recomendado para VS Code: ver `.vscode/settings.json` (asociar `.FCMacro` como Python y silenciar imports de FreeCAD en análisis).

Trabajar en dos equipos
- Versiona esta carpeta con Git y sube a GitHub (o sincroniza con OneDrive). En la otra máquina, clona/descarga y coloca el contenido en `Macros`.
- VS Code compartirá configuración si este repo incluye la carpeta `.vscode/` (ya incluida).

Revisar la versi�n actual
- Ejecuta scripts\show_version.ps1 desde la ra�z del repositorio para ver la rama activa, el estado del �rbol y el �ltimo commit; as� sabes sin abrir paneles si est�s en la compilaci�n m�s reciente.
