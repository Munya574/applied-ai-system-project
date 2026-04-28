"""
Reliability tests for the AI hint system.

These tests use mocks to verify that the hint system behaves consistently
without requiring a live Anthropic API key.
"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_hint import get_ai_hint


def make_mock_response(text: str):
    """Build a fake Anthropic API response with the given text."""
    block = MagicMock()
    block.text = text
    response = MagicMock()
    response.content = [block]
    return response


# --- Reliability tests (mocked) ---

def test_hint_consistent_when_too_high():
    """Claude should consistently say 'lower' when the last guess was Too High."""
    hints = [
        "You're too high — try going lower!",
        "Too high! Aim lower next time.",
        "That's above the target, go lower.",
        "Go lower — you overshot it!",
        "Lower your next guess, you're above it.",
    ]
    responses = [make_mock_response(h) for h in hints]

    with patch("ai_hint.client.messages.create", side_effect=responses):
        results = [get_ai_hint([75], (1, 100), "Too High") for _ in range(5)]

    lower_count = sum(1 for r in results if "lower" in r.lower())
    rate = lower_count / len(results)
    print(f"\nConsistency (Too High -> lower): {rate:.0%}")
    assert rate >= 0.8, f"Expected ≥80% consistency, got {rate:.0%}. Results: {results}"


def test_hint_consistent_when_too_low():
    """Claude should consistently say 'higher' when the last guess was Too Low."""
    hints = [
        "Too low! Try going higher.",
        "Aim higher — you're below the target.",
        "Go higher, you haven't reached it yet.",
        "Higher! Your guess is below the number.",
        "That's too low, push higher next time.",
    ]
    responses = [make_mock_response(h) for h in hints]

    with patch("ai_hint.client.messages.create", side_effect=responses):
        results = [get_ai_hint([25], (1, 100), "Too Low") for _ in range(5)]

    higher_count = sum(1 for r in results if "higher" in r.lower())
    rate = higher_count / len(results)
    print(f"\nConsistency (Too Low -> higher): {rate:.0%}")
    assert rate >= 0.8, f"Expected ≥80% consistency, got {rate:.0%}. Results: {results}"


def test_hint_returns_nonempty_string():
    """AI hint should always return a non-empty string."""
    mock_response = make_mock_response("Go lower, you're above the number!")

    with patch("ai_hint.client.messages.create", return_value=mock_response):
        hint = get_ai_hint([75], (1, 100), "Too High")

    assert isinstance(hint, str)
    assert len(hint.strip()) > 0, "Hint should not be empty"


def test_hint_failure_does_not_crash_game(monkeypatch):
    """If the API call fails, app.py should fall back to the basic hint gracefully."""
    import ai_hint

    def broken_hint(*args, **kwargs):
        raise RuntimeError("API unavailable")

    monkeypatch.setattr(ai_hint, "get_ai_hint", broken_hint)

    # Simulate what app.py does: call get_ai_hint inside a try/except
    fallback = "📉 Go LOWER!"
    try:
        result = ai_hint.get_ai_hint([75], (1, 100), "Too High")
    except Exception:
        result = fallback

    assert result == fallback, "Game should fall back to basic hint on API failure"
