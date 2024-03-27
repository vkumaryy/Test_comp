const fs = require('fs');
const PDFParser = require('pdf-parse');

async function isPDFCorrupted(filePath) {
    try {
        const dataBuffer = fs.readFileSync(filePath);
        const pdfData = await PDFParser(dataBuffer);
        
        // Check if the parsed PDF data contains necessary properties
        if (pdfData && pdfData.text) {
            return false; // PDF is not corrupted
        } else {
            return true; // PDF is corrupted
        }
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
