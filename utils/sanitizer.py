import os
import fitz  # PyMuPDF
from typing import Dict, List

from config.settings import settings

def sanitize_vault() -> Dict[str, List[str]]:
    """
    Scans the data directory for PDFs and categorizes them by readability.
    Identifies files that require OCR preprocessing for the AI to ingest them.
    
    Returns:
        Dict containing lists of 'clean', 'scanned_image', and 'corrupted' filenames.
    """
    print("🔍 Starting Data Sanitization...")
    report: Dict[str, List[str]] = {"clean": [], "scanned_image": [], "corrupted": []}

    for root, _, files in os.walk(settings.data_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                f_path = os.path.join(root, file)
                try:
                    doc = fitz.open(f_path)
                    text_found = False
                    for page in doc:
                        if page.get_text().strip():
                            text_found = True
                            break

                    if text_found:
                        report["clean"].append(file)
                    else:
                        report["scanned_image"].append(file)
                    doc.close()
                except Exception:
                    # Catching Exception specifically prevents catching SystemExit/KeyboardInterrupt
                    report["corrupted"].append(file)

    print("\n--- SANITIZATION REPORT ---")
    print(f"✅ Readable: {len(report['clean'])}")
    print(f"🚨 Scanned (Needs OCR): {len(report['scanned_image'])}")
    print(f"❌ Corrupted: {len(report['corrupted'])}")

    if report["scanned_image"]:
        print("\nAction Required: The following files are images and cannot be read by AI without OCR:")
        for f in report["scanned_image"]: 
            print(f" - {f}")
            
    return report

if __name__ == "__main__":
    # Ensure environment is initialized if run as a standalone script
    settings.initialize_environment()
    sanitize_vault()