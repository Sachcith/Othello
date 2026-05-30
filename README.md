# Othello AI Engine

A complete implementation of the classic **Othello (Reversi)** board game featuring a custom-built game engine, Alpha-Beta Pruned Minimax AI, positional heuristic evaluation, and an experimental YOLO-based neural-network evaluator.

The project includes a real-time Flask + Socket.IO web interface, multiple AI difficulty levels, board-state image generation, and neural-network-assisted move selection.

---

### Gameplay

![Gameplay](Recordings/Othello_Game.GIF)

🎥 **Full Gameplay Video:**
[Click here to watch the complete demonstration](Recordings/Othello_Game.mp4)

---

## Overview

This project explores multiple approaches to game-playing AI through Othello (Reversi).

The system includes:

* Complete Othello game engine
* Real-time browser gameplay
* Alpha-Beta Pruned Minimax Search
* Positional heuristic evaluation
* CNN/YOLO-based board-state evaluation
* Multiple AI difficulty levels
* Undo support
* Legal move detection
* Piece-flipping mechanics
* Human vs AI gameplay
* Flask + Socket.IO communication

The objective was to compare traditional search-based game AI with machine-learning-based board evaluation techniques.

---

## Comparative AI Design

This project investigates two fundamentally different approaches to game-playing AI:

### Search-Based AI
- Alpha-Beta Pruned Minimax
- Positional Heuristics
- Explicit game-tree exploration

### Learned Evaluation
- YOLO-based board-state classification
- Image-based position evaluation
- Data-driven move selection

The objective was to compare classical search techniques against neural-network-based evaluation within the same game environment.

---

## Features

### Othello Engine

* Full Othello rules implementation
* Automatic legal move generation
* Multi-directional piece flipping
* Board-state tracking
* Undo support
* Win/Loss detection

---

### Classical AI Engine

* Minimax Search
* Alpha-Beta Pruning
* Configurable search depth
* Positional board evaluation
* Automatic move selection
* Efficient game-tree exploration

---

### Neural Network Evaluation

* YOLO-based board-state classifier
* Board-to-image conversion pipeline
* Neural-network-guided move selection
* Experimental alternative to search-based AI

---

### Web Application

* Flask backend
* Flask-SocketIO communication
* Real-time board updates
* Interactive browser gameplay
* Difficulty selection
* Game reset functionality
* Live score tracking

---

### Difficulty Levels

#### Easy

Uses a trained YOLO model to evaluate candidate board states.

The AI:

1. Simulates all legal moves
2. Converts resulting boards into RGB images
3. Runs YOLO inference
4. Selects the move with the highest predicted advantage

---

#### Medium

Uses Alpha-Beta Pruned Minimax Search with depth:

```text
Depth = 3
```

Provides reasonably strong gameplay while maintaining fast response times.

---

#### Hard

Uses deeper Alpha-Beta Search with:

```text
Depth = 6
```

Produces significantly stronger gameplay through deeper game-tree exploration.

---

## AI Architecture

### Alpha-Beta Pruned Minimax

The primary AI engine uses Minimax Search enhanced with Alpha-Beta Pruning.

The search alternates between:

* Maximizing Player (⚫)
* Minimizing Player (⚪)

Benefits include:

* Reduced search space
* Faster decision making
* Stronger gameplay
* Deeper exploration within practical response times

---

### Positional Heuristic Evaluation

Board positions are evaluated using a weighted positional matrix.

The heuristic rewards:

* Corner ownership
* Stable edge positions
* Strategic expansion

The heuristic penalizes:

* Dangerous edge-adjacent squares
* Positions vulnerable to corner captures

Weight matrix:

```text
100  -20   10   5   5   10  -20  100
-20  -50   -2  -2  -2   -2  -50  -20
 10   -2    1   1   1    1   -2   10
  5   -2    1   0   0    1   -2    5
  5   -2    1   0   0    1   -2    5
 10   -2    1   1   1    1   -2   10
-20  -50   -2  -2  -2   -2  -50  -20
100  -20   10   5   5   10  -20  100
```

This allows the AI to make strategically strong decisions without searching to terminal game states.

---

### YOLO-Based Board Evaluation

An experimental AI mode uses a trained YOLO model as a board evaluator.

Pipeline:

```text
Board State
      ↓
RGB Image Generation
      ↓
YOLO Inference
      ↓
Class Probability Prediction
      ↓
Move Selection
```

The AI evaluates every legal move and chooses the position predicted to maximize advantage.

This creates a neural-network-based evaluation strategy that differs fundamentally from Minimax search.

---

## Move Generation

Legal moves are detected by scanning all eight directions from existing pieces.

The engine:

1. Finds adjacent opponent pieces
2. Continues searching in the same direction
3. Identifies valid placement squares
4. Records legal moves
5. Updates board state after placement


---

## Undo System

The engine maintains:

* Board snapshots
* Piece position dictionaries

This allows:

* Efficient state restoration
* AI search backtracking
* Minimax tree exploration

without reconstructing the board from scratch.

---

## Technical Challenges

Some major challenges during development included:

* Implementing legal move detection in eight directions
* Correctly handling piece flipping
* Efficient state restoration during search
* Designing a strong positional heuristic
* Implementing Alpha-Beta Pruning
* Managing recursive game-tree exploration
* Converting board states into image representations
* Integrating YOLO inference into gameplay
* Synchronizing frontend and backend state

---

## Results

The Hard AI consistently performs significantly better than the YOLO-based evaluator due to deeper strategic planning.

Key characteristics:

### Hard Mode

* Deep game-tree exploration
* Alpha-Beta optimization
* Strategic corner acquisition
* Strong positional play

### Medium Mode

* Faster response times
* Reduced search depth
* Balanced gameplay difficulty

### Easy Mode

* Neural-network-based decisions
* Experimental evaluation strategy
* Fast move generation

---

## Performance

A naive Minimax implementation would explore an exponential number of game states.

This project improves performance through:

* Alpha-Beta Pruning
* Positional Heuristics
* Efficient Undo System
* Early Terminal Detection
* Board Snapshot Reuse

These optimizations allow practical gameplay even with deeper searches.

---

## Project Structure

```text
.
├── app.py
├── Backtracking.py
├── best.pt
├── requirements.txt
├── LICENSE
├── README.md
├── Recordings
│   ├── Othello_Game.GIF
│   └── Othello_Game.mp4
├── screenshots
│   └── Screenshot_20250817_224352.png
├── static
│   └── socketio.min.js
└── templates
    └── index.html
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Sachcith/Connect-4_Game.git
cd Othello
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the server:

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## Technologies Used

### Programming Languages

* Python

---

### AI & Machine Learning

* NumPy
* YOLO
* Alpha-Beta Pruning
* Minimax Search
* Heuristic Evaluation

---

### Web Technologies

* Flask
* Flask-SocketIO
* HTML
* CSS
* JavaScript

---

### Image Processing

* Pillow (PIL)

---

## Technical Highlights

This project demonstrates:

* Adversarial Search Algorithms
* Alpha-Beta Pruning
* Recursive Game Tree Exploration
* Heuristic Evaluation Design
* Neural Network Evaluation
* Board-State Image Generation
* Real-Time Client-Server Communication
* State Synchronization
* Search Optimization Techniques
* Othello Rule Engine Design

---

## Future Improvements


* Monte Carlo Tree Search (MCTS)
* Iterative Deepening Search
* Transposition Tables
* Zobrist Hashing
* Reinforcement Learning
* Self-Play Training
* Stronger Neural-Network Evaluators
* Online Multiplayer Support
* AI vs AI Tournament Mode
* Move Explanation System

---

## Author

Developed as a personal exploration of:

* Game AI
* Adversarial Search Algorithms
* Alpha-Beta Pruning
* Neural Network Evaluation
* Othello Strategy
* Real-Time Web Applications

The project combines classical game-search techniques with neural-network-based evaluation methods to explore multiple approaches to intelligent game-playing agents.

---