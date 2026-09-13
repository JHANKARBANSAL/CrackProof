"""
Automated CI/CD test suite for CrackProof RAG & Knowledge Base.
Runs on every GitHub commit to prevent regression.
"""

import os
import json
import unittest


class TestKnowledgeBase(unittest.TestCase):

    def test_chunks_exist_and_valid(self):
        chunks_path = os.path.join("knowledge", "chunks.json")
        self.assertTrue(os.path.exists(chunks_path), "knowledge/chunks.json missing")

        with open(chunks_path) as f:
            chunks = json.load(f)

        self.assertGreater(len(chunks), 1800, "Chunks count too low")

        # Verify chunk structure
        sample = chunks[0]
        required_keys = ["chunk_id", "subject", "title", "section", "source", "text"]
        for key in required_keys:
            self.assertIn(key, sample, f"Missing key {key} in chunk")

    def test_bm25_retrieval(self):
        from retriever_bm25 import BM25Retriever
        retriever = BM25Retriever()
        self.assertGreater(len(retriever.chunks), 1800)

        # Query test
        results = retriever.search("What is the difference between String and StringBuilder?", subject="JAVA", top_k=3)
        self.assertGreater(len(results), 0, "BM25 returned no results for Java String query")
        self.assertEqual(results[0]["subject"], "JAVA")

    def test_grounding_references(self):
        from grounding import get_reference
        text, sources = get_reference("What is the difference between String and StringBuilder?", "JAVA", top_k=3)

        self.assertGreater(len(text), 100, "Reference text should not be empty")
        self.assertGreater(len(sources), 0, "Sources list should not be empty")

        # Verify source metadata
        first_source = sources[0]
        self.assertIn("number", first_source)
        self.assertIn("url", first_source)
        self.assertTrue(first_source["url"].startswith("http"), "Source URL must be valid HTTP/HTTPS")


if __name__ == "__main__":
    unittest.main()
