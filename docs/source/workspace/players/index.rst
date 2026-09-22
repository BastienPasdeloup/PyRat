Players
=======

The ``players`` directory is where you will store your players.
In PyRat, you define the behavior of a player by creating a class that inherits from the ``Player`` class.
This class must implement the methods that define how the player behaves in the game.
In the default workspace, you will find a few sample players that you can use as a template to create your own players:

- ``TemplatePlayer``, in ``template_player.py``, shows the minimal implementation of a player, and is the file to copy when you start a new one.
- ``Random1`` to ``Random4``, in ``random1.py`` to ``random4.py``, are four players that move at random, each one smarter than the previous one.

.. tip::

   The :doc:`The Random Programs <../../tutorials/the_random_programs>` tutorial goes through these four players one by one, and explains what each of them improves.

.. toctree::
   :maxdepth: 1

   Random1
   Random2
   Random3
   Random4
   TemplatePlayer