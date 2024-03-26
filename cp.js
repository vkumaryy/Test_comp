const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

async function isPDFCorrupted(filePath) {
    try {
        const pdfBytes = await fs.promises.readFile(filePath);
        await PDFDocument.load(pdfBytes);
        return false; // PDF is not corrupted
    } catch (error) {
        return true; // PDF is corrupted
    }
}

async function main() {
    const filePath = process.argv[2];
    if (!filePath) {
        console.log('Usage: node checkpdf.js <pdfFilePath>');
        return;
    }

    const isCorrupted = await isPDFCorrupted(filePath);
    console.log(isCorrupted ? "Corrupted PDF" : "Not Corrupted PDF");
}

main();
