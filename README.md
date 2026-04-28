# Game Glitch Investigator: Applied AI System

## Demo Walkthrough

[Watch the Loom video walkthrough here](#) ← replace with your Loom link after recording

---

## Original Project

This project extends the **Game Glitch Investigator** from Module 1 — a Streamlit number-guessing game where an AI wrote broken code and the player had to debug it. The original project's goal was to identify and fix logic bugs (wrong hints, broken scoring, incorrect difficulty ranges) by reading code, running tests, and applying fixes using Copilot Agent mode. After all bugs were resolved, the game allowed players to guess a secret number within a difficulty-scaled range using a limited number of attempts.

---

## Title and Summary

**Game Glitch Investigator: Applied AI System**

This system extends the original guessing game by adding an AI-powered hint engine backed by Claude (claude-haiku-4-5). After each guess, Claude analyzes the player's guess history and the outcome, then generates a short, context-aware hint to guide the next move. A reliability testing layer verifies that Claude's hints are directionally consistent — always saying "lower" when a guess is too high and "higher" when too low — ensuring the AI behaves predictably as part of the game loop.

---

## Architecture Overview

![System Diagram](assets/system-diagram.png)

The system has four main components:

| Component | File | Role |
|---|---|---|
| Game UI | `app.py` | Streamlit interface — takes player input, displays results and AI hints |
| Game Logic | `logic_utils.py` | Validates guesses, computes scores, returns outcomes |
| AI Hint Engine | `ai_hint.py` | Calls Claude API (claude-haiku-4-5) with guess history and outcome, returns a hint |
| Reliability Tests | `tests/test_ai_reliability.py` | Verifies AI hint consistency using mocked responses |

**Data flow:** Player enters a guess → Game Logic checks it → if hint is enabled, AI Hint Engine calls Claude → Claude returns a hint → hint is displayed to the player. If the API call fails, the system falls back to the original static hint automatically.

---

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Munya574/applied-ai-system-project.git
cd applied-ai-system-project/ai110-module1show-gameglitchinvestigator-starter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key

```bash
# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

> The game still works without an API key — it falls back to static hints automatically.

### 4. Run the game

```bash
python -m streamlit run app.py
```

### 5. Run the reliability tests

```bash
pytest tests/test_ai_reliability.py -v -s
```

---

## Sample Interactions

### Example 1 — Guess Too High (Normal difficulty, range 1–100)

**Player guesses:** 75  
**Outcome:** Too High  
**AI Hint:** *"Whoa, that's way up there! Try aiming lower — you've still got plenty of range below 75."*

---

### Example 2 — Guess Too Low (Hard difficulty, range 1–200)

**Player guesses:** 30  
**Outcome:** Too Low  
**AI Hint:** *"You're starting low! The number is hiding somewhere higher — push further up the range."*

---

### Example 3 — Getting Closer (multiple guesses in history)

**Guess history:** [75, 40, 55]  
**Last outcome:** Too Low  
**AI Hint:** *"Nice narrowing! You've gone 75 → 40 → 55. Still too low — try somewhere in the 56–74 range."*

---

## Reflection and Ethics

**What are the limitations or biases in your system?**
The AI hint engine depends entirely on Claude following the system prompt consistently. If the model interprets "Too High" ambiguously or generates a hint that omits directional language, the player gets a confusing or unhelpful hint. The system also has no memory of past hints — each call is stateless, so Claude can't notice patterns like "this player always guesses too high first." Additionally, the hints are only in English, which limits accessibility.

**Could your AI be misused, and how would you prevent that?**
In a guessing game the misuse risk is low, but the hint engine does send user guess history to an external API. A bad actor could craft a guess history designed to confuse the model into giving misleading hints. To prevent this, the `parse_guess` function already validates that all inputs are integers before they reach the AI, and the fallback system ensures a broken or manipulated hint never crashes the game. For a production system, rate limiting and input sanitization on the API call would be the next steps.

**What surprised you while testing your AI's reliability?**
The biggest surprise was how much the *structure* of the test matters more than the live model output. Writing mocked reliability tests forced me to define exactly what "reliable" means — not just "Claude gives a good answer" but "Claude's answer always contains the word lower when the guess is too high." That precision is more useful for catching regressions than a vague "it seemed to work" check.

**Collaboration with AI during this project:**
- **Helpful:** Claude Code suggested adding a `try/except` fallback in `app.py` so the game never crashes if the API is unavailable. This was the right call — it made the AI feature genuinely optional rather than a hard dependency.
- **Flawed:** The initial test file imported from `app.py` directly, which would have caused Streamlit to execute all its module-level UI code during testing and crash. Claude Code caught this and restructured the imports — but only after the error surfaced, not proactively. A more defensive suggestion upfront would have saved a debugging step.

---

## Design Decisions

**Why a Reliability Testing System instead of RAG or Agentic Workflow?**  
Given the scope of the project and the time constraint, a reliability/testing system was the most honest fit. The game already had a working hint system — the meaningful upgrade was proving that the AI addition behaves predictably, not just hooking up an API call and hoping for the best.

**Why mocked tests?**  
The reliability tests use `unittest.mock` to simulate Claude's responses. This means the tests run without an API key, are fast, and are deterministic. The trade-off is they test the *structure* of reliability rather than live model behavior — but for a student project, demonstrating the testing pattern clearly is more valuable than requiring expensive API calls in CI.

**Why prompt caching on the system prompt?**  
The system prompt in `ai_hint.py` is identical on every call. Adding `cache_control: ephemeral` means repeated calls (e.g., across a long game session) reuse the cached prompt prefix, reducing cost and latency once the cache warms up.

**Why a try/except fallback in `app.py`?**  
The AI hint is an enhancement, not a core game mechanic. Wrapping the API call in a try/except ensures a missing API key or network error never crashes the game — players just see the original static hint instead.

---

## Testing Summary

**What worked:**  
- The mock-based reliability tests pass 100% consistently and cover the key behavioral contracts: directional consistency (lower/higher), non-empty output, and graceful failure fallback.  
- The existing `logic_utils` tests (from Module 1) still pass unchanged, confirming the AI integration didn't break anything.

**What didn't work initially:**  
- The `anthropic` package installed into Python 3.14 while pytest was running on Python 3.13 — causing `ModuleNotFoundError`. Fixed by installing with the explicit Python 3.13 binary.  
- The `→` Unicode arrow in `print()` statements caused a `UnicodeEncodeError` on Windows (CP1252 terminal encoding). Fixed by replacing with `->`.

**What I learned:**  
Reliability testing for AI is less about "did the model give a good answer" and more about "does the model's behavior stay within the bounds the system needs." Checking for keyword consistency ("lower"/"higher") is a simple but real contract — and mocking makes that contract testable without burning API credits.

---

## Reflection

This project taught me that adding AI to an existing system is less about the API call and more about the surrounding design. The most important parts were: making the AI integration optional (fallback), proving it behaves consistently (reliability tests), and keeping it integrated into the actual game loop rather than bolted on as a standalone script.

I also learned that "reliability" in AI systems doesn't mean the model is always right — it means the model's outputs stay within the guardrails the system depends on. A hint that says "go higher" when the guess was too high would break player trust even if it was beautifully written. That's what the tests are checking.

If I were to extend this further, I'd add a live consistency test that actually calls Claude and logs the hit rate over time, so I could monitor whether model updates affect hint directional accuracy.
