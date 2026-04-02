"""Tests for retrieval quality."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestRetrieverQuality:
    """Test retrieval quality and relevance."""

    def test_farmer_query_returns_farm_schemes(self, retriever):
        """Verify farmer query returns agriculture related schemes."""
        results = retriever.retrieve("schemes for farmers", n_results=5)
        assert len(results) > 0

        # At least one result should be farm related
        texts = " ".join([r["text"].lower() for r in results])
        farm_keywords = ["farmer", "agriculture", "crop", "kisan", "farm"]
        assert any(kw in texts for kw in farm_keywords), \
            "No farm-related content in results"

    def test_scholarship_query_returns_scholarships(self, retriever):
        """Verify scholarship query returns scholarship schemes."""
        results = retriever.retrieve("scholarships for students", n_results=5)
        assert len(results) > 0

        texts = " ".join([r["text"].lower() for r in results])
        edu_keywords = ["scholarship", "student", "education", "stipend"]
        assert any(kw in texts for kw in edu_keywords), \
            "No scholarship-related content in results"

    def test_women_query_returns_women_schemes(self, retriever):
        """Verify women query returns women-focused schemes."""
        results = retriever.retrieve("schemes for women", n_results=5)
        assert len(results) > 0

        texts = " ".join([r["text"].lower() for r in results])
        women_keywords = ["women", "woman", "female", "mahila", "girl"]
        assert any(kw in texts for kw in women_keywords), \
            "No women-related content in results"

    def test_different_queries_return_different_results(self, retriever):
        """Verify different queries return different results."""
        results1 = retriever.retrieve("farmer schemes", n_results=3)
        results2 = retriever.retrieve("scholarships for students", n_results=3)

        schemes1 = set(r["scheme_name"] for r in results1)
        schemes2 = set(r["scheme_name"] for r in results2)

        # Results should not be identical
        assert schemes1 != schemes2, \
            "Different queries returned identical results"

    def test_retriever_handles_long_query(self, retriever):
        """Verify retriever handles long queries gracefully."""
        long_query = "What are all the government schemes available for poor farmers living in rural areas of India who belong to scheduled caste and scheduled tribe communities?"
        results = retriever.retrieve(long_query, n_results=5)
        assert len(results) > 0

    def test_retriever_handles_short_query(self, retriever):
        """Verify retriever handles very short queries."""
        results = retriever.retrieve("farmer", n_results=3)
        assert len(results) > 0

    def test_all_results_have_required_fields(self, retriever):
        """Verify all results have required fields."""
        results = retriever.retrieve("government schemes India", n_results=5)
        for result in results:
            assert "text" in result
            assert "scheme_name" in result
            assert "source" in result
            assert len(result["text"]) > 0
            assert len(result["scheme_name"]) > 0

    def test_n_results_respected(self, retriever):
        """Verify n_results parameter is respected."""
        for n in [1, 3, 5]:
            results = retriever.retrieve("schemes", n_results=n)
            assert len(results) <= n, \
                f"Expected <={n} results, got {len(results)}"