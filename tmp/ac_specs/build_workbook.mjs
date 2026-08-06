import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const baseDir = path.resolve("tmp/ac_specs");
const outputDir =
  "C:\\Users\\marco\\OneDrive - Caja Costarricense de Seguro Social\\EIMGF\\Recopilacion_Especificaciones_Aire_Acondicionado";
const previewDir = path.join(baseDir, "previews");

const sources = JSON.parse(
  await fs.readFile(path.join(baseDir, "index", "sources.json"), "utf8"),
);
const history = JSON.parse(
  await fs.readFile(path.join(baseDir, "index", "history_analysis.json"), "utf8"),
);
const content = JSON.parse(
  await fs.readFile(path.join(baseDir, "technical_content.json"), "utf8"),
);
const control2026 = JSON.parse(
  await fs.readFile(path.join(baseDir, "control_2026.json"), "utf8"),
);

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const workbook = Workbook.create();
const palette = {
  navy: "#16324F",
  blue: "#24577A",
  teal: "#2A7F78",
  paleTeal: "#DDEFEA",
  paleBlue: "#E8F0F7",
  paleGold: "#FFF2CC",
  paleRed: "#FCE4E4",
  paleGreen: "#E2F0D9",
  gray: "#667085",
  lightGray: "#E6E9ED",
  white: "#FFFFFF",
  dark: "#1F2937",
};

function writeMatrix(sheet, startRow, startCol, matrix) {
  if (!matrix.length || !matrix[0].length) return null;
  const range = sheet.getRangeByIndexes(
    startRow,
    startCol,
    matrix.length,
    matrix[0].length,
  );
  range.values = matrix;
  return range;
}

function styleTitle(sheet, range, title, subtitle = null) {
  range.merge();
  range.values = [[title]];
  range.format = {
    fill: palette.navy,
    font: { bold: true, color: palette.white, size: 18 },
    verticalAlignment: "center",
    horizontalAlignment: "left",
    wrapText: true,
  };
  range.format.rowHeight = 34;
  if (subtitle) {
    const sub = range.offset(1, 0);
    sub.merge();
    sub.values = [[subtitle]];
    sub.format = {
      fill: palette.paleBlue,
      font: { italic: true, color: palette.dark, size: 10 },
      verticalAlignment: "center",
      wrapText: true,
    };
    sub.format.rowHeight = 28;
  }
}

function styleHeader(range) {
  range.format = {
    fill: palette.blue,
    font: { bold: true, color: palette.white, size: 10 },
    verticalAlignment: "center",
    horizontalAlignment: "center",
    wrapText: true,
    borders: {
      bottom: { style: "medium", color: palette.navy },
    },
  };
  range.format.rowHeight = 30;
}

function styleBody(range) {
  range.format = {
    font: { color: palette.dark, size: 9 },
    verticalAlignment: "top",
    wrapText: true,
    borders: {
      insideHorizontal: { style: "thin", color: palette.lightGray },
    },
  };
}

function addTable(sheet, rangeAddress, name) {
  const table = sheet.tables.add(rangeAddress, true, name);
  table.style = "TableStyleMedium2";
  table.showBandedRows = true;
  table.showFilterButton = true;
  return table;
}

function categorize(source) {
  const primaryPurchase = source.filename.includes("GF-EIM-IT-0031-2025");
  const primaryMaintenance = source.filename.includes("GF-EIM-IT-0020-2023");
  const lesson = [
    "GF-EIM-N-0005-2026",
    "GF-EIM-IT-0025-2026",
  ].some((token) => source.filename.includes(token));
  const falsePositive = source.filename.includes("GF-EIM-N-0032-2026");
  const lowText = Number(source.pages) > 0 && Number(source.text_chars) < 100;

  let relevance = "Complementario";
  let authority = "Histórico / apoyo";
  let reviewStatus = "Extraído";
  if (source.category.startsWith("especificacion_")) relevance = "Fuente técnica";
  if (primaryPurchase) {
    relevance = "Fuente principal";
    authority = "Base compra e instalación";
  }
  if (primaryMaintenance) {
    relevance = "Fuente principal";
    authority = "Base mantenimiento";
  }
  if (lesson) {
    relevance = "Lección técnica";
    authority = "Complemento 2026";
  }
  if (falsePositive) {
    relevance = "No pertinente";
    authority = "Aclaratoria de alquiler Puriscal";
  }
  if (lowText) reviewStatus = "Requiere OCR / revisión visual";
  return { relevance, authority, reviewStatus };
}

// All sheets are created before formulas are assigned.
const summarySheet = workbook.worksheets.add("Resumen");
const inventorySheet = workbook.worksheets.add("Inventario");
const historySheet = workbook.worksheets.add("Cambios históricos");
const findingsSheet = workbook.worksheets.add("Hallazgos");
const normsSheet = workbook.worksheets.add("Normativa");
const matrixSheet = workbook.worksheets.add("Matriz técnica");
const routineSheet = workbook.worksheets.add("Rutina mantenimiento");
const controlSheet = workbook.worksheets.add("Control 2026");

for (const sheet of [
  summarySheet,
  inventorySheet,
  historySheet,
  findingsSheet,
  normsSheet,
  matrixSheet,
  routineSheet,
  controlSheet,
]) {
  sheet.showGridLines = false;
}

// Inventory
styleTitle(
  inventorySheet,
  inventorySheet.getRange("A1:K1"),
  "Inventario documental de aire acondicionado",
  "Fuente principal: EIMGF. La clasificación combina nombre, contenido extraído, firma y fecha.",
);
const inventoryHeaders = [
  "Año",
  "Categoría",
  "Firmado",
  "Archivo",
  "Páginas",
  "Caracteres",
  "Relevancia",
  "Autoridad",
  "Estado de revisión",
  "Ruta",
  "SHA-256",
];
const inventoryRows = sources.map((source) => {
  const c = categorize(source);
  return [
    Number(source.year),
    source.category,
    source.signed ? "Sí" : "No",
    source.filename,
    Number(source.pages),
    Number(source.text_chars),
    c.relevance,
    c.authority,
    c.reviewStatus,
    source.path,
    source.sha256,
  ];
});
writeMatrix(inventorySheet, 3, 0, [inventoryHeaders, ...inventoryRows]);
styleHeader(inventorySheet.getRange("A4:K4"));
styleBody(inventorySheet.getRange(`A5:K${4 + inventoryRows.length}`));
addTable(
  inventorySheet,
  `A4:K${4 + inventoryRows.length}`,
  "InventarioDocumental",
);
inventorySheet.freezePanes.freezeRows(4);
inventorySheet.getRange("A:A").format.columnWidth = 8;
inventorySheet.getRange("B:B").format.columnWidth = 28;
inventorySheet.getRange("C:C").format.columnWidth = 9;
inventorySheet.getRange("D:D").format.columnWidth = 48;
inventorySheet.getRange("E:F").format.columnWidth = 11;
inventorySheet.getRange("G:I").format.columnWidth = 23;
inventorySheet.getRange("J:J").format.columnWidth = 72;
inventorySheet.getRange("K:K").format.columnWidth = 20;
inventorySheet
  .getRange(`G5:G${4 + inventoryRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "principal",
    format: { fill: palette.paleGreen, font: { bold: true, color: "#1E5631" } },
  });
inventorySheet
  .getRange(`I5:I${4 + inventoryRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "OCR",
    format: { fill: palette.paleGold, font: { color: "#8A5A00" } },
  });

// Summary
styleTitle(
  summarySheet,
  summarySheet.getRange("A1:H1"),
  "Recopilación de especificaciones técnicas de aire acondicionado",
  `Corte documental y normativo: ${content.cutoff_date}. ${content.status}.`,
);
summarySheet.getRange("A4:B9").values = [
  ["Indicador", "Valor"],
  ["Documentos candidatos", null],
  ["Fuentes principales", null],
  ["PDF que requieren OCR/revisión", null],
  ["Oficios 2026 pendientes/eliminados", null],
  ["Hallazgos de prioridad alta", null],
];
styleHeader(summarySheet.getRange("A4:B4"));
styleBody(summarySheet.getRange("A5:B9"));
summarySheet.getRange("B5").formulas = [
  [`=COUNTA('Inventario'!$A$5:$A$${4 + inventoryRows.length})`],
];
summarySheet.getRange("B6").formulas = [
  [
    `=COUNTIF('Inventario'!$G$5:$G$${4 + inventoryRows.length},"Fuente principal")`,
  ],
];
summarySheet.getRange("B7").formulas = [
  [
    `=COUNTIF('Inventario'!$I$5:$I$${4 + inventoryRows.length},"Requiere OCR / revisión visual")`,
  ],
];
summarySheet.getRange("B8").formulas = [
  [
    `=COUNTIF('Control 2026'!$C$5:$C$55,"Eliminado / Pendiente")`,
  ],
];
summarySheet.getRange("B9").formulas = [
  [`=COUNTIF('Hallazgos'!$A$5:$A$${4 + content.technical_findings.length},"Alta")`],
];
summarySheet.getRange("A11:H11").merge();
summarySheet.getRange("A11").values = [["Criterio de consolidación"]];
summarySheet.getRange("A11:H11").format = {
  fill: palette.teal,
  font: { bold: true, color: palette.white, size: 11 },
};
summarySheet.getRange("A12:H15").merge();
summarySheet.getRange("A12").values = [[
  "La especificación firmada GF-EIM-IT-0031-2025 se utiliza como base de compra e instalación; GF-EIM-IT-0020-2023 como base de mantenimiento; y los criterios 2026 de Santa Cruz y Turrialba como lecciones de diseño, recepción, drenaje, tensión y seguridad. Las normas vigentes prevalecen sobre requisitos históricos incompatibles.",
]];
summarySheet.getRange("A12:H15").format = {
  fill: palette.paleTeal,
  font: { color: palette.dark, size: 10 },
  wrapText: true,
  verticalAlignment: "center",
};
summarySheet.getRange("A17:H17").merge();
summarySheet.getRange("A17").values = [["Fuentes documentales rectoras"]];
summarySheet.getRange("A17:H17").format = {
  fill: palette.blue,
  font: { bold: true, color: palette.white },
};
const baseRows = content.base_documents.map((item) => [
  item.role,
  item.document,
  item.authority,
  item.date,
]);
writeMatrix(summarySheet, 17, 0, [
  ["Función", "Documento", "Autoridad", "Fecha"],
  ...baseRows,
]);
styleHeader(summarySheet.getRange("A18:D18"));
styleBody(summarySheet.getRange(`A19:D${18 + baseRows.length}`));
summarySheet.getRange("A:A").format.columnWidth = 28;
summarySheet.getRange("B:B").format.columnWidth = 55;
summarySheet.getRange("C:C").format.columnWidth = 42;
summarySheet.getRange("D:D").format.columnWidth = 15;
summarySheet.getRange("E:H").format.columnWidth = 14;
summarySheet.freezePanes.freezeRows(3);

// Historical changes
styleTitle(
  historySheet,
  historySheet.getRange("A1:F1"),
  "Cambios históricos y evolución",
  "Los porcentajes son similitud secuencial aproximada de párrafos entre documentos editables cotejados.",
);
const historyRows = content.historical_summary.map((item) => [
  item.period,
  item.development,
  item.implication,
]);
writeMatrix(historySheet, 3, 0, [
  ["Periodo", "Desarrollo observado", "Implicación"],
  ...historyRows,
]);
styleHeader(historySheet.getRange("A4:C4"));
styleBody(historySheet.getRange(`A5:C${4 + historyRows.length}`));
addTable(
  historySheet,
  `A4:C${4 + historyRows.length}`,
  "ResumenHistorico",
);
let deltaStart = 6 + historyRows.length;
historySheet.getRange(`A${deltaStart}:F${deltaStart}`).merge();
historySheet.getRange(`A${deltaStart}`).values = [["Comparación de versiones"]];
historySheet.getRange(`A${deltaStart}:F${deltaStart}`).format = {
  fill: palette.teal,
  font: { bold: true, color: palette.white },
};
const deltaRows = history.version_deltas.map((delta) => [
  delta.old,
  delta.new,
  Number(delta.sequence_similarity),
  Number(delta.change_blocks.length),
]);
writeMatrix(historySheet, deltaStart, 0, [
  ["Versión anterior", "Versión posterior", "Similitud", "Bloques de cambio"],
  ...deltaRows,
]);
styleHeader(historySheet.getRange(`A${deltaStart + 1}:D${deltaStart + 1}`));
styleBody(
  historySheet.getRange(
    `A${deltaStart + 2}:D${deltaStart + 1 + deltaRows.length}`,
  ),
);
historySheet
  .getRange(`C${deltaStart + 2}:C${deltaStart + 1 + deltaRows.length}`)
  .setNumberFormat("0.0%");
historySheet.getRange("A:A").format.columnWidth = 28;
historySheet.getRange("B:C").format.columnWidth = 62;
historySheet.getRange("D:F").format.columnWidth = 18;
historySheet.freezePanes.freezeRows(4);

// Findings
styleTitle(
  findingsSheet,
  findingsSheet.getRange("A1:E1"),
  "Hallazgos técnicos y actualización recomendada",
  "Prioridad Alta: debe corregirse antes de reutilizar el texto en un cartel.",
);
const findingRows = content.technical_findings.map((item) => [
  item.priority,
  item.topic,
  item.historical_text,
  item.finding,
  item.action,
]);
writeMatrix(findingsSheet, 3, 0, [
  ["Prioridad", "Tema", "Texto/criterio histórico", "Hallazgo", "Acción recomendada"],
  ...findingRows,
]);
styleHeader(findingsSheet.getRange("A4:E4"));
styleBody(findingsSheet.getRange(`A5:E${4 + findingRows.length}`));
addTable(
  findingsSheet,
  `A4:E${4 + findingRows.length}`,
  "HallazgosTecnicos",
);
findingsSheet.getRange("A:A").format.columnWidth = 12;
findingsSheet.getRange("B:B").format.columnWidth = 25;
findingsSheet.getRange("C:E").format.columnWidth = 55;
findingsSheet
  .getRange(`A5:A${4 + findingRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "Alta",
    format: { fill: palette.paleRed, font: { bold: true, color: "#A61B1B" } },
  });
findingsSheet
  .getRange(`A5:A${4 + findingRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "Media",
    format: { fill: palette.paleGold, font: { color: "#8A5A00" } },
  });
findingsSheet.freezePanes.freezeRows(4);

// Norms
styleTitle(
  normsSheet,
  normsSheet.getRange("A1:D1"),
  "Normativa y referencias técnicas vigentes",
  "Se distingue entre obligación jurídica, recomendación pública y referencia técnica.",
);
const normRows = content.normative_sources.map((item) => [
  item.instrument,
  item.status,
  item.application,
  item.url,
]);
writeMatrix(normsSheet, 3, 0, [
  ["Instrumento", "Carácter", "Aplicación", "Fuente oficial"],
  ...normRows,
]);
styleHeader(normsSheet.getRange("A4:D4"));
styleBody(normsSheet.getRange(`A5:D${4 + normRows.length}`));
addTable(normsSheet, `A4:D${4 + normRows.length}`, "NormativaTecnica");
normsSheet.getRange("A:A").format.columnWidth = 48;
normsSheet.getRange("B:B").format.columnWidth = 30;
normsSheet.getRange("C:C").format.columnWidth = 70;
normsSheet.getRange("D:D").format.columnWidth = 75;
normsSheet.freezePanes.freezeRows(4);

// Technical matrix
styleTitle(
  matrixSheet,
  matrixSheet.getRange("A1:F1"),
  "Matriz de especificaciones consolidadas",
  content.scope_note,
);
const matrixRows = [];
for (const section of content.sections) {
  let requirementNumber = 1;
  const sectionNumber = section.heading.split(".")[0];
  for (const requirement of section.requirements) {
    matrixRows.push([
      `${sectionNumber}.${requirementNumber}`,
      section.heading,
      requirement,
      sectionNumber === "5" || sectionNumber === "6" || sectionNumber === "7"
        ? "Actualizado con norma vigente"
        : "Consolidado",
      "Validación técnica previa al cartel",
      "Word consolidado",
    ]);
    requirementNumber += 1;
  }
}
writeMatrix(matrixSheet, 3, 0, [
  ["ID", "Sección", "Requisito consolidado", "Origen/estado", "Control", "Destino"],
  ...matrixRows,
]);
styleHeader(matrixSheet.getRange("A4:F4"));
styleBody(matrixSheet.getRange(`A5:F${4 + matrixRows.length}`));
addTable(matrixSheet, `A4:F${4 + matrixRows.length}`, "MatrizConsolidada");
matrixSheet.getRange("A:A").format.columnWidth = 10;
matrixSheet.getRange("B:B").format.columnWidth = 36;
matrixSheet.getRange("C:C").format.columnWidth = 90;
matrixSheet.getRange("D:F").format.columnWidth = 28;
matrixSheet.freezePanes.freezeRows(4);

// Routine
styleTitle(
  routineSheet,
  routineSheet.getRange("A1:E1"),
  "Rutina consolidada de mantenimiento preventivo",
  "Base: anexo de mantenimiento 2023, depurado y actualizado con criterios de diagnóstico.",
);
const routineRows = content.maintenance_routine.map((item, index) => [
  index + 1,
  item,
  "Trimestral en garantía",
  "Pendiente / Realizado / N.A.",
  "Registrar medición u observación",
]);
writeMatrix(routineSheet, 3, 0, [
  ["Nº", "Actividad", "Frecuencia base", "Resultado", "Evidencia"],
  ...routineRows,
]);
styleHeader(routineSheet.getRange("A4:E4"));
styleBody(routineSheet.getRange(`A5:E${4 + routineRows.length}`));
addTable(
  routineSheet,
  `A4:E${4 + routineRows.length}`,
  "RutinaPreventiva",
);
routineSheet.getRange("A:A").format.columnWidth = 8;
routineSheet.getRange("B:B").format.columnWidth = 85;
routineSheet.getRange("C:E").format.columnWidth = 28;
routineSheet.getRange(`D5:D${4 + routineRows.length}`).dataValidation = {
  rule: { type: "list", values: ["Pendiente", "Realizado", "N.A."] },
};
routineSheet.freezePanes.freezeRows(4);

// 2026 control
styleTitle(
  controlSheet,
  controlSheet.getRange("A1:E1"),
  "Control de consecutivos 2026",
  "Inventario suministrado por el usuario; registra faltantes, eliminados y duplicados. No implica pertinencia técnica con aire acondicionado.",
);
const controlRows = control2026.map(([number, filename, status]) => {
  let relevance = "Fuera del tema por nombre";
  let note = "";
  if (number === "0005") {
    relevance = "Complementario de A.A.";
    note = "Criterio técnico Santa Cruz; aporta lecciones de recepción y diseño.";
  } else if (number === "0032") {
    relevance = "No pertinente a A.A.";
    note = "Aclaratoria de especificaciones para alquiler de Puriscal.";
  } else if (status.includes("Duplicado")) {
    relevance = "Control documental";
    note = "Dos archivos comparten el consecutivo 0036.";
  } else if (status.includes("Pendiente")) {
    relevance = "Sin documento";
    note = "No existe archivo asociado en la lista preliminar.";
  }
  return [number, filename, status, relevance, note];
});
writeMatrix(controlSheet, 3, 0, [
  ["Nº Oficio", "Archivo / estado", "Condición", "Pertinencia A.A.", "Observación"],
  ...controlRows,
]);
styleHeader(controlSheet.getRange("A4:E4"));
styleBody(controlSheet.getRange(`A5:E${4 + controlRows.length}`));
addTable(controlSheet, `A4:E${4 + controlRows.length}`, "ControlOficios2026");
controlSheet.getRange("A:A").format.columnWidth = 12;
controlSheet.getRange("B:B").format.columnWidth = 75;
controlSheet.getRange("C:D").format.columnWidth = 28;
controlSheet.getRange("E:E").format.columnWidth = 60;
controlSheet
  .getRange(`C5:C${4 + controlRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "Pendiente",
    format: { fill: palette.paleGold, font: { color: "#8A5A00" } },
  });
controlSheet
  .getRange(`C5:C${4 + controlRows.length}`)
  .conditionalFormats.add("containsText", {
    text: "Duplicado",
    format: { fill: palette.paleRed, font: { bold: true, color: "#A61B1B" } },
  });
controlSheet.freezePanes.freezeRows(4);

// Common body row sizing.
for (const sheet of [
  inventorySheet,
  historySheet,
  findingsSheet,
  normsSheet,
  matrixSheet,
  routineSheet,
  controlSheet,
]) {
  const used = sheet.getUsedRange();
  used.format.autofitRows();
}

const checks = [];
for (const sheetName of [
  "Resumen",
  "Inventario",
  "Cambios históricos",
  "Hallazgos",
  "Normativa",
  "Matriz técnica",
  "Rutina mantenimiento",
  "Control 2026",
]) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const used = sheet.getUsedRange();
  checks.push(
    await workbook.inspect({
      kind: "table",
      sheetId: sheetName,
      range: used.address,
      include: "values,formulas",
      tableMaxRows: 8,
      tableMaxCols: 8,
      maxChars: 2500,
    }),
  );
  const preview = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 0.8,
    format: "png",
  });
  await fs.writeFile(
    path.join(previewDir, `${sheetName.replaceAll(" ", "_")}.png`),
    new Uint8Array(await preview.arrayBuffer()),
  );
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 3000,
});
console.log(errors.ndjson);

const outputPath = path.join(
  outputDir,
  "Trazabilidad_y_analisis_historico_aire_acondicionado.xlsx",
);
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(
  JSON.stringify(
    {
      outputPath,
      sheetCount: 8,
      inventoryRows: inventoryRows.length,
      matrixRows: matrixRows.length,
      previewDir,
    },
    null,
    2,
  ),
);
