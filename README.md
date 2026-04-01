# 🇮🇳 India Schemes RAG

A Retrieval-Augmented Generation (RAG) system that answers questions about Indian Government schemes, scholarships, and welfare programs for citizens across all age groups, income levels, and regions (rural & urban).

---

## 🎯 What It Does

Ask questions like:
- *"What schemes are available for farmers?"*
- *"What scholarships exist for SC/ST students?"*
- *"What documents are required for PM-KISAN?"*
- *"What welfare programs are available for disabled persons?"*
- *"What schemes are available for women in rural areas?"*

And get accurate, source-backed answers instantly.

---

## 🏗️ Tech Stack

| Component | Tool |
|---|---|
| **Data** | [shrijayan/gov_myscheme](https://huggingface.co/datasets/shrijayan/gov_myscheme) — 2000+ Indian govt scheme PDFs |
| **PDF Extraction** | PyMuPDF (fitz) |
| **Text Chunking** | LangChain RecursiveCharacterTextSplitter |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 (local, free) |
| **Vector Database** | ChromaDB (local, free) |
| **LLM** | Groq — Llama 3 8B (free tier) |
| **Framework** | LangChain |

---

## 📁 Project Structure
```
india-schemes-rag/
├── data/
│   ├── raw/          ← downloaded PDFs (auto-generated)
│   ├── processed/    ← extracted text (auto-generated)
│   ├── chunks/       ← chunked data (auto-generated)
│   └── chroma_db/    ← vector database (auto-generated)
├── src/
│   ├── ingestion/
│   │   ├── download_data.py    ← downloads dataset from HuggingFace
│   │   ├── extract_text.py     ← extracts text from PDFs
│   │   ├── clean_text.py       ← removes UI noise from text
│   │   └── chunk_text.py       ← splits text into chunks
│   ├── embedding/
│   │   └── embed_and_store.py  ← generates embeddings & stores in ChromaDB
│   ├── retrieval/
│   │   └── retriever.py        ← searches ChromaDB for relevant chunks
│   └── pipeline/
│       └── rag_pipeline.py     ← connects retriever + Groq LLM
├── notebooks/                  ← Jupyter notebooks for experiments
├── tests/                      ← unit tests
├── config.py                   ← all settings and configuration
├── requirements.txt            ← all dependencies
└── .env                        ← API keys (never commit this!)
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Mac / Linux / Windows
- Free accounts on [HuggingFace](https://huggingface.co/join) and [Groq](https://console.groq.com)

### 2. Clone the repo
```bash
git clone https://github.com/CaptainLevy/India-scheme-rag.git
cd India-scheme-rag
```

### 3. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up API keys
Create a `.env` file in the root directory:
```
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

Get your free keys here:
- HuggingFace token → [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Groq API key → [console.groq.com](https://console.groq.com)

---

## 🚀 Run the Pipeline

Run these scripts in order to build the knowledge base:
```bash
# Step 1 — Download 2000+ scheme PDFs from HuggingFace
python3 src/ingestion/download_data.py

# Step 2 — Extract text from all PDFs
python3 src/ingestion/extract_text.py

# Step 3 — Clean noise from extracted text
python3 src/ingestion/clean_text.py

# Step 4 — Split text into chunks
python3 src/ingestion/chunk_text.py

# Step 5 — Generate embeddings and store in ChromaDB
python3 src/embedding/embed_and_store.py
```

> ⏱️ Total setup time: ~15-20 minutes (mostly downloading & embedding)

---

## 💬 Ask Questions
```bash
python3 src/pipeline/rag_pipeline.py
```

### Example Output
```
❓ Question: What schemes are available for farmers?

💬 Answer: Several schemes are available for farmers in India:

1. PM-KISAN — Provides ₹6000/year to small and marginal farmers
2. NAIS (National Agriculture Insurance Scheme) — Covers crop loss due to 
   natural calamities for Kharif and Rabi crops
3. Krishak Durghatna Kalyan Yojana — Accident insurance for farmers in UP

📚 Sources: nais, kdky, pmkisan
```

---

## 📊 Dataset Stats

| Metric | Value |
|---|---|
| Total PDFs | 2,153 |
| Total chunks | ~52,000 |
| Avg chunks per scheme | 23 |
| Vector dimensions | 384 |
| Embedding model | all-MiniLM-L6-v2 |

---

## 🗺️ Roadmap

- [x] Data collection & PDF extraction
- [x] Text cleaning & chunking
- [x] Embeddings & vector database
- [x] RAG pipeline with Groq
- [ ] Web UI (Streamlit)
- [ ] Deploy to Hugging Face Spaces
- [ ] Add Hindi language support
- [ ] Filter by state, category, beneficiary type

---

## 🙏 Acknowledgements

- [MyScheme Portal](https://myscheme.gov.in) — Government of India
- [shrijayan/gov_myscheme](https://huggingface.co/datasets/shrijayan/gov_myscheme) — Dataset
- [Groq](https://groq.com) — Free LLM inference
- [ChromaDB](https://chromadb.com) — Vector database
- [sentence-transformers](https://sbert.net) — Embeddings

---

## 📄 License

MIT License — free to use, modify and distribute.