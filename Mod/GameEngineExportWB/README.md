# Game Engine Export WB

## Resumen / Summary

Game Engine Export WB prepara escenas de FreeCAD para Castle Game Engine con escala en metros, rotacion global en X de -90 grados y soporte para Viewpoint inicial, luces y persistencia de configuracion.

## Estado

Version inicial 0.1.0 (2025-10-13 13:54 UTC). Solo contiene la estructura base y paneles de interfaz sin logica de exportacion.

## Instalacion rapida

1. Copiar la carpeta `Mod/GameEngineExportWB` dentro del directorio de macros o mods de FreeCAD.
2. Reiniciar FreeCAD.
3. Seleccionar el workbench **Game Engine Export WB**.

## Uso rapido

Abre el comando **GameEngineExport Open** para mostrar el panel principal. Desde ahi podras elegir la raiz de la escena, listas de objetos, marcador GameStart, luces y carpeta de salida. Aun no existe funcionalidad final de exportacion.

## Archivos incluidos

- `Init.py`, `InitGui.py`: arranque del workbench y registro de comandos.
- `core/`: modulos para exportar, manejar luces, persistencia y utilidades.
- `ui/`: paneles TaskPanel de escena, configuracion y texto informativo.
- `commands/`: comando principal GameEngineExport_Open.
- `resources/icons/gameexport.svg`: icono del workbench.

## Creditos

Creado por el Ing. Marco Vinicio Mora Fallas con ayuda de ChatGPT (99.9%).

