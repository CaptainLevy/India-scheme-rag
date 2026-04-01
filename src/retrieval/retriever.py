import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL

class SchemeRetriever:
    def __init__(self):
        print("🔍 Loading retriever...")
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.client.get_collection(CHROMA_COLLECTION_NAME)
        print("✅ Retriever ready!")

    def retrieve(self, query, n_results=5):
        """Retrieve top n relevant chunks for a query."""

        # Convert query to embedding
        query_embedding = self.model.encode(query).tolist()

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        chunks = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            chunks.append({
                "text": doc,
                "scheme_name": meta["scheme_name"],
                "source": meta["source"]
            })

        return chunks