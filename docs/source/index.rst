PyRat Documentation
===================

Welcome to the PyRat documentation website!
This documentation is designed to help you understand and use the PyRat library effectively.

.. grid:: 1 1 3 3
   :gutter: 3

   .. grid-item-card:: Install PyRat
      :link: install
      :link-type: doc

      Install uv, create your workspace, and run your first game.

      +++
      Start here.

   .. grid-item-card:: Quick Overview
      :link: overview
      :link-type: doc

      What a game is made of, how a player takes decisions, and what the interface shows.

      +++
      Read this next.

   .. grid-item-card:: Tutorials
      :link: tutorials/index
      :link-type: doc

      Guided walkthroughs, from the provided example players to custom mazes.

      +++
      Learn by doing.

.. grid:: 1 1 3 3
   :gutter: 3

   .. grid-item-card:: Maze Builder
      :link: maze_builder
      :link-type: doc

      An interactive tool to draw a maze in your browser and use it in your games.

      +++
      Build a maze.

   .. grid-item-card:: PyRat API
      :link: pyrat/index
      :link-type: doc

      Every class and function of the library, with its arguments and examples.

      +++
      Look things up.

   .. grid-item-card:: Workspace API
      :link: workspace/index
      :link-type: doc

      The players and games that come with a fresh workspace.

      +++
      See the examples.

New to PyRat?
-------------

The fastest path from nothing to a running game is:

.. card:: Three steps to your first game

   1. :doc:`Install PyRat <install>` and create your workspace with a single command.
   2. Run the provided ``sample_game.py`` to check that everything works.
   3. Follow :doc:`The Random Programs <tutorials/the_random_programs>` to understand how a player is written, then write your own.

Useful links
------------

.. grid:: 1 2 2 2
   :gutter: 2

   .. grid-item::

      - `PyRat GitHub repository <https://github.com/BastienPasdeloup/PyRat>`_.
      - `GitHub issues <https://github.com/BastienPasdeloup/PyRat/issues>`_.
      - `PyRat on PyPI <https://pypi.org/project/pyrat-game/>`_.

   .. grid-item::

      - `PyRat documentation <https://bastienpasdeloup.github.io/PyRat/>`_.
      - `IMT Atlantique course page <https://hub.imt-atlantique.fr/ueinfo-fise1a/>`_.
      - `Discord server of the course <https://discord.gg/eMnFArZ8ht>`_.

.. toctree::
   :hidden:

   install
   overview
   tutorials/index
   maze_builder
   pyrat/index
   workspace/index
