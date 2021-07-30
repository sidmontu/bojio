# Project Bojio

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.9-brightgreen.svg" alt="Python version">
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Chess engine with AI players. Goal is to train the AI with latest research
results (budget-AlphaZero). Long-term goal is to explore some wacky variants of
chess, ideally ones that reduce the likelihood of draws.

# Status

- Engine working, all moves programmed (including en-passant and castling)
- Players are rudimentary, currently use a 'naive' strategy, which is simply randomly selecting a legal move
- Can output board position as an image with sprites of pieces superimposed on top
- Shell script that can convert a folder of images into a low-framerate video (useful for debugging)

# To-do

- Highlight square with slightly different color from which the last move was played from
- Input/output chess.com-compatible sequence of moves, possibly for stronger verification that the engine works, and other potential use-cases
- Improved player strategy: choose a move that maximizes the difference in score between 'me' and 'opponent' (depth = 1)
- RL unsupervised self-play ML training and evaluation (some form of AlphaZero)
- Command-line interface to simulate games with/without AI model strategies and other settings
- Might need some code re-factoring to improve simulation speed, especially in the future to implement depth-limited search as a heauristic (depth > 10?)
- Write docstrings for each class/function
