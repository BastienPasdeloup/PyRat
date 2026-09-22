``game``
========

The ``game`` subpackage is what runs a game.
It contains the class you instantiate to start one, the description of the situation your player is given at each turn, the constants you pass around, and the exception raised when a game cannot go on.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`Game <../Game>`

      The central class: it builds the maze, registers the players, runs the turns and returns the statistics.

   .. grid-item-card:: :doc:`GameState <../GameState>`

      The snapshot your player receives at each turn: scores, locations, remaining cheese, mud, turn number.

   .. grid-item-card:: :doc:`enums <../enums>`

      All the constants you pass around, such as ``Action``, ``GameMode``, ``RenderMode`` and ``PlayerSkin``.

   .. grid-item-card:: :doc:`PyRatException <../PyRatException>`

      The exception raised when a game cannot proceed, for instance because a player crashed or returned something that is not an action.

.. toctree::
   :maxdepth: 1

   ../Game
   ../GameState
   ../enums
   ../PyRatException
