# Plantilla para investigaciones documentales técnicas con Codex

## Propósito

Esta plantilla sirve para iniciar una investigación documental similar a la recopilación de especificaciones técnicas de aire acondicionado. Incluye las instrucciones que ayudan a reducir retrasos por duplicados, documentos escaneados, archivos de OneDrive, conversiones de Word y grandes cantidades de archivos.

Copie el bloque siguiente en un nuevo chat y sustituya los campos entre corchetes.

---

## Instrucción reutilizable

Deseo realizar una investigación documental técnica similar. Use razonabilidad alta y continúe de manera autónoma, sin detenerse por dificultades normales de extracción, duplicados o conversión.

### 1. Directorios

El directorio principal es:

`[DIRECTORIO PRINCIPAL]`

Los siguientes directorios contienen posibles copias:

```text
[DIRECTORIO SECUNDARIO 1]
[DIRECTORIO SECUNDARIO 2]
[DIRECTORIO SECUNDARIO 3]
```

Inicie por el año más reciente y avance hacia atrás.

### 2. Alcance

La búsqueda se limitará a:

`[TEMA, ABREVIATURAS Y SINÓNIMOS]`

Excluya expresamente:

`[EQUIPOS, SISTEMAS O TEMAS FUERA DEL ALCANCE]`

No incorpore información ajena a las especificaciones, salvo normativa, aclaraciones, inspecciones o antecedentes necesarios para comprobar y actualizar los requisitos.

### 3. Autoridad documental

Aplique el siguiente orden:

1. Priorice el PDF firmado más reciente localizado en el directorio principal.
2. Use el documento editable correspondiente únicamente para recuperar texto, tablas y estructura.
3. Use documentos anteriores para reconstruir la evolución histórica.
4. Use aclaraciones, modificaciones, inspecciones y recepciones como lecciones técnicas.
5. Si dos documentos se contradicen, prevalecerá el documento firmado más reciente, salvo que una norma vigente establezca otra condición.
6. No modifique, mueva, renombre ni elimine los documentos fuente.

### 4. Inventario inicial

Antes de redactar, cree un inventario que contenga como mínimo:

- Año.
- Número de oficio o informe.
- Nombre del archivo.
- Ruta completa.
- Tipo documental.
- Estado de firma.
- Número de páginas.
- Cantidad de texto extraíble.
- Relevancia técnica.
- Autoridad documental.
- Estado de revisión.
- Necesidad de OCR o revisión visual.
- Hash o identificador para detectar duplicados.

Deduplicate por número documental, firma, contenido y hash; no solamente por nombre de archivo.

Los archivos con nombres distintos pero contenido igual deben registrarse como copias. Los archivos con el mismo número pero contenido diferente deben marcarse para revisión.

### 5. Extracción y análisis

Identifique:

- Requisitos vigentes y repetidos.
- Cambios históricos.
- Requisitos agregados o eliminados.
- Contradicciones.
- Requisitos posiblemente obsoletos.
- Aclaraciones y modificaciones.
- Lecciones de instalación, recepción, fallas, garantía y mantenimiento.
- Documentos faltantes.
- Números duplicados.
- Versiones firmadas y no firmadas.
- Diferencias entre PDF y documento editable.

Para documentos escaneados:

- Márquelos inicialmente como “Requiere OCR / revisión visual”.
- Realice OCR solamente cuando el documento tenga relevancia técnica y no exista otra versión legible.
- No permita que el OCR sustituya la comprobación del documento firmado.

### 6. Análisis histórico

Compare las versiones por año y registre:

- Documento anterior.
- Documento posterior.
- Fecha.
- Similitud aproximada.
- Requisitos incorporados.
- Requisitos eliminados.
- Requisitos modificados.
- Cambios de evaluación o puntuación.
- Cambios de garantía y mantenimiento.
- Implicación técnica del cambio.

No suponga que el documento más extenso es necesariamente el más vigente o autorizado.

### 7. Normativa

Contraste los requisitos únicamente con fuentes oficiales y normativa vigente, especialmente:

```text
[INSTITUCIONES, REGLAMENTOS Y NORMAS APLICABLES]
```

Para cada referencia registre:

- Instrumento.
- Edición o decreto.
- Estado de vigencia.
- Aplicación en las especificaciones.
- Enlace oficial.
- Requisito histórico afectado.
- Acción recomendada.

Cuando una afirmación normativa pueda haber cambiado, verifíquela en la fuente oficial vigente y no dependa únicamente del conocimiento previo de Codex.

### 8. Entregables

Prepare:

1. Un documento Word con únicamente las especificaciones técnicas consolidadas.
2. Un Excel con inventario, trazabilidad, análisis histórico, hallazgos, normativa, matriz técnica y control documental.

El Word debe quedar identificado como:

> Borrador técnico consolidado para revisión institucional.

No debe presentarse como documento oficialmente aprobado.

El Word deberá incluir, cuando corresponda:

- Objeto y alcance.
- Jerarquía documental.
- Levantamiento y diseño.
- Requisitos de equipos.
- Instalación.
- Obras asociadas.
- Puesta en marcha.
- Recepción.
- Garantía.
- Mantenimiento preventivo.
- Mantenimiento correctivo.
- Personal y seguridad.
- Informes y trazabilidad.
- Cuadro de datos que debe completar cada contratación.
- Entregables mínimos de recepción.
- Normativa y referencias oficiales.

El Excel deberá incluir, como mínimo:

- Resumen.
- Inventario.
- Cambios históricos.
- Hallazgos.
- Normativa.
- Matriz técnica.
- Rutina de mantenimiento.
- Control de números documentales.

### 9. Reglas para evitar bloqueos y retrasos

- Realice extracción, comparación y conversiones sobre copias temporales locales.
- No dependa de archivos abiertos directamente desde OneDrive para renderizar o convertir.
- Preserve intactos los documentos fuente.
- Use PDF firmado como autoridad y DOCX como apoyo estructural.
- Use numeración nativa de Word; evite definiciones de numeración personalizadas innecesarias.
- No mezcle la numeración de fuentes documentales con la numeración de cláusulas técnicas.
- Evite dividir tablas extensas de forma inestable entre páginas.
- Si una tabla provoca bloqueos, manténgala en una página nueva o divídala de manera controlada.
- Si LibreOffice no está disponible, use Microsoft Word sobre una copia local para verificar el renderizado.
- Si Word queda bloqueado, detenga únicamente la instancia temporal creada por Codex.
- Evite caracteres comodín no controlados en fórmulas de Excel.
- Compruebe que las fórmulas muestran resultados correctos.
- Mantenga enlaces oficiales completos en la hoja de normativa.
- No deje archivos auxiliares de inspección junto a los entregables finales.

### 10. Verificación obligatoria

Antes de entregar:

- Verifique todas las páginas del Word después de renderizarlo.
- Compruebe cortes de texto, numeración, tablas, encabezados y pies de página.
- Confirme que no existan textos dañados, caracteres extraños, “TODO”, “TBD” o marcadores pendientes.
- Verifique visualmente todas las hojas del Excel.
- Revise filtros, paneles congelados, anchos de columna, formatos, fórmulas y listas desplegables.
- Compruebe el número de documentos inventariados y requisitos consolidados.
- Confirme que la versión entregada sea exactamente la versión revisada.
- Entregue solamente los archivos finales solicitados.

### 11. Forma de trabajo

Manténgame informado por etapas, pero continúe trabajando sin solicitar confirmaciones repetidas, salvo que:

- Una decisión cambie materialmente el alcance.
- Falte una fuente indispensable.
- Exista riesgo de modificar o eliminar documentos fuente.
- Sea necesario elegir entre dos criterios técnicos incompatibles.
- La normativa no permita determinar una respuesta razonable.

Cuando exista una dificultad técnica normal, aplique una alternativa segura y continúe.

---

## Datos que conviene proporcionar al iniciar un nuevo chat

Para reducir preguntas y retrasos, indique desde el principio:

- Directorio principal.
- Directorios de copias.
- Año inicial y orden de revisión.
- Tema y sinónimos.
- Exclusiones.
- Documento que debe prevalecer.
- Tipos de equipo incluidos y excluidos.
- Si se autoriza OCR.
- Normativa prioritaria.
- Formato de los entregables.
- Público destinatario.
- Carpeta de salida.
- Si se requiere análisis histórico.
- Si se requiere control de documentos faltantes y duplicados.

## Nota

Una investigación extensa puede completarse por fases. Si existen muchos documentos escaneados, conviene consolidar primero las fuentes legibles y relevantes, y dejar el OCR histórico como una segunda fase claramente identificada.
