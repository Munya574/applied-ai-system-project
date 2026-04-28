from logic_utils import check_guess
from app import check_guess as app_check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix tests (import from app.py where fixes were applied) ---

# Bug 1: Hints were backwards — "Go HIGHER!" shown when guess was too high
def test_hint_too_high_says_go_lower():
    outcome, message = app_check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message}"

def test_hint_too_low_says_go_higher():
    outcome, message = app_check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message}"


# Bug 2: Secret was cast to str on even attempts, breaking int comparison
def test_check_guess_always_uses_int_secret():
    # Even if somehow a str secret is passed, the outcome must not be wrong
    # The fix removes str() coercion — verify int comparison works correctly
    outcome, _ = app_check_guess(9, 50)
    assert outcome == "Too Low", "9 < 50 should be Too Low (not fooled by string sort order)"

    outcome, _ = app_check_guess(99, 50)
    assert outcome == "Too High", "99 > 50 should be Too High"


# Bug 3: Hard difficulty range was 1–50, easier than Normal (1–100)
def test_hard_range_is_harder_than_normal():
    hard_low, hard_high = get_range_for_difficulty("Hard")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high, (
        f"Hard range (1–{hard_high}) should be larger than Normal range (1–{normal_high})"
    )


# Bug 4: "Too High" on even attempts incorrectly gave +5 points instead of -5
def test_too_high_always_deducts_score():
    for attempt in range(1, 7):
        new_score = update_score(100, "Too High", attempt)
        assert new_score < 100, f"Score should decrease for Too High on attempt {attempt}"

def test_too_low_always_deducts_score():
    for attempt in range(1, 7):
        new_score = update_score(100, "Too Low", attempt)
        assert new_score < 100, f"Score should decrease for Too Low on attempt {attempt}"
