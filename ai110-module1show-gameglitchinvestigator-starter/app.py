import random
import streamlit as st
# FIX: Refactored logic functions into logic_utils.py using Copilot Agent mode
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
from ai_hint import get_ai_hint

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

demo_mode = st.sidebar.checkbox("Enable AI Hints", value=True)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

# FIX: attempts was initialized to 1, causing off-by-one in attempts left display. Changed to 0 using Copilot Agent mode
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

# FIX: Info message was hardcoded to "1 and 100" regardless of difficulty. Now uses dynamic low/high using Copilot Agent mode
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: New Game did not reset score, status, or history. Added missing resets using Copilot Agent mode
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: secret was cast to str on even attempts, breaking int comparison. Removed str() coercion using Copilot Agent mode
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            if demo_mode:
                gap = abs(guess_int - secret)
                range_size = high - low
                closeness = gap / range_size

                if closeness <= 0.05:
                    proximity = "burning"
                elif closeness <= 0.15:
                    proximity = "close"
                else:
                    proximity = "far"

                demo_hints = {
                    ("Too High", "burning"): "🔥 So close! Just a tiny bit lower — you're almost there!",
                    ("Too High", "close"):   "📉 Getting warmer! Go a bit lower, you're not far off.",
                    ("Too High", "far"):     "⬇️ Too high! Aim quite a bit lower — you've got a ways to go.",
                    ("Too Low",  "burning"): "🔥 Nearly there! Just nudge a little higher!",
                    ("Too Low",  "close"):   "📈 You're in the ballpark! Try a bit higher.",
                    ("Too Low",  "far"):     "⬆️ Too low! You need to go quite a bit higher.",
                }
                ai_message = demo_hints.get((outcome, proximity), message)
                st.warning(f"🤖 {ai_message}")
            else:
                try:
                    ai_message = get_ai_hint(
                        guess_history=st.session_state.history,
                        secret_range=(low, high),
                        last_outcome=outcome,
                    )
                    st.warning(f"🤖 {ai_message}")
                except Exception:
                    st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
