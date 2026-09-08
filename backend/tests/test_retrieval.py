import unittest

from app.corpus import DOCUMENTS
from app.rag import answer_question, retrieve_briefing
from app.retrieval import retrieve


class RetrievalTests(unittest.TestCase):
    def test_retrieves_agent_workflow_document(self):
        matches = retrieve("python agent workflow retries checkpoints", DOCUMENTS)
        self.assertEqual(matches[0]["id"], "github-agent-checkpoints")

    def test_grounded_answer_contains_sources(self):
        result = answer_question({"topics": ["RAG", "vector search"]}, "How can I evaluate retrieval?")
        self.assertTrue(result["sources"])
        self.assertIn("retrieved technical sources", result["answer"])

    def test_briefing_has_explanations(self):
        result = retrieve_briefing({"topics": ["Python", "RAG"]})
        self.assertTrue(result["signals"])
        self.assertTrue(all(signal["why"] for signal in result["signals"]))


if __name__ == "__main__":
    unittest.main()
