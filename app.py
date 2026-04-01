import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from src.pipeline.rag_pipeline import RAGPipeline

# Page config
st.set_page_config(
    page_title="India Schemes RAG",
    page_icon="🇮🇳",
    layout="centered"
)

# Header
st.title("🇮🇳 India Government Schemes Assistant")
st.markdown("Ask me anything about Indian government schemes, scholarships, and welfare programs.")
st.divider()

# Initialize RAG pipeline (only once)
@st.cache_resource
def load_pipeline():
    return RAGPipeline()

with st.spinner("🚀 Loading RAG Pipeline..."):
    rag = load_pipeline()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about any Indian government scheme..."):

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching schemes..."):
            result = rag.ask(prompt)

        # Display answer
        st.markdown(result["answer"])

        # Display sources
        if result["sources"]:
            with st.expander("📚 Sources"):
                for source in result["sources"]:
                    st.markdown(f"- `{source}`")

        # Add assistant message to history
        full_response = result["answer"] + f"\n\n📚 **Sources:** {', '.join(result['sources'])}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

# Sidebar
with st.sidebar:
    st.markdown("## 💡 Example Questions")
    st.markdown("""
    - What schemes are available for farmers?
    - What scholarships exist for SC/ST students?
    - What documents are required for PM-KISAN?
    - What welfare programs are there for disabled persons?
    - What schemes are available for women in rural areas?
    - What schemes exist for senior citizens?
    """)

    st.divider()

    st.markdown("## ℹ️ About")
    st.markdown("""
    This assistant uses **RAG (Retrieval Augmented Generation)** to answer questions about 2000+ Indian government schemes.
    
    **Powered by:**
    - 🤗 HuggingFace Embeddings
    - 🗄️ ChromaDB Vector Database  
    - ⚡ Groq LLM (Llama 3)
    """)

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()