# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

The purpose of the game is to create a number guessing game where the player tries to guess a secret number within a certain range using hints and a limited number of attempts. While testing the game, I found several bugs including incorrect hints, attempts starting at the wrong value, wrong scoring behavior, difficulty ranges that were inconsistent, and the New Game button not properly resetting the game state. The secret number was also changing due to Streamlit reruns and there was a type mismatch between strings and integers during comparisons. To fix these issues, I corrected the hint logic, adjusted the difficulty ranges, fixed the scoring and attempt counter, removed the unnecessary string conversion, and used Streamlit session state to store the secret number and reset values properly when starting a new game.

## 📸 Demo
<img width="1916" height="921" alt="image" src="https://github.com/user-attachments/assets/63cf41d4-5f30-4811-9d75-66343fe5a2f7" />

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
