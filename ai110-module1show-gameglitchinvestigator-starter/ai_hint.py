import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a witty assistant for "Game Glitch Investigator", a number guessing game.
When given a player's guess history and the result of their last guess, provide a short (1 sentence)
encouraging hint about their next move. Be strictly consistent with direction:
- If the last result was "Too High", always tell the player to go LOWER.
- If the last result was "Too Low", always tell the player to go HIGHER.
Keep the tone fun and game-themed."""


def get_ai_hint(guess_history: list, secret_range: tuple, last_outcome: str) -> str:
    """Return a Claude-generated hint based on guess history and last outcome."""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Range: {secret_range[0]}-{secret_range[1]}. "
                    f"Guesses so far: {guess_history}. "
                    f"Last result: {last_outcome}. "
                    f"Give me one short hint."
                ),
            }
        ],
    )
    return response.content[0].text
