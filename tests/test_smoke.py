"""Smoke tests for RAG pipeline components.

This suite validates:
1. Retriever returns non-empty results for known queries
2. RAG pipeline produces complete answers with sources for test queries
3. Chunk corpus integrity (count > 0, no empty chunks, valid structure)
"""

import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from dotenv import load_dotenv

load_dotenv()


class TestChunkCorpus:
    """Validate chunk corpus integrity."""

    @pytest.fixture
    def chunks(self):
        """Load all chunks from disk."""
        chunks_path = Path("data/chunks/all_chunks.json")
        assert chunks_path.exists(), "chunks/all_chunks.json not found"
        with open(chunks_path, encoding="utf-8") as f:
            return json.load(f)

    def test_chunk_count_non_zero(self, chunks):
        """Verify chunk corpus is not empty."""
        assert len(chunks) > 0, "No chunks found in corpus"

    def test_no_empty_chunks(self, chunks):
        """Verify all chunks contain text."""
        empty_chunks = [c for c in chunks if not c.get("text", "").strip()]
        assert (
            len(empty_chunks) == 0
        ), f"Found {len(empty_chunks)} empty chunks: {empty_chunks[:3]}"

    def test_chunk_structure_valid(self, chunks):
        """Verify all chunks have required fields."""
        required_fields = {"text", "scheme_name", "chunk_index"}
        for i, chunk in enumerate(chunks[:10]):  # Spot check first 10
            missing = required_fields - set(chunk.keys())
            assert (
                not missing
            ), f"Chunk {i} missing fields: {missing}. Keys: {chunk.keys()}"

    def test_schemes_populated(self, chunks):
        """Verify chunks span multiple schemes."""
        schemes = set(c.get("scheme_name") for c in chunks)
        assert len(schemes) > 100, f"Expected >100 schemes, found {len(schemes)}"


class TestRetriever:
    """Validate retriever component."""

    @pytest.fixture
    def retriever(self):
        """Initialize retriever."""
        pytest.importorskip("chromadb", reason="chromadb not installed")
        from src.retrieval.retriever import SchemeRetriever

        return SchemeRetriever()

    def test_retriever_loads(self, retriever):
        """Verify retriever initializes without error."""
        assert retriever is not None
        assert hasattr(retriever, "retrieve")

    def test_retriever_returns_results_for_known_query(self, retriever):
        """Verify retriever returns non-empty results for a known scheme."""
        results = retriever.retrieve("pm-kisan", n_results=5)
        assert len(results) > 0, "Retriever returned no results for 'pm-kisan'"
        assert all(
            "scheme_name" in r and "text" in r for r in results
        ), "Retrieved chunks missing required fields"

    def test_retriever_result_count(self, retriever):
        """Verify retriever respects n_results parameter."""
        results = retriever.retrieve("agriculture", n_results=3)
        assert (
            len(results) <= 3
        ), f"Expected <=3 results, got {len(results)}"

    def test_retriever_returns_dict_with_text(self, retriever):
        """Verify result structure is correct."""
        results = retriever.retrieve("farmer schemes", n_results=1)
        assert len(results) >= 1
        result = results[0]
        assert isinstance(result, dict)
        assert "text" in result
        assert "scheme_name" in result
        assert len(result["text"]) > 0


class TestRAGPipeline:
    """Validate full RAG pipeline."""

    @pytest.fixture
    def rag_pipeline(self):
        """Initialize RAG pipeline."""
        pytest.importorskip("groq", reason="groq not installed")
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            pytest.skip("GROQ_API_KEY not set")
        from src.pipeline.rag_pipeline import RAGPipeline

        return RAGPipeline()

    def test_rag_pipeline_ask_returns_dict(self, rag_pipeline):
        """Verify RAG pipeline returns structured response."""
        response = rag_pipeline.ask("What is PM-KISAN?")
        assert isinstance(response, dict)
        assert "question" in response
        assert "answer" in response
        assert "sources" in response

    def test_rag_pipeline_answer_non_empty(self, rag_pipeline):
        """Verify RAG pipeline generates non-empty answers."""
        response = rag_pipeline.ask("What schemes are available for farmers?")
        answer = response.get("answer", "").strip()
        assert len(answer) > 10, f"Answer too short: {answer}"

    def test_rag_pipeline_sources_populated(self, rag_pipeline):
        """Verify RAG pipeline includes sources in response."""
        response = rag_pipeline.ask("Tell me about agriculture schemes")
        sources = response.get("sources", [])
        assert len(sources) > 0, "No sources returned in RAG response"

    def test_rag_pipeline_preserves_question(self, rag_pipeline):
        """Verify RAG pipeline echoes back the question."""
        question = "What is the eligibility for PM-KISAN?"
        response = rag_pipeline.ask(question)
        assert "question" in response
        # Question should be present (may be normalized)
        assert len(response["question"]) > 0


if __name__ == "__main__":
    # Run: pytest tests/test_smoke.py -v
    pytest.main([__file__, "-v"])
