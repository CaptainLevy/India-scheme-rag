import os 
import fitz #PyMuPDF
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
        return None
    
def extract_all_pdfs():
    """Extract all text from all PDFs in the raw data folder."""
    
    # Find all PDFs recursively
    pdf_files = []
    for root, dirs, files in os.walk(RAW_DATA_PATH):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    
    print(f"📄 Found {len(pdf_files)} PDF files.")

    # Create output directory
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    success = 0
    failed = 0

    for pdf_path in tqdm(pdf_files, desc="Extracting PDFs"):
        # Get scheme name from filename
        scheme_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Extract text
        text = extract_text_from_pdf(pdf_path)

        if text and len(text) > 5: # skip empty/corruput PDFs
            # Save as .txt file
            output_path = os.path.join(PROCESSED_DATA_PATH, f"{scheme_name}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            success += 1
        else:
            failed += 1

    print(f"\n✅ Successfully extracted: {success} PDFs.")
    print(f"❌ Failed/Empty: {failed} PDFs.")
    print(f"📂 Saved to: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    extract_all_pdfs()
    