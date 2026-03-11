# Game Engine Export WB

## Resumen / Summary

Game Engine Export WB prepara escenas de FreeCAD para Castle Game Engine con escala en metros, rotacion global en X de -90 grados y soporte para Viewpoint inicial, luces y persistencia de configuracion.

## Estado

Version inicial 0.1.0 (2025-10-13 13:54 UTC). Solo contiene la estructura base y paneles de interfaz sin logica de exportacion.

## Instalacion rapida

1. Copiar la carpeta `Mod/GameEngineExportWB` dentro del directorio de macros o mods de FreeCAD.
2. Reiniciar FreeCAD.
3. Seleccionar el workbench **Game Engine Export WB**.

## Abrir el proyecto en Visual Studio Code

1. Abre Visual Studio Code y elige **File > Open Folder**.
2. Selecciona la carpeta raiz que contiene `Mod/GameEngineExportWB`.
3. Cuando el editor termine de indexar, podras navegar por los subdirectorios `core`, `ui`, `commands` y `resources`.
4. Si deseas conservar notas de las sesiones, utiliza el archivo `notes/GameEngineExportWB_chat.md` descrito mas adelante.

## Aplicar cambios en Visual Studio Code

1. Abre la misma carpeta del repositorio en Visual Studio Code.
2. En la vista **Source Control** revisa los cambios pendientes y usa **Pull** para traer la ultima version.
3. Copia la carpeta `Mod/GameEngineExportWB` y el archivo `GameEngineExportLoader.FCMacro` a tu carpeta `FreeCAD/Mod` o `FreeCAD/Macro` segun corresponda.
4. Ejecuta la macro `GameEngineExportLoader.FCMacro` desde FreeCAD para recargar el workbench y ver los cambios sin reiniciar.
5. Si modificas archivos, confirma en el panel de Source Control que los cambios se hayan guardado y versionado antes de probar en FreeCAD.

## Cargar el workbench en FreeCAD

1. Copia `Mod/GameEngineExportWB` en tu carpeta de usuario `FreeCAD/Mod` o `FreeCAD/Macro` segun la instalacion.
2. Inicia o reinicia FreeCAD para que detecte el nuevo workbench.
3. Desde la barra superior elige el workbench **Game Engine Export WB**.
4. Abre el comando **GameEngineExport Open** para mostrar el TaskPanel.
5. Veras mensajes `[GAMEEXPORT]` en la consola de reportes confirmando la carga.

## Uso rapido

Abre el comando **GameEngineExport Open** para mostrar el panel principal. Desde ahi podras elegir la raiz de la escena, listas de objetos, marcador GameStart, luces y carpeta de salida. Aun no existe funcionalidad final de exportacion.

## Archivos incluidos

- `Init.py`, `InitGui.py`: arranque del workbench y registro de comandos.
- `core/`: modulos para exportar, manejar luces, persistencia y utilidades.
- `ui/`: paneles TaskPanel de escena, configuracion y texto informativo.
- `commands/`: comando principal GameEngineExport_Open.
- `resources/icons/gameexport.svg`: icono del workbench.
- `notes/GameEngineExportWB_chat.md`: registro de conversaciones y decisiones relevantes.
- `../GameEngineExportLoader.FCMacro`: macro para recargar el workbench en FreeCAD sin reiniciar.

## Ubicacion dentro del repositorio / Location inside repository

- El codigo fuente del workbench vive en `Mod/GameEngineExportWB` dentro del repositorio.
- El icono y otros recursos estan en `Mod/GameEngineExportWB/resources`.
- La macro de recarga rapida esta en la raiz del repositorio como `GameEngineExportLoader.FCMacro`.
- Si abres el repositorio desde Visual Studio Code veras la macro en el nivel superior junto a la carpeta `Mod/`.
- Al clonar o descargar desde GitHub, verifica que la carpeta `Mod/GameEngineExportWB` exista antes de copiarla a tu directorio `FreeCAD/Mod`.
- En el disco local puedes usar **File > Open Folder** en Visual Studio Code y apuntar a la carpeta que contiene `Mod/GameEngineExportWB`; en el panel izquierdo deberias ver tambien `GameEngineExportLoader.FCMacro`.

## Ubicacion del loader / Loader location

- Ruta relativa dentro del repositorio: `GameEngineExportLoader.FCMacro`.
- En FreeCAD, copia el archivo anterior dentro de tu carpeta `FreeCAD/Macro` junto con la carpeta `Mod/GameEngineExportWB`.
- En caso de dudas, busca `[GAMEEXPORT]` en la consola de FreeCAD despues de ejecutar la macro para confirmar que se encontro y cargo el workbench.

## Workbench vs macro

- **Workbench**: se instala en `Mod/`, ofrece menus y toolbars propios, y carga paneles dedicados sin mezclar con otras macros. Es mas facil mantener configuraciones (ParamGet) y sidecars por archivo, y se actualiza como paquete completo.
- **Macro unitaria**: suele ser un unico archivo en `Macro/`, rapida de compartir pero tiende a mezclar UI y logica en un bloque, con menos separacion de modulos y sin menues persistentes. Para funciones simples es ligera, pero para flujos largos se vuelve dificil de mantener.
- **En este proyecto**: se eligio workbench porque necesitamos paneles, comandos y persistencia, ademas de iconos y recursos adicionales. La macro `GameEngineExportLoader` solo se usa para recargar rapido durante el desarrollo.

## Creditos

Creado por el Ing. Marco Vinicio Mora Fallas con ayuda de ChatGPT (99.9%).

