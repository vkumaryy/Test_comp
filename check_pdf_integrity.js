const { PDFDocument } = require('pdf-lib');

async function checkPdfIntegrity(filePath) {
    try {
        const pdfDoc = await PDFDocument.load(filePath);
        console.log("PDF file appears valid (basic checks passed using pdf-lib).");
    } catch (error) {
        console.error("Error:", error.message);
    }
}

const filePath = process.argv[2]; // Get file path from command line argument

if (!filePath) {
    console.error("Error: Please provide a PDF file path as a command line argument.");
    process.exit(1); // Exit with error code
}

checkPdfIntegrity(filePath);
