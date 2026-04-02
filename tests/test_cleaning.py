"""Tests for text cleaning functions."""

import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion.clean_text import clean_text


class TestCleanText:
    """Test individual cleaning functions."""

    def test_removes_eng_english(self):
        """Verify EngEnglish artifact is removed."""
        text = "EngEnglish/ Some scheme details here."
        cleaned = clean_text(text)
        assert "EngEnglish" not in cleaned

    def test_removes_sign_in(self):
        """Verify Sign In UI text is removed."""
        text = "Sign In Cancel Ok Some real content here."
        cleaned = clean_text(text)
        assert "Sign In" not in cleaned

    def test_removes_cancel_ok(self):
        """Verify Cancel Ok noise is removed."""
        text = "Cancel Ok You need to before applying for schemes Cancel"
        cleaned = clean_text(text)
        assert "Cancel Ok" not in cleaned

    def test_preserves_scheme_name(self, sample_noisy_text):
        """Verify scheme name is preserved after cleaning."""
        cleaned = clean_text(sample_noisy_text)
        assert "National Agriculture Insurance Scheme" in cleaned

    def test_preserves_eligibility(self, sample_noisy_text):
        """Verify eligibility content is preserved."""
        cleaned = clean_text(sample_noisy_text)
        assert "Eligibility" in cleaned

    def test_preserves_documents(self, sample_noisy_text):
        """Verify documents required content is preserved."""
        cleaned = clean_text(sample_noisy_text)
        assert "Documents Required" in cleaned

    def test_removes_broken_encoding(self):
        """Verify broken Hindi encoding is removed."""
        text = "à¤¹à¤¿à¤‚à¤¦à¥€ Some real content here."
        cleaned = clean_text(text)
        assert "à¤¹" not in cleaned

    def test_cleans_extra_whitespace(self):
        """Verify multiple spaces are collapsed."""
        text = "Some    scheme    with    extra    spaces."
        cleaned = clean_text(text)
        assert "  " not in cleaned

    def test_empty_text_handled(self):
        """Verify empty text doesn't crash."""
        cleaned = clean_text("")
        assert cleaned == ""

    def test_clean_text_unchanged(self, sample_clean_text):
        """Verify already clean text is not corrupted."""
        cleaned = clean_text(sample_clean_text)
        assert "insurance coverage" in cleaned
        assert "Eligibility" in cleaned
        assert "Documents Required" in cleaned

    def test_removes_sign_out(self):
        """Verify Sign Out UI text is removed."""
        text = "Are you sure you want to sign out? Cancel Sign Out Real content."
        cleaned = clean_text(text)
        assert "sign out" not in cleaned.lower()

    def test_removes_something_went_wrong(self):
        """Verify error message noise is removed."""
        text = "Something went wrong. Please try again later. Real content."
        cleaned = clean_text(text)
        assert "Something went wrong" not in cleaned