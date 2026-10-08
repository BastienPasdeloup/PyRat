``game``
========

The ``game`` subpackage is what runs a game.
It contains the class you instantiate to start one, the description of the situation your player is given at each turn, the constants you pass around, and the exceptions raised when something goes wrong.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`Game <../Game>`

      The central class: it builds the maze, registers the players, runs the turns and returns the statistics.

   .. grid-item-card:: :doc:`GameState <../GameState>`

      The snapshot your player receives at each turn: scores, locations, remaining cheese, mud, turn number.

   .. grid-item-card:: :doc:`enums <../enums>`

      All the constants you pass around, such as ``Action``, ``GameMode``, ``RenderMode`` and ``PlayerSkin``.

   .. grid-item-card:: :doc:`PyRatException <../PyRatException>`

      The exception raised when the library is used incorrectly, for instance with an invalid argument.

   .. grid-item-card:: :doc:`PyRatPlayerException <../PyRatPlayerException>`

      The exception raised when a player causes an error during a game, for instance by crashing or by returning something that is not an action.

.. toctree::
   :maxdepth: 1

   ../Game
   ../GameState
   ../enums
   ../PyRatException
   ../PyRatPlayerException
