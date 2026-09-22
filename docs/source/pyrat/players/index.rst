``players``
===========

The ``players`` subpackage describes what a character in a game is.
It contains the class your own programs inherit from, and one ready-made player.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item-card:: :doc:`Player <../Player>`

      The class your own players inherit from, with the ``preprocessing()``, ``turn()`` and ``postprocessing()`` methods.

   .. grid-item-card:: :doc:`FixedPlayer <../FixedPlayer>`

      A player that replays a predefined list of actions, used in particular by the game replays saved by PyRat.

.. tip::

   The players you write live in your own workspace, not in this subpackage.
   See the :doc:`Workspace API <../../workspace/players/index>` for the ones that come with a fresh workspace.

.. toctree::
   :maxdepth: 1

   ../Player
   ../FixedPlayer
