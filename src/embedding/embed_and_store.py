import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import chromadb
from config import (
    CHUNKS_DATA_PATH,
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL
)

def load_chunks():
    """Load all chunks from JSON file."""
    chunks_path = os.path.join(CHUNKS_DATA_PATH, "all_chunks.json")
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"📦 Loaded {len(chunks)} chunks")
    return chunks

def embed_and_store():
    """Embed all chunks and store in ChromaDB."""

    # Load chunks
    chunks = load_chunks()

    # Load embedding model
    print(f"🤖 Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("✅ Embedding model loaded!")

    # Set up ChromaDB
    print(f"🗄️ Setting up ChromaDB at: {CHROMA_DB_PATH}")
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    # Delete collection if exists (fresh start)
    try:
        client.delete_collection(CHROMA_COLLECTION_NAME)
        print("🗑️ Deleted existing collection")
    except:
        pass

    # Create fresh collection
    collection = client.create_collection(
        name=CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}  # cosine similarity
    )
    print(f"✅ Created collection: {CHROMA_COLLECTION_NAME}")

    # Process in batches (ChromaDB works better in batches)
    BATCH_SIZE = 500
    total_batches = len(chunks) // BATCH_SIZE + 1

    print(f"\n🔢 Embedding and storing {len(chunks)} chunks in batches of {BATCH_SIZE}...")

    for i in tqdm(range(0, len(chunks), BATCH_SIZE), desc="Embedding batches", total=total_batches):
        batch = chunks[i:i + BATCH_SIZE]

        # Extract texts and metadata
        texts = [c["text"] for c in batch]
        ids = [f"{c['scheme_name']}_chunk_{c['chunk_index']}" for c in batch]
        metadatas = [
            {
                "scheme_name": c["scheme_name"],
                "chunk_index": c["chunk_index"],
                "total_chunks": c["total_chunks"],
                "source": c["source"]
            }
            for c in batch
        ]

        # Generate embeddings
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        # Store in ChromaDB
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    print(f"\n✅ Successfully embedded and stored {len(chunks)} chunks!")
    print(f"🗄️ ChromaDB saved at: {CHROMA_DB_PATH}")
    print(f"📊 Collection: {CHROMA_COLLECTION_NAME}")
    print(f"📦 Total vectors: {collection.count()}")

if __name__ == "__main__":
    embed_and_store()