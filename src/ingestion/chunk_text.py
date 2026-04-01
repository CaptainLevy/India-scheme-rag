import os 
import json
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import PROCESSED_DATA_PATH, CHUNKS_DATA_PATH, CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text():
    """Split all extracted text files into chunks"""

    # Get all .txt files
    txt_files = [
        f for f in os.listdir(PROCESSED_DATA_PATH)
        if f.endswith(".txt")
    ]

    print(f"📄 Found {len(txt_files)} text files to chunk.")

    # Set up the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Create ouput directory
    os.makedirs(CHUNKS_DATA_PATH, exist_ok=True)

    all_chunks = []
    total_chunks = 0

    for txt_file in tqdm(txt_files, desc="Chunking files"):
        # Read the text file
        file_path = os.path.join(PROCESSED_DATA_PATH, txt_file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Get scheme name from filename
        scheme_name = os.path.splitext(txt_file)[0]

        # Split into chunks
        chunks = splitter.split_text(text)

        # Store each chunk with metadata
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "scheme_name": scheme_name,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "text": chunk,
                "source": f"data/raw/text_data/{scheme_name}.pdf"
            })

        total_chunks += len(chunks)

    # Save all chunks as one JSON file
    output_path = os.path.join(CHUNKS_DATA_PATH, "all_chunks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Total chunks created: {total_chunks}")
    print(f"📊 Average chunks per scheme: {total_chunks // len(txt_files)}")
    print(f"📂 All chunks saved to: {output_path}")

if __name__ == "__main__":
    chunk_text()