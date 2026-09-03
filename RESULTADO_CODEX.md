# Resultado Codex - Programacion y limpieza de raiz

Fecha: 2026-08-12
FreeCAD: 1.1.3 en Windows
Estado: IMPLEMENTADO Y PROBADO EN GUI; REINICIO FINAL Y VALIDACION DE MARCO PENDIENTES

## Movimientos realizados mediante Git

- Los cuatro `*Loader.FCMacro` y sus cuatro SVG: raiz -> `Loaders/`.
- `UI_Audit_FreeCAD.FCMacro`: raiz -> `Programación/`.
- `Alias.FCMacro`: raiz -> `Scripts Varios/Spreadsheet/`.
- `VentanadeMacros.FCMacro`: se mantiene en la raiz como punto de entrada global confirmado.
- `AbrirDirectorioDocumento.FCMacro`, su SVG y `AbrirDirectorioElectricCR.FCMacro`:
  raiz -> `Respaldos/Programacion_reemplazadas/` despues de validar la herramienta sustituta.

No se elimino ningun archivo.

## Cambios de rutas

- `RegistrarLoadersGlobales.FCMacro` busca macros e iconos dentro de `Loaders/`.
- Los loaders toman la raiz del repositorio como el padre de `Loaders`.
- `Macros-de-Freecad/loader_toolbar.py` permanece en su ubicacion compartida.
- Los comandos persistentes guardan `Loaders/<loader>.FCMacro`, conservando sus
  CommandName existentes y evitando registros duplicados.
- La herramienta consolidada se llama `Programación/Abrir_Directorios_FreeCAD.FCMacro`.
- `.macro_recent.json` y la copia por equipo migraron rutas trasladadas sin borrar el historial.

## Macros Personalizadas

La verificacion GUI confirmo los submenus `Loaders`, `Programación`,
`Scripts Varios` y `Respaldos`, `RegistrarLoadersGlobales` visible en raiz y
ausencia de archivos `.py` como acciones ejecutables. `_resolve_macro_path()`
resuelve por existencia, rutas relativas y busqueda conservadora por nombre.

## Pruebas GUI FreeCAD 1.1.3

- `RegistrarLoadersGlobales.FCMacro`: aprobado.
- ElectricCRLoader -> `ElectricCRWorkbench`: aprobado.
- FacilArquitecturaLoader -> `FacilArquitecturaWorkbench`: aprobado.
- GameEngineExportLoader -> `GameEngineExportWorkbench`: aprobado.
- MEPWorkbenchCRLoader -> `MEPWorkbenchCR`: aprobado.
- Barras detectadas: una `Macros` y una `Programacion`.
- Scripts persistentes: cuatro rutas `Loaders/*.FCMacro`.
- `Abrir_Directorios_FreeCAD`: resolucion dinamica y apertura de `Programación`, aprobadas.
- `CopyReportLast1Min`: siguio visible/ejecutable, aprobado.

## Pendiente

- Marco debe reiniciar FreeCAD y confirmar visualmente que no reaparecen barras duplicadas.
- No mover otras versiones antiguas a `Programación/Antiguas` sin autorizacion.
- La tarea anterior de Areas sigue implementada y pendiente de validacion de Marco.

No se modifico ni guardo ningun `.FCStd`. No se hizo commit ni push.

## Ollama y diagnostico legacy (2026-08-12)

La implementacion existente de Ollama fue localizada en el historial Git local:

- Ruta anterior: `Macros/Ollama_Asistente_Local.FCMacro`.
- Commit fuente: `7c4db88d0bde132c5dd404c1ef85b3aef1f72aa2`.
- Ruta nueva: `Macros/Programacion/Ollama_Asistente_Local.FCMacro` (carpeta real con tilde).
- Icono exclusivo: `ollama_llama_icon.svg`, movido junto con la macro.

La fuente y el icono se recuperaron exactamente del historial; no se creo otra
implementacion ni se rediseno la interfaz. En FreeCAD 1.1.3 la macro abrio la
ventana original `Ollama Chat Local - FreeCAD`. No se envio ninguna consulta.
`Macros Personalizadas > Programacion` contiene `Ollama_Asistente_Local`.
Tambien se agrego `Ollama Asistente Local` como boton propio de la barra
`Programacion`, reutilizando `ollama_llama_icon.svg`.

`VentanadeMacros.FCMacro` permanece en la raiz. La regla quedo escrita en
`AGENTS.md` y en la documentacion para impedir que vuelva a clasificarse como
interfaz legacy.

`Scripts Varios/Diagnostico/AutoCorreccion_Local.FCMacro` se confirmo como
generador de contexto/reporte JSON cuyo trabajo protegido solo devuelve nombre
del documento y conteo de objetos. No usa Ollama ni corrige objetos; se movio
intacto a `Respaldos/Diagnostico_legacy/AutoCorreccion_Local.FCMacro`. No tenia
SVG companero ni referencias activas de importacion/ejecucion.

## Registrador dinamico de loaders

`RegistrarLoadersGlobales.FCMacro` ahora descubre automaticamente los
`Loaders/*.FCMacro` del nivel inmediato, exige el SVG con el mismo nombre base,
registra u omite con mensajes de consola y conserva
`Macros-de-Freecad/loader_toolbar.py`. Se agrego
`RegistrarLoadersGlobales.svg` en la raiz.

Pruebas GUI FreeCAD 1.1.3:

- Primera y segunda ejecucion del registrador: cuatro loaders en ambas.
- Los cuatro loaders activaron su Workbench correspondiente.
- Cambio a Part: una barra `Macros` y una `Programacion`.
- Rutas persistentes: cuatro entradas unicas `Loaders/*.FCMacro`.
- Compilacion sintactica de registrador, loaders, helper, Ollama,
  AutoCorreccion y MacrosPersonalizadas: aprobada.
- SVG del registrador y de Ollama: XML valido.

La activacion de MEP durante la prueba creo su jerarquia HVAC vacia en memoria;
los cinco grupos de prueba fueron identificados y retirados. El documento no se
guardo. El reinicio final no se realizo porque `La_Cruz_Version_2_1` estaba
abierto; queda como validacion manual para Marco.

## Instalacion externa de FreeCAD-HVAC (2026-08-22)

Estado: **INSTALADO Y VALIDADO EN FREECAD 1.1.3**.

### Alcance y separacion

FreeCAD-HVAC se instalo como complemento externo independiente. No se copio
codigo dentro de ElectricCR, FacilArquitecturaWB, MEPWorkbenchCR, GameExport ni
las macros propias. Tampoco se modifico ningun archivo fuente del complemento.

Ruta final:

`C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC`

La estructura quedo correcta, sin un nivel ZIP adicional: en la raiz del clon
estan `.git`, `package.xml`, `README.md`, `LICENSE` y `freecad/`; el paquete del
Workbench esta directamente en `freecad/HVAC/`.

### Git y version instalada

- Origen de fetch y push: `https://github.com/Francisco-Rosa/FreeCAD-HVAC.git`.
- Rama: `main`.
- Commit: `ae8e28464ef4616b7570d22b0464960113086ce5`.
- Mensaje del commit: `Merge pull request #6 from manuvarkey/main`.
- Historial completo: 40 commits; `--is-shallow-repository=false`.
- `git status`, `git diff` y `git fsck`: aprobados; arbol limpio.
- No se creo ningun commit local.

### Estructura, metadatos y dependencias

`package.xml` declara:

- nombre del Workbench: `HVAC`;
- version del complemento: `2026.03.01`;
- FreeCAD minimo: `1.0.0`;
- licencia: `LGPL-2.1-or-later`;
- rama de repositorio: `main`;
- clase de Workbench: `HVAC`.

El proyecto usa el formato moderno de paquete `freecad/HVAC/init_gui.py`; no
incluye `Init.py`/`InitGui.py` clasicos en la raiz. FreeCAD reconocio
`freecad.HVAC` y completo su inicializacion GUI.

No hay dependencias Python ni de otros Addons declaradas en `package.xml`. El
codigo de ejecucion usa modulos incluidos con FreeCAD (`FreeCAD`, `FreeCADGui`,
`Part`, `Draft`, `PySide` y `pivy`). El repositorio incluye su propia copia de
`networkx` 3.6.1 en `freecad/HVAC/ext_libs`, por lo que la prueba no requirio
instalar paquetes con `pip`. Algunas funciones opcionales de la biblioteca
vendorizada pueden requerir dependencias cientificas adicionales, pero no se
usaron ni fueron necesarias para la red minima probada.

### Prueba real en FreeCAD 1.1.3

FreeCAD probado:

- ejecutable: `C:\Users\marco\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCAD.exe`;
- version: `1.1.3`, build `20260725 (Git shallow)`;
- datos de usuario: `C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\`.

Resultados GUI:

- FreeCAD inicio normalmente;
- `HVAC` aparecio en `Gui.listWorkbenches()` y, por tanto, en el selector;
- se activo como Workbench actual;
- aparecieron el menu y la barra `HVAC`, visibles y con 13 acciones principales;
- se registraron 16 comandos `HVAC_*`; no falto ninguno de los 13 esperados;
- se creo una red `DuctNetwork` mediante `HVAC_CreateDuctNetwork`;
- se agrego una ruta Draft recta de 2000 mm;
- la sincronizacion genero un segmento `circular_straight` y dos terminales;
- el documento temporal se cerro sin guardar;
- al finalizar no quedo ningun documento temporal ni proceso FreeCAD abierto.

La prueba y sus evidencias quedaron fuera del repositorio del complemento en:

- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/Verificar_FreeCAD_HVAC_1_1_3.py`;
- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/resultado_verificacion_2026-08-22.json`;
- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/FreeCAD_1_1_3_HVAC.log`.

### Errores y advertencias

No se registraron errores de FreeCAD-HVAC durante la carga, activacion ni prueba
geometrica. El log si contiene un `FileNotFoundError` previo y ajeno a HVAC para:

`C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FacilArquitecturaWB\FacilArquitecturaWB`

No se corrigio ni se altero FacilArquitecturaWB porque estaba fuera del alcance
de esta instalacion. Los mensajes sobre ausencia de `Init.py`/`InitGui.py` en la
raiz del clon son parte del descubrimiento del formato de paquete; FreeCAD cargo
despues `freecad.HVAC/init_gui.py` correctamente.

### Actualizacion futura recomendada

Con FreeCAD cerrado:

```powershell
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" status --short
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" fetch origin
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" pull --ff-only origin main
```

Antes de actualizar conviene confirmar que `status --short` no produzca salida.
Usar `--ff-only` evita crear merges locales accidentales. No copiar ni parchear
el repositorio oficial; cualquier integracion futura debe implementarse desde
nuestros Workbenches mediante adaptadores externos y contratos publicos.

### Pendientes

- Evaluar por separado la advertencia de ruta de FacilArquitecturaWB.
- Probar redes ramificadas y bibliotecas de perfiles solo cuando se defina una
  tarea funcional especifica; la instalacion y el flujo basico ya estan aprobados.

## Reverificacion de FreeCAD-HVAC (2026-09-02)

Estado: **INSTALACION EXISTENTE, VIGENTE Y REVALIDADA EN FREECAD 1.1.3**.

### Diagnostico previo y decision de instalacion

FreeCAD reporto directamente mediante `--dump-config`:

- ejecutable GUI:
  `C:\Users\marco\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCAD.exe`;
- ejecutable de consola:
  `C:\Users\marco\AppData\Local\Programs\FreeCAD 1.1\bin\FreeCADCmd.exe`;
- version: `1.1.3`, revision `20260725 (Git shallow)`, hash de FreeCAD
  `145529fe741292ff0b3977a01195bf0247425794`;
- datos de usuario: `C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\`;
- modulos de usuario:
  `C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod`.

Ya existia un clon Git correcto en:

`C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC`

La busqueda en las ubicaciones de usuario aplicables no encontro otra copia,
ZIP ni extraccion `FreeCAD-HVAC-main`/`FreeCAD-HVAC-master`. Como la instalacion
existente estaba limpia, completa y en el mismo commit publicado por
`origin/main`, no se reclono, no se sobrescribio y no se ejecuto un `pull`
innecesario.

### Git, estructura e integridad

- Remoto de fetch y push:
  `https://github.com/Francisco-Rosa/FreeCAD-HVAC.git`.
- Rama instalada: `main`.
- Commit local: `ae8e28464ef4616b7570d22b0464960113086ce5`.
- `git ls-remote` confirmo que `refs/heads/main` remoto apunta al mismo commit.
- Repositorio no shallow.
- `git status --short --branch`: `## main...origin/main`, sin cambios.
- `git diff`, `git diff --cached` y `git fsck --full`: aprobados.
- No se modifico ningun archivo fuente ni se creo ningun commit local.

La raiz contiene directamente `.git`, `package.xml`, `README.md`, `LICENSE` y
`freecad/`; el paquete esta en `freecad/HVAC/`. No existe el nivel incorrecto
`FreeCAD-HVAC/FreeCAD-HVAC-main`.

### Metadatos y dependencias

`package.xml` es XML valido y declara Workbench/clase `HVAC`, version del Addon
`2026.03.01`, FreeCAD minimo `1.0.0`, licencia `LGPL-2.1-or-later` y rama
`main`. Usa el formato moderno `freecad/HVAC/init_gui.py`; la ausencia de
`Init.py`/`InitGui.py` clasicos en la raiz es esperada y no impide la carga.

No declara dependencias Python ni Addons externos. El codigo usa la biblioteca
estandar y modulos incluidos con FreeCAD: `FreeCAD`, `FreeCADGui`, `Part`,
`Draft`, `PySide` y `pivy`. Tambien usa `networkx` 3.6.1:

- el repositorio incluye una copia funcional en
  `freecad/HVAC/ext_libs/networkx`;
- una prueba aislada con el Python de FreeCAD importo correctamente esa copia;
- en la prueba GUI real FreeCAD resolvio primero otra copia 3.6.1 ya instalada
  en `AdditionalPythonPackages/py311`, porque el Workbench agrega su ruta
  vendorizada al final de `sys.path`.

La red minima no necesito `pip` ni paquetes adicionales. Algunos algoritmos
opcionales de `networkx` pueden importar NumPy, SciPy, pandas u otras bibliotecas
solo cuando se usan; no forman parte del flujo de ductos validado.

### Prueba GUI real y no persistente

Se inicio un proceso separado de FreeCAD 1.1.3 con la ruta real de datos de
usuario y una configuracion de prueba aislada. La sesion que ya estaba abierta
(PID 38280) no se cerro ni se manipulo; solo el proceso de prueba (PID 100800)
se cerro al terminar.

Resultado:

- FreeCAD inicio y `HVAC` aparecio en `Gui.listWorkbenches()`;
- HVAC se activo como Workbench actual;
- el paquete se cargo desde la ruta Git esperada;
- menu y barra `HVAC` visibles, ambos con 13 acciones principales;
- 16 comandos `HVAC_*` registrados y ninguno de los 13 esperados ausente;
- `HVAC_CreateDuctNetwork` creo una red `DuctNetwork`;
- una linea Draft de 2000 mm se agrego como ruta;
- la sincronizacion produjo un segmento `circular_straight` y dos terminales
  `end_terminal_marker`;
- el documento temporal se cerro sin guardar y no quedo abierto en el proceso;
- el proceso de prueba termino normalmente.

Evidencias nuevas, todas fuera del repositorio oficial:

- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/Verificar_FreeCAD_HVAC_1_1_3_2026-09-02.py`;
- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/resultado_verificacion_2026-09-02.json`;
- `Documentacion_organizacion/Pruebas_FreeCAD_HVAC/FreeCAD_1_1_3_HVAC_2026-09-02.log`.

### Errores y advertencias

No hubo error, excepcion ni advertencia atribuible a FreeCAD-HVAC. El log
confirmo `HVAC - Workbench loaded`, registro de observadores, creacion de red y
sincronizacion.

El inicio registro dos incidencias ajenas al complemento y no se corrigieron por
estar fuera de alcance:

- `FileNotFoundError` por el destino inexistente de
  `Mod/FacilArquitecturaWB/FacilArquitecturaWB`;
- con la configuracion aislada de la prueba, `MacrosPersonalizadasStartup` no
  encontro `MacrosPersonalizadas.FCMacro` en `MacroPath`.

Los mensajes de que no existe `Init.py`/`InitGui.py` en la raiz del clon son
informativos del descubrimiento de paquetes; seguidamente FreeCAD inicializo
`freecad.HVAC/init_gui.py` correctamente.

### Separacion, pendientes y actualizacion futura

FreeCAD-HVAC continua totalmente separado de ElectricCR, FacilArq,
MEPWorkbenchCR, GameExport y las macros propias. No se copio ni adapto codigo
del Workbench externo.

Pendientes fuera de esta instalacion:

- revisar en una tarea independiente el enlace roto de FacilArquitecturaWB;
- probar redes ramificadas, perfiles adicionales y operaciones avanzadas solo
  cuando exista un alcance funcional especifico.

Para actualizar posteriormente, cerrar FreeCAD y ejecutar:

```powershell
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" status --short
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" fetch origin
git -C "C:\Users\marco\AppData\Roaming\FreeCAD\v1-1\Mod\FreeCAD-HVAC" pull --ff-only origin main
```

Continuar solo si el primer comando no muestra cambios. `--ff-only` conserva
una historia lineal y evita merges locales accidentales. Cualquier extension o
integracion futura debe vivir en nuestros Workbenches/adaptadores, no como
parche dentro del clon oficial.
