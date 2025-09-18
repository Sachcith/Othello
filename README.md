# ♟️ Othello (Reversi) in Python

This is a **Python implementation of the classic board game Othello (also known as Reversi)**.  
The game supports:
- **Player vs Player (PvP)** mode.
- **Player vs AI** mode, where the AI uses **Minimax search with Alpha-Beta pruning**.

---

## 🎮 Features
- 8x8 Othello board initialized with standard setup.
- Displays the board using Unicode symbols:
  - ⚫ for Player X
  - ⚪ for Player O
  - ⭕ for empty cells
  - ✳️ for valid moves
- Undo functionality (for internal AI computations).
- **AI Opponent**:
  - Implements Minimax algorithm.
  - Uses Alpha-Beta pruning for efficiency.
  - Adjustable search depth.

---

## 🛠️ Requirements
- Python **3.8+** (no external libraries required).

---

## ▶️ How to Run
1. Save the file as `othello.py`.
2. Run the program in terminal:

   ```bash
   python othello.py
   ```

3. Play the game...
4. Checkout the UI build using FLASK-Socketio api
