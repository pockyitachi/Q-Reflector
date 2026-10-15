import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from summarize_qreflector_teacher_pilot import cost


class CostTests(unittest.TestCase):
    def test_cache_writes_replace_input_rate_and_reasoning_is_already_output(self):
        events = [{'usage': {'input_tokens': 1000, 'input_tokens_details': {
            'cached_tokens': 200, 'cache_write_tokens': 700}, 'output_tokens': 300,
            'output_tokens_details': {'reasoning_tokens': 200}}}]
        result = cost(events, 'test-teacher-b', rates={
            'input': 2, 'cached_input': .1, 'cache_write': 2.5, 'output': 10})
        self.assertAlmostEqual(result['estimated_standard_api_cost_usd'],
                               (100*2 + 200*0.1 + 700*2.5 + 300*10)/1e6)
        self.assertEqual(result['reasoning_tokens'], 200)

    def test_usage_of_failed_or_incomplete_attempts_is_counted(self):
        event = {'event': 'response_received', 'response_status': 'incomplete',
                 'usage': {'input_tokens': 100, 'output_tokens': 100}}
        result = cost([event,event], 'test-teacher-a', rates={
            'input': .1, 'cached_input': .01, 'cache_write': .125, 'output': .5})
        self.assertAlmostEqual(result['estimated_standard_api_cost_usd'], .00012)

    def test_missing_prices_report_usage_without_inventing_a_cost(self):
        result = cost([{'usage': {'input_tokens': 100, 'output_tokens': 20}}], 'custom-model')
        self.assertEqual(result['input_tokens'], 100)
        self.assertIsNone(result['estimated_standard_api_cost_usd'])
        self.assertIsNone(result['pricing_source'])


if __name__ == '__main__':
    unittest.main()
