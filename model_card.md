# Model Card — Game Glitch Investigator: Applied AI System

## Model Details

- **Model used:** claude-haiku-4-5 (Anthropic)
- **Access method:** Anthropic Python SDK via REST API
- **Task:** Context-aware hint generation for a number guessing game
- **Input:** Player guess history, number range, last guess outcome (Too High / Too Low)
- **Output:** One sentence of directional guidance for the player's next guess

---

## AI Collaboration

### Helpful instance
Claude Code suggested wrapping the `get_ai_hint()` call in a `try/except` block inside `app.py` so the game never crashes if the API key is missing or the network is unavailable. This was the right design decision — it made the AI feature a genuine enhancement rather than a hard dependency, and meant the game remained fully playable without any API access.

### Flawed instance
When setting up the test file, the initial approach imported functions directly from `app.py`. Because `app.py` runs Streamlit UI code at the module level, this caused the test suite to fail at import time. The AI did not flag this risk upfront — it only surfaced after the error appeared. A better suggestion would have been to isolate all testable logic in `logic_utils.py` and `ai_hint.py` from the start, keeping `app.py` untestable by design.

---

## Intended Use

This model is used to generate short, encouraging hints for players of a number guessing game. It is intended to make the game more engaging by providing context-aware feedback rather than static "Too High / Too Low" messages.

---

## Limitations and Biases

- **Stateless:** The model has no memory between turns. Each call is independent, so Claude cannot notice patterns like "this player always guesses too high first" or adjust its tone over time.
- **Language:** Hints are generated only in English. Non-English speakers receive no benefit from the AI feature.
- **Directional consistency:** The model is instructed to always say "lower" for Too High and "higher" for Too Low, but without live testing, there is a small risk the model occasionally phrases a hint in a way that omits the direction word — which the reliability tests are designed to catch.
- **Input scope:** The system only passes guess history and outcome to the model. It does not pass the actual secret number, so Claude cannot calculate exact distance or give mathematically precise hints.

---

## Potential Misuse

The hint engine sends player guess history to an external API. A malicious actor could craft unusual guess histories to attempt to confuse the model. This is mitigated by:
- Input validation in `parse_guess()` — only valid integers reach the AI
- The fallback system — a bad or missing response defaults to the static hint
- The short, constrained prompt — the model has little surface area to be manipulated

---

## Testing and Reliability Results

| Test | Result |
|---|---|
| Hint says "lower" when Too High (5 runs) | 100% consistent |
| Hint says "higher" when Too Low (5 runs) | 100% consistent |
| Hint returns non-empty string | Pass |
| Game falls back gracefully on API failure | Pass |
| All game logic tests (9 tests) | Pass |
| **Total** | **13/13 passed** |

The reliability tests use mocked API responses to verify directional consistency without requiring live API access. This makes the test suite fast, deterministic, and runnable in any environment.

---

## Reflection

This project taught me that integrating AI into an existing system is less about the API call and more about the surrounding design — fallbacks, testing, and constraints. The most valuable part was writing reliability tests that define exactly what "consistent AI behavior" means in measurable terms, rather than assuming the model will always do the right thing.
