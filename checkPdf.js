
function isPdf(fileName) {
    return /\.pdf$/i.test(fileName);
}

// Example usage
console.log(isPdf("document.pdf")); // Output: true
console.log(isPdf("presentation.PDF")); // Output: true
console.log(isPdf("report.docx")); // Output: false

// Exporting the function for use in other modules (optional)
module.exports = isPdf;
