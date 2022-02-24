# Chess UI

This is a chess UI which uses `python-chess` and `pygame` to implement a working chess board.

[Python Chess](https://python-chess.readthedocs.io/en/latest/)

[Pygame](https://www.pygame.org/docs/)

## Move Generation

I have included a sample move generation function in `main.py`. It generates a valid move at random from the list
of all available moves. You will see that creating a random move generator with our library is very simple!

```python
def random_move_generator(board):
    moves = list(board.legal_moves)
    return random.choice(moves)
```

A "move generator" is just going to be any function which accepts a `chess.Board` and returns a `chess.Move`.
The goal of this project then is to use AI to create an intelligent move generator.

## Game Initialization

To play a game, you just need to call the `play_chess()` function. It accepts two optional arguments,
`white` and `black` with which you can pass any move generation function.

### Use cases:
```python
# Case 1. No arguments. The user will play both sides of the board.
play_chess()

# Case 2. The user will play white. The computer will play black.
play_chess(black=move_generation_function)

# Case 3. The user will play black. The computer will play white.
play_chess(white=move_generation_function)

# Case 4. The computer will play both sides.
play_chess(white=move_generation_function_a, black=move_generation_function_b)
```


## User Interface

I learned enough to make a basic chess interface which can interact with our chess library.

### Example 1. Initial Position

![Initial Position](interface/images/initial_pos.png)

### Example 2. Scholar's Mate

![Fool's Mate](interface/images/scholars_mate.png)

