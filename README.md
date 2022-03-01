# Chess UI

This is a chess UI which uses [Python Chess](https://python-chess.readthedocs.io/en/latest/)
and [Pygame](https://www.pygame.org/docs/) to implement a working chess board.

 ```bash
 pip install python-chess
 pip install pygame
 ````

## Move Generation

I have included a sample move generation function in each `example.py` script. It generates a valid move at random from the list
of all available moves. You will see that creating a random move generator with our library is very simple!

```python
def random_move_generator(board):
    moves = list(board.legal_moves)
    return random.choice(moves)
```

A "move generator" is simply any function which accepts a `chess.Board` and returns a `chess.Move`.
The goal of this project then is to use AI to create an intelligent move generator.

## Game Initialization

To play a game, you just need to call the `play_chess()` function. It accepts two optional arguments,
`white` and `black` with which you can pass any move generation function.
Run `example.py` to try this out.

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


## Graphical User Interface

I learned enough about *pygame* to make a basic chess interface which can interact with our chess library.
You can run `example_gui.py` to see the graphical interface in action.

### Example 1. Initial Position

![Initial Position](interface/images/initial_pos.png)

### Example 2. Scholar's Mate

![Fool's Mate](interface/images/scholars_mate.png)


## Terminal User Interface

The graphical interface is useful for human play, but the terminal interface is much more convenient
for self-play, when the AI wants to play against itself, maybe many times in rapid succession.
You can run `example_tui.py` to see the terminal interface in action as well.

