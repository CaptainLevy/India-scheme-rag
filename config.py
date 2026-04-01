import os 
from dotenv import load_dotenv

load_dotenv()

#API Keys
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Paths
RAW_DATA_PATH = "./data/raw"
PROCESSED_DATA_PATH = "./data/processed"
CHUNKS_DATA_PATH = "./data/chunks"

#Embedding Model (free, runs locally)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

#Groq LLM
GROQ_MODEL = "llama3-8b-8192"

#Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

#ChromaDB
CHROMA_DB_PATH = "./data/chroma_db"
CHROMA_COLLECTION_NAME = "india_schemes"
