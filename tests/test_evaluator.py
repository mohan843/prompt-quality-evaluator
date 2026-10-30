import unittest

from evaluator import compare, evaluate, has_any, words


class EvaluatorTests(unittest.TestCase):
    def test_word_extraction(self):
        self.assertEqual(words("Hello, AI-world!"), ["hello", "ai", "world"])

    def test_phrase_matching(self):
        self.assertTrue(has_any("Return JSON output", ("json", "table")))
        self.assertFalse(has_any("Write clearly", ("json", "table")))

    def test_basic_prompt_scores_lower(self):
        report = evaluate("Summarize this article.")
        self.assertLess(report.score, 40)
        self.assertIn("Add context.", report.suggestions)

    def test_detailed_prompt_scores_excellent(self):
        prompt = "You are a senior data analyst. Given the sales context, explain changes for a manager. Return a markdown table with metric and evidence. Use only supplied data, keep it under 200 words, and show one example row."
        report = evaluate(prompt)
        self.assertGreaterEqual(report.score, 80)
        self.assertEqual(report.label, "excellent")
        self.assertFalse(report.suggestions)

    def test_compare_preserves_order(self):
        reports = compare(["Summarize this.", "Return JSON with examples and context for a developer."])
        self.assertEqual(len(reports), 2)
        self.assertLess(reports[0].score, reports[1].score)

    def test_empty_prompt_rejected(self):
        with self.assertRaises(ValueError):
            evaluate("   ")


if __name__ == "__main__":
    unittest.main()
