# Chess

Chess engine with AI players. Goal is to train the AI with latest research
results (budget-AlphaZero). Long-term goal is to explore some wacky variants of
chess, ideally ones that reduce the likelihood of draws.

# Status

- Engine working, all moves programmed (including en-passant and castling)
- Players are rudimentary, currently use a 'naive', which is simply randomly selecting a legal move
- Can output board position as an image with sprites of pieces
- Shell script that can convert a folder of images into a low-framerate video (useful for debugging)

# To-do

- Input/output chess.com-compatible sequence of moves, possibly for stronger verification that the engine works, and other uses
- Improved player strategy: choose move that maximizes the difference in score between 'me' and 'opponent' (depth = 1)
- RL unsupervised self-play ML training and evaluation
- Command-line interface to simulate games with/without AI model strategies and other settings
- Might need some code re-factoring to improve simulation speed, especially in the future to implement depth-limited search as a heauristic (depth > 10?)
