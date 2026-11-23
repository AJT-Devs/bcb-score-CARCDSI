import json
import unittest
from services.ia.briefing import generate_briefing


class BriefingTests(unittest.TestCase):
    def test_local_report_preserves_calculated_metrics(self):
        data = {"mae": 0.03, "alvo": "inadimplência"}
        self.assertEqual(json.loads(generate_briefing(data)), data)
