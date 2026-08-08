# Tarea actual - limpieza de la raiz de Macros

Fecha: 2026-08-08

## Objetivo

Limpiar la raiz del repositorio `MVM444/Macros` para que vuelva a contener solamente puntos de entrada globales, loaders y archivos minimos de control.

## Antecedente

El 2026-06-22/24 se realizo una primera reorganizacion de la raiz. Posteriormente volvieron a aparecer numerosos archivos especializados, pruebas, modelos, capturas y utilidades.

## Decision confirmada por el usuario

`AbrirDirectorioElectricCR.FCMacro` debe permanecer en la raiz.

## Regla de trabajo

No borrar por nombre ni por antiguedad. Primero clasificar y revisar dependencias.

## Grupo Puriscal

Los archivos relacionados con Puriscal deben separarse por funcion.

### Potencialmente reutilizables

- `AnalizarAreasDesdeMuroBIM.FCMacro`
- `CrearAnalisisAreasRectangulares.FCMacro`
- `CrearPoligonosRecintosDesdeMurosBIM.FCMacro`
- `CrearPuertasBIMDesdeSketch.FCMacro`
- `CrearVentanasBIMDesdeSketch.FCMacro`
- `InsertarPuertasBIMDesdeRecintos.FCMacro`
- `InsertarVentanasBIMDesdeRecintos.FCMacro`
- `RecopilarRotulosRecintos.FCMacro`

Estas herramientas deben revisarse antes de decidir si pasan a FacilArquitectura, Scripts Varios u otra ubicacion definitiva.

### Especificos de Puriscal

- `AgregarPuertasFrentePuriscal.FCMacro`
- `OrganizarPuriscalDepurado.FCMacro`
- modelos `Puriscal*.FCStd` o respaldos asociados;
- capturas `Puriscal_*.png`;
- documentacion de handoff y resultados especificos.

## Otros grupos detectados en raiz

- herramientas DXF;
- scripts de revision editorial de Word;
- importadores IFC/CAD;
- archivos de prueba `Silla_Madera.*`;
- resultados temporales y respaldos.

## Resultado esperado

La raiz debe quedar estable, pequena y predecible. Toda excepcion debe quedar documentada.