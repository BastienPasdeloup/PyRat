Stopping a PyRat Game
=====================

As you may have noticed, closing the game window (clicking the cross, or pressing the ``Esc`` key) does not stop the game.
This is because the game runs in a separate process, allowing the game to continue even if the window is closed.

Default Behavior
----------------

By default, the game will continue running until one of the following conditions is met:

- It reaches an end condition.
- An error occurs in one of the players' codes.

In the second case, the error of the player is printed, and the ``start()`` method of the game raises a :doc:`PyRatPlayerException </pyrat/PyRatPlayerException>`.
Your program can catch it, for instance to skip that game and go on with the next one when running many games in a row:

.. code-block:: python

    from pyrat import Game, PyRatPlayerException

    game = Game()
    game.add_player(MyPlayer())
    try:
        stats = game.start()
    except PyRatPlayerException as error:
        print("A player caused an error:", error)

However, if you want to let the game run even in the event of a player error, you can set the ``continue_on_error`` parameter to ``True`` when creating the game instance.
This is particularly useful when running matches with multiple players, as it does not penalize other players.

Stopping the Game
-----------------

If you want to abort the game at any time, the best way is to click in the terminal in which the game is running and press ``Ctrl+C``.
The game then stops, its window closes, and the ``start()`` method of the game raises a :doc:`PyRatException </pyrat/PyRatException>` with the message ``The game was interrupted by the user``.
Unless your program catches this exception, it stops as well, even if it is running games in a loop.

.. note::

   If your program catches ``PyRatException`` to go on with the next game (for instance in a loop of games), it will also go on after a ``Ctrl+C``.
   To avoid this, catch ``PyRatPlayerException`` instead, which is only raised when a player causes an error.

In VSCode, you can also stop the game by clicking the red square at the top of the editor window.

.. tip::

   If a game seems stuck, check the terminal first: a player that raises an error stops the game there, and the traceback tells you which one.