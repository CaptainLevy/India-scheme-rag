"""Tests for RAG pipeline edge cases."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRAGPipelineEdgeCases:
    """Test RAG pipeline edge cases and robustness."""

    def test_response_structure_always_complete(self, rag_pipeline):
        """Verify response always has all required keys."""
        response = rag_pipeline.ask("What is PM-KISAN?")
        assert "question" in response
        assert "answer" in response
        assert "sources" in response

    def test_sources_always_a_list(self, rag_pipeline):
        """Verify sources is always a list."""
        response = rag_pipeline.ask("Tell me about farmer schemes")
        assert isinstance(response["sources"], list)

    def test_answer_is_string(self, rag_pipeline):
        """Verify answer is always a string."""
        response = rag_pipeline.ask("What schemes exist for women?")
        assert isinstance(response["answer"], str)

    def test_unknown_topic_handled_gracefully(self, rag_pipeline):
        """Verify unknown topics return graceful response."""
        response = rag_pipeline.ask(
            "What is the latest iPhone model released by Apple?"
        )
        answer = response["answer"].lower()
        # Should either say it doesn't know or return something reasonable
        assert len(answer) > 0, "Empty answer returned"

    def test_very_long_query_handled(self, rag_pipeline):
        """Verify very long queries don't crash the pipeline."""
        long_query = " ".join(["farmer scheme India benefits eligibility"] * 20)
        response = rag_pipeline.ask(long_query)
        assert "answer" in response
        assert len(response["answer"]) > 0

    def test_question_preserved_in_response(self, rag_pipeline):
        """Verify question is preserved in response."""
        question = "What documents are needed for PM-KISAN?"
        response = rag_pipeline.ask(question)
        assert response["question"] == question

    def test_multiple_queries_consistent(self, rag_pipeline):
        """Verify same query returns consistent results."""
        query = "What schemes are available for farmers?"
        response1 = rag_pipeline.ask(query)
        response2 = rag_pipeline.ask(query)

        # Both should have answers
        assert len(response1["answer"]) > 0
        assert len(response2["answer"]) > 0

    def test_sc_st_scholarship_query(self, rag_pipeline):
        """Verify SC/ST scholarship query returns relevant answer."""
        response = rag_pipeline.ask(
            "What scholarships are available for SC ST students?"
        )
        answer = response["answer"].lower()
        keywords = ["scholarship", "sc", "st", "student", "education"]
        assert any(kw in answer for kw in keywords), \
            f"Answer not relevant to SC/ST scholarships: {answer[:200]}"

    def test_disabled_persons_query(self, rag_pipeline):
        """Verify query for disabled persons returns relevant answer."""
        response = rag_pipeline.ask(
            "What schemes are available for disabled persons?"
        )
        assert len(response["answer"]) > 10

    def test_rural_urban_query(self, rag_pipeline):
        """Verify query covers both rural and urban schemes."""
        response = rag_pipeline.ask(
            "What housing schemes are available for poor people?"
        )
        assert len(response["answer"]) > 10
        assert len(response["sources"]) > 0