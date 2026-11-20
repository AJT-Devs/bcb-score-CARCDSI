import unittest
from unittest.mock import patch

from services.ia.briefing import generate_briefing
from services.ia.client import LLMResponse


class CustomClient:
    def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse("custom", prompt, {"source": "custom"})


class BriefingTests(unittest.TestCase):
    def test_custom_client_receives_metrics_and_preserves_response(self):
        result = generate_briefing({"mae": 0.03}, client=CustomClient())
        self.assertEqual(result.provider, "custom")
        self.assertIn("0.03", result.text)
        self.assertEqual(result.raw, {"source": "custom"})

    def test_unknown_provider_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_briefing({}, provider="unknown")

    def test_existing_provider_still_uses_its_client(self):
        response = LLMResponse("nvidia", "resultado", {})
        with patch("services.ia.briefing.NVIDIAClient") as client:
            client.return_value.generate.return_value = response
            self.assertEqual(generate_briefing({}, provider="nvidia"), response)


if __name__ == "__main__":
    unittest.main()
