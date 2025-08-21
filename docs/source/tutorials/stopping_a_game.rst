Stopping a PyRat Game
=====================

As you may have noticed, closing the game window (clicking the cross, or pressing the ``Esc`` key) does not stop the game.
This is because the game runs in a separate process, allowing the game to continue even if the window is closed.

Default Behavior
----------------

By default, the game will continue running until: one of the following conditions is met:

- It reaches an end condition.
- An error occurs in one of the players' codes.

However, if you want to let the game run even in the event of a player error, you can set the ``stop_on_error`` parameter to ``False`` when creating the game instance.
This is particularly useful when running matches with multiple players, as it does not penalize other players.

Stopping the Game
-----------------

If you want to abort the game at any time, the best way is to click in the terminal in which the game is running and press ``Ctrl+C``.
However, if you are running games in a loop, PyRat may just abort the current game and continue with the next one.
To ensure that the game stops completely, you can hold ``Ctrl+C`` for a few seconds.

In VSCode, you can also stop the game by clicking the red square at the top of the editor window.