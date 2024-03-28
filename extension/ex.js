const fs = require('fs');
const { performance } = require('perf_hooks');
const pdfParse = require('pdf-parse');

async function checkPDF(file) {
    const t0 = performance.now();
    try {
        const fileExtension = file.split('.').pop();
        if (fileExtension === file) {
            console.log("Please put extension in this file.");
            return;
        }
        const dataBuffer = fs.readFileSync(file);
        const { numpages, info } = await pdfParse(dataBuffer);
        const t1 = performance.now();
        console.log("Number of pages:", numpages);
        console.log("Info:", info);
        console.log("Time taken to read metadata:", (t1 - t0), "milliseconds");
    } catch (error) {
        console.error("Error reading PDF:", error);
    }
}

// Example usage:
const file = 'example_file'; // Path to your file
checkPDF(file);
