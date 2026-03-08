import os
import fitz  # PyMuPDF

DATA_DIR = "data_in"


def sanitize_vault():
    print("🔍 Starting Data Sanitization...")
    report = {"clean": [], "scanned_image": [], "corrupted": []}

    for root, _, files in os.walk(DATA_DIR):
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
                except:
                    report["corrupted"].append(file)

    print("\n--- SANITIZATION REPORT ---")
    print(f"✅ Readable: {len(report['clean'])}")
    print(f"🚨 Scanned (Needs OCR): {len(report['scanned_image'])}")
    print(f"❌ Corrupted: {len(report['corrupted'])}")

    if report["scanned_image"]:
        print("\nAction Required: The following files are images and cannot be read by AI without OCR:")
        for f in report["scanned_image"]: print(f" - {f}")


if __name__ == "__main__":
    sanitize_vault()