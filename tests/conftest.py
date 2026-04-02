"""Shared fixtures for all tests."""

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="session")
def chunks():
    """Load all chunks from disk once per session."""
    chunks_path = Path("data/chunks/all_chunks.json")
    assert chunks_path.exists(), "chunks/all_chunks.json not found"
    with open(chunks_path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def retriever():
    """Initialize retriever once per session."""
    from src.retrieval.retriever import SchemeRetriever
    return SchemeRetriever()


@pytest.fixture(scope="session")
def rag_pipeline():
    """Initialize RAG pipeline once per session."""
    from dotenv import load_dotenv
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        pytest.skip("GROQ_API_KEY not set")
    from src.pipeline.rag_pipeline import RAGPipeline
    return RAGPipeline()


@pytest.fixture
def sample_noisy_text():
    """Sample text with portal UI noise."""
    return """National Agriculture Insurance Scheme EngEnglish/
    OkYou need to before applying for schemesCancelSign In Gujarat
    National Agriculture Insurance SchemeAgricultureFarmerFinancial
    The scheme provides insurance coverage to farmers in the event
    of failure of notified crops due to natural calamities.
    Eligibility: All farmers including sharecroppers and tenant farmers.
    Documents Required: Aadhaar Card, Bank Account Details, Land Records."""


@pytest.fixture
def sample_clean_text():
    """Sample clean scheme text."""
    return """The scheme provides insurance coverage to farmers in the event
    of failure of notified crops due to natural calamities.
    Eligibility: All farmers including sharecroppers and tenant farmers.
    Documents Required: Aadhaar Card, Bank Account Details, Land Records.
    Benefits: Financial support up to 100% of sum insured."""


@pytest.fixture
def sample_chunk():
    """A single valid chunk."""
    return {
        "scheme_name": "test_scheme",
        "chunk_index": 0,
        "total_chunks": 3,
        "text": "This is a test scheme for farmers in India providing financial support.",
        "source": "data/raw/text_data/test_scheme.pdf"
    }