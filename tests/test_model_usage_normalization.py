import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.model_usage_normalization import (  # noqa: E402
    normalize_anthropic_usage,
    normalize_copilot_footer_usage,
    normalize_gemini_usage,
    normalize_openai_usage,
    normalize_provider_usage,
)


class ModelUsageNormalizationTests(unittest.TestCase):
    def test_openai_responses_usage_normalizes_as_exact_provider_usage(self):
        usage = normalize_openai_usage(
            {
                "input_tokens": 100,
                "output_tokens": 25,
                "total_tokens": 125,
                "input_tokens_details": {"cached_tokens": 40},
                "output_tokens_details": {"reasoning_tokens": 5},
            }
        )

        self.assertEqual(
            usage,
            {
                "usage_source": "provider",
                "usage_precision": "exact",
                "token_input": 100,
                "token_output": 25,
                "token_total": 125,
                "token_cache_read_input": 40,
                "token_cache_write_input": 0,
                "token_reasoning_output": 5,
            },
        )

    def test_anthropic_messages_usage_normalizes_as_exact_provider_usage(self):
        usage = normalize_anthropic_usage(
            {
                "input_tokens": 80,
                "output_tokens": 20,
                "cache_read_input_tokens": 30,
                "cache_creation_input_tokens": 10,
            }
        )

        self.assertEqual(
            usage,
            {
                "usage_source": "provider",
                "usage_precision": "exact",
                "token_input": 80,
                "token_output": 20,
                "token_total": 100,
                "token_cache_read_input": 30,
                "token_cache_write_input": 10,
            },
        )

    def test_gemini_usage_metadata_normalizes_as_exact_provider_usage(self):
        usage = normalize_gemini_usage(
            {
                "usageMetadata": {
                    "promptTokenCount": 60,
                    "candidatesTokenCount": 15,
                    "thoughtsTokenCount": 5,
                    "totalTokenCount": 80,
                    "cachedContentTokenCount": 12,
                }
            }
        )

        self.assertEqual(
            usage,
            {
                "usage_source": "provider",
                "usage_precision": "exact",
                "token_input": 60,
                "token_output": 20,
                "token_total": 80,
                "token_cache_read_input": 12,
                "token_cache_write_input": 0,
                "token_reasoning_output": 5,
            },
        )

    def test_copilot_footer_stays_runner_estimated_usage(self):
        output = "\n".join(
            [
                "## TDD Plan",
                "",
                "Total usage est:       1 Premium request",
                "Total duration (API):  3.6s",
                "Usage by model:",
                "    Claude Sonnet 4.5    7.0k input, 4 output, 12 cache read, 3 cache write (Est. 1 Premium request)",
            ]
        )

        self.assertEqual(
            normalize_copilot_footer_usage(output),
            {
                "usage_source": "runner",
                "usage_precision": "estimated",
                "token_input": 7000,
                "token_output": 4,
                "token_total": 7004,
                "token_cache_read_input": 12,
                "token_cache_write_input": 3,
                "model_name": "Claude Sonnet 4.5",
            },
        )

    def test_invalid_payloads_do_not_normalize_as_exact(self):
        invalid_payloads = [
            ("openai", {"input_tokens": 10, "output_tokens": 2}),
            ("openai", {"input_tokens": 10, "output_tokens": "2", "total_tokens": 12}),
            ("openai", {"input_tokens": 10, "output_tokens": 2, "total_tokens": 13}),
            ("anthropic", {"input_tokens": 10, "output_tokens": -1}),
            ("gemini", {"promptTokenCount": 10, "candidatesTokenCount": 2, "totalTokenCount": 13}),
        ]

        for provider, payload in invalid_payloads:
            with self.subTest(provider=provider, payload=payload):
                self.assertIsNone(normalize_provider_usage(provider, payload))


if __name__ == "__main__":
    unittest.main()
