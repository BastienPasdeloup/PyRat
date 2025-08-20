Players
=======

The ``players`` directory is where you will store your players.
In PyRat, you define the behavior of a player by creating a class that inherits from the ``Player`` class.
This class must implement the methods that define how the player behaves in the game.
In the default workspace, you will find a few sample players that you can use as a template to create your own players.
The ``TemplatePlayer`` defines the minimal implementation of a player, while the ``Random1`` to ``Random4`` players are examples of players that make random moves.

.. toctree::
   :maxdepth: 1

   Random1
   Random2
   Random3
   Random4
   TemplatePlayer