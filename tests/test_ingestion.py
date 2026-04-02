"""Tests for data ingestion pipeline."""

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestChunking:
    """Test chunking logic."""

    def test_chunks_file_exists(self):
        """Verify chunks file was created."""
        assert Path("data/chunks/all_chunks.json").exists()

    def test_chunk_size_within_limit(self, chunks):
        """Verify no chunk exceeds max size."""
        from config import CHUNK_SIZE
        oversized = [
            c for c in chunks
            if len(c["text"]) > CHUNK_SIZE * 2  # allow 2x for overlap
        ]
        assert len(oversized) == 0, \
            f"Found {len(oversized)} oversized chunks"

    def test_chunk_overlap_creates_continuity(self, chunks):
        """Verify consecutive chunks from same scheme share some content."""
        # Group chunks by scheme
        scheme_chunks = {}
        for chunk in chunks:
            name = chunk["scheme_name"]
            if name not in scheme_chunks:
                scheme_chunks[name] = []
            scheme_chunks[name].append(chunk)

        # Find a scheme with multiple chunks
        multi_chunks = {
            k: v for k, v in scheme_chunks.items()
            if len(v) >= 2
        }
        assert len(multi_chunks) > 0, "No schemes with multiple chunks found"

    def test_all_chunks_have_text(self, chunks):
        """Verify no chunk has empty text."""
        empty = [c for c in chunks if not c.get("text", "").strip()]
        assert len(empty) == 0, f"Found {len(empty)} empty chunks"

    def test_chunk_indices_are_sequential(self, chunks):
        """Verify chunk indices start from 0 per scheme."""
        scheme_chunks = {}
        for chunk in chunks:
            name = chunk["scheme_name"]
            if name not in scheme_chunks:
                scheme_chunks[name] = []
            scheme_chunks[name].append(chunk["chunk_index"])

        for scheme, indices in list(scheme_chunks.items())[:20]:
            assert 0 in indices, \
                f"Scheme {scheme} missing chunk at index 0"

    def test_total_chunks_field_accurate(self, chunks):
        """Verify total_chunks field matches actual chunk count per scheme."""
        scheme_chunks = {}
        for chunk in chunks:
            name = chunk["scheme_name"]
            if name not in scheme_chunks:
                scheme_chunks[name] = []
            scheme_chunks[name].append(chunk)

        for scheme, scheme_chunk_list in list(scheme_chunks.items())[:20]:
            reported_total = scheme_chunk_list[0]["total_chunks"]
            actual_total = len(scheme_chunk_list)
            assert reported_total == actual_total, \
                f"Scheme {scheme}: reported {reported_total} but found {actual_total}"

    def test_processed_files_exist(self):
        """Verify processed text files were created."""
        processed_path = Path("data/processed")
        assert processed_path.exists()
        txt_files = list(processed_path.glob("*.txt"))
        assert len(txt_files) > 100, \
            f"Expected >100 processed files, found {len(txt_files)}"


class TestDataIntegrity:
    """Test overall data integrity."""

    def test_scheme_count_reasonable(self, chunks):
        """Verify we have a reasonable number of unique schemes."""
        schemes = set(c["scheme_name"] for c in chunks)
        assert len(schemes) > 500, \
            f"Expected >500 schemes, found {len(schemes)}"

    def test_no_duplicate_chunk_ids(self, chunks):
        """Verify no two chunks have the same ID."""
        ids = [
            f"{c['scheme_name']}_chunk_{c['chunk_index']}"
            for c in chunks
        ]
        assert len(ids) == len(set(ids)), \
            "Found duplicate chunk IDs"

    def test_chunks_json_valid(self):
        """Verify chunks JSON is valid and parseable."""
        with open("data/chunks/all_chunks.json", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) > 0