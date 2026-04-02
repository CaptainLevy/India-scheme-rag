#!/bin/bash
set -e

echo "🚀 Starting setup..."

# Run data pipeline only if chroma_db doesn't exist yet
if [ ! -d "data/chroma_db" ]; then
    echo "📥 Downloading dataset..."
    python3 src/ingestion/download_data.py

    echo "📄 Extracting text..."
    python3 src/ingestion/extract_text.py

    echo "🧹 Cleaning text..."
    python3 src/ingestion/clean_text.py

    echo "✂️ Chunking text..."
    python3 src/ingestion/chunk_text.py

    echo "🔢 Embedding and storing..."
    python3 src/embedding/embed_and_store.py
else
    echo "✅ Data already exists, skipping pipeline..."
fi

echo "🌐 Starting Streamlit..."
streamlit run app.py --server.port 8000 --server.address 0.0.0.0