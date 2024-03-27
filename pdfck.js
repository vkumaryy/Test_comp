function checkPdfIntegrity(pdfFile) {
    if (!pdfFile || !pdfFile.type) {
      console.error("Error: Invalid PDF file or missing file type.");
      return false;
    }
  
    if (pdfFile.type !== "application/pdf") {
      console.error("Error: File is not a valid PDF.");
      return false;
    }
  
    // Attempt to parse the first few bytes for basic PDF structure (limited check)
    const magicBytes = new Uint8Array(pdfFile.slice(0, 4));
    if (!(magicBytes[0] === 0x25 && magicBytes[1] === 0x50 && magicBytes[2] === 0x44 && magicBytes[3] === 0x46)) {
      console.error("Error: Invalid PDF structure (magic bytes mismatch).");
      return false;
    }
  
    console.log("PDF file appears valid (basic checks passed).");
    return true; // Potential for further integrity checks on server-side
  }
  