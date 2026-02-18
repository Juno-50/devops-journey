const fs = require("fs");
const path = require("path");

async function ensureDir(dirPath) {
  await fs.promises.mkdir(dirPath, { recursive: true });
}

async function writeJsonFile(filePath, data) {
  await ensureDir(path.dirname(filePath));
  const json = JSON.stringify(data, null, 2);
  await fs.promises.writeFile(filePath, json, "utf8");
}

function toCsv(rows) {
  if (!rows || rows.length === 0) {
    return "";
  }
  const headers = Object.keys(rows[0]);
  const escape = (value) => {
    if (value == null) return "";
    const str = String(value);
    if (str.includes('"') || str.includes(",") || str.includes(" ")) {
      return `"${str.replace(/"/g, '""')}"`;
    }
    return str;
  };
  const headerLine = headers.join(",");
  const lines = rows.map((row) =>
    headers.map((h) => escape(row[h])).join(",")
  );
  return [headerLine, ...lines].join("\n");
}

async function writeCsvFile(filePath, rows) {
  await ensureDir(path.dirname(filePath));
  const csv = toCsv(rows);
  await fs.promises.writeFile(filePath, csv, "utf8");
}

module.exports = {
  ensureDir,
  writeJsonFile,
  writeCsvFile,
  toCsv,
};