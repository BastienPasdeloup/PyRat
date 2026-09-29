PyRat Documentation
===================

.. The title above names the page for Sphinx and the browser, but is hidden on screen, where the banner below stands for it (see custom.css).
.. The files of the banner, of the video and of the learning path are produced by "make home" (see docs/home/make_home_assets.py).

.. raw:: html

   <div class="pyrat-hero">
     <img class="pyrat-hero-image" src="_static/home/pyrat_go.png" width="252" height="320"
          alt="The PyRat mascot, a pirate rat with a python around its shoulders, looking through a spyglass and shouting Go!">
     <div class="pyrat-hero-text">
       <p class="pyrat-hero-kicker">Computer science course &middot; IMT Atlantique</p>
       <p class="pyrat-hero-title" aria-hidden="true">PyRat</p>
       <p class="pyrat-hero-tagline">Teach a rat to find cheese in a maze, and learn algorithms along the way.</p>
       <div class="pyrat-hero-actions">
         <a class="pyrat-button pyrat-button-primary" href="install.html">Get started</a>
         <a class="pyrat-button" href="overview.html">Quick overview</a>
       </div>
       <p class="pyrat-hero-command"><code>uvx --from pyrat-game pyrat-init</code><span>creates your workspace, with PyRat installed in it</span></p>
     </div>
   </div>

See It in Action
----------------

.. raw:: html

   <figure class="pyrat-video">
     <video autoplay muted loop playsinline controls preload="metadata" width="1600" height="900" poster="_static/home/home_match_poster.jpg">
       <source src="_static/home/home_match.webm" type="video/webm">
       <source src="_static/home/home_match.mp4" type="video/mp4">
     </video>
     <figcaption>
       A match between two players that always run to the closest piece of cheese.
       The rat of <em>Team Ratz</em> wins 8 to 7 against the python of <em>Team Pythonz</em>.
     </figcaption>
   </figure>
   <script>
     // Readers who asked their system for less motion get a video that waits for them to start it
     if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
       document.querySelectorAll(".pyrat-video video").forEach(video => { video.removeAttribute("autoplay"); video.pause(); });
     }
   </script>

What is PyRat?
--------------

PyRat is a maze game, played by programs.
A rat, or a python, is placed in a maze where pieces of cheese are scattered.
Your job is to write the program that decides, at each turn, where it goes next.
Walls block the way, mud slows you down, and an opponent may be after the same pieces of cheese.

Behind the game, the maze is a graph: cells are vertices, and the passages between them are edges, weighted by the mud.
Catching cheese therefore means traversing a graph, finding shortest paths, solving a traveling salesperson problem, and eventually outsmarting an opponent.
PyRat takes care of everything else: it generates the mazes, runs the game, times the players, and shows what happens.

.. grid:: 1 2 2 2
   :gutter: 3
   :class-container: pyrat-features

   .. grid-item-card:: :octicon:`code;1.2em;sd-mr-1` Write players in Python

      A player is a class with a ``turn()`` method that returns a move.
      Add a ``preprocessing()`` method to think ahead before the game starts.

   .. grid-item-card:: :octicon:`device-desktop;1.2em;sd-mr-1` Watch them play

      An animated interface shows every move, the mud being crossed, the scores of the teams and the final ranking.

   .. grid-item-card:: :octicon:`graph;1.2em;sd-mr-1` Measure and compare

      Turn the interface off to play hundreds of games in seconds, and get statistics on each of them to compare your ideas.

   .. grid-item-card:: :octicon:`pencil;1.2em;sd-mr-1` Shape your mazes

      Choose the size, walls, mud and cheese, fix a seed to replay the same game, or draw a maze with the :doc:`Maze Builder <maze_builder>`.

A Player in a Few Lines
-----------------------

A player goes in the ``players`` directory of your workspace, and a game that uses it goes in the ``games`` directory.
Here is a player that moves at random, and a game in which it looks for 5 pieces of cheese.

.. tab-set::

   .. tab-item:: players/my_player.py

      .. code-block:: python

         import random
         from pyrat import Player, Maze, GameState, Action

         class MyPlayer (Player):

             def turn (self, maze: Maze, game_state: GameState) -> Action:

                 # Go to a random neighbor of the current cell
                 here = game_state.player_locations[self.get_name()]
                 there = random.choice(maze.get_neighbors(here))
                 return maze.locations_to_action(here, there)

   .. tab-item:: games/my_game.py

      .. code-block:: python

         from pyrat import Game
         from players.my_player import MyPlayer

         if __name__ == "__main__":

             # A maze of 15 by 11 cells, with 5 pieces of cheese to find
             game = Game(maze_width=15, maze_height=11, nb_cheese=5)
             game.add_player(MyPlayer())
             stats = game.start()

Then run ``uv run games/my_game.py`` from your workspace.
:doc:`The Random Programs <tutorials/the_random_programs>` tutorial goes further, with four players that get better and better.

From One Piece of Cheese to a Tournament
----------------------------------------

The `course at IMT Atlantique <https://hub.imt-atlantique.fr/ueinfo-fise1a/>`_ uses PyRat as a thread through a series of algorithmic problems.
Each step makes the game a bit harder, and calls for a new idea.

.. raw:: html

   <ol class="pyrat-path">
     <li>
       <img src="_static/home/flag.png" alt="" width="66" height="60">
       <div><strong>Discover PyRat</strong><span>Install it, run a first game, and see how players take decisions.</span></div>
     </li>
     <li>
       <img src="_static/home/cheese.png" alt="" width="64" height="60">
       <div><strong>Catch a piece of cheese</strong><span>Model the maze as a graph, and explore it with a breadth-first or depth-first search.</span></div>
     </li>
     <li>
       <img src="_static/home/mud.png" alt="" width="39" height="60">
       <div><strong>Cross the mud</strong><span>Some moves take longer than others: find shortest paths in a weighted graph with Dijkstra's algorithm.</span></div>
     </li>
     <li>
       <span class="pyrat-path-cheeses"><img src="_static/home/cheese.png" alt="" width="43" height="40"><img src="_static/home/cheese.png" alt="" width="43" height="40"><img src="_static/home/cheese.png" alt="" width="43" height="40"></span>
       <div><strong>Catch them all</strong><span>Visit every piece of cheese in as few moves as possible: a traveling salesperson problem, solved by exhaustive search.</span></div>
     </li>
     <li>
       <img src="_static/home/rat.png" alt="" width="78" height="37">
       <div><strong>Catch them faster</strong><span>Trade optimality for speed, with heuristics and greedy algorithms.</span></div>
     </li>
     <li>
       <img src="_static/home/python.png" alt="" width="54" height="80">
       <div><strong>Face an opponent</strong><span>Another player wants the same cheese: time to think in terms of game theory.</span></div>
     </li>
     <li>
       <img src="_static/home/medal.png" alt="" width="60" height="80">
       <div><strong>Win the tournament</strong><span>Put your best player against those of everyone else.</span></div>
     </li>
   </ol>

Explore the Documentation
-------------------------

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: :octicon:`rocket;1.2em;sd-mr-1` Install PyRat
      :link: install
      :link-type: doc

      Install uv, create your workspace, and run your first game.

      +++
      Start here.

   .. grid-item-card:: :octicon:`book;1.2em;sd-mr-1` Quick Overview
      :link: overview
      :link-type: doc

      What a game is made of, how a player takes decisions, and what the interface shows.

      +++
      Read this next.

   .. grid-item-card:: :octicon:`mortar-board;1.2em;sd-mr-1` Tutorials
      :link: tutorials/index
      :link-type: doc

      Guided walkthroughs, from the provided example players to custom mazes.

      +++
      Learn by doing.

   .. grid-item-card:: :octicon:`tools;1.2em;sd-mr-1` Maze Builder
      :link: maze_builder
      :link-type: doc

      An interactive tool to draw a maze in your browser and use it in your games.

      +++
      Build a maze.

   .. grid-item-card:: :octicon:`package;1.2em;sd-mr-1` PyRat API
      :link: pyrat/index
      :link-type: doc

      Every class and function of the library, with its arguments and examples.

      +++
      Look things up.

   .. grid-item-card:: :octicon:`file-directory;1.2em;sd-mr-1` Workspace API
      :link: workspace/index
      :link-type: doc

      The players and games that come with a fresh workspace.

      +++
      See the examples.

Useful Links
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
