const fs = require('fs');
const { performance } = require('perf_hooks');
const PDFParser = require('pdf2json');

function checkPDF(file) {
    const t0 = performance.now();
    if (!file.endsWith('.pdf')) {
        return "Please put extension in this file.";
    } else {
        const pdfParser = new PDFParser();
        pdfParser.loadPDF(file);
        pdfParser.on('pdfParser_dataReady', (pdfData) => {
            const t1 = performance.now();
            const metaData = pdfData.formImage.Pages[0].MediaBox;
            console.log("Metadata:", metaData);
            console.log("Time taken to read metadata:", (t1 - t0), "milliseconds");
        });
    }
}

// Example usage:
const file = 'example_file'; // Path to your file
checkPDF(file);
