The ``postprocessing(...)`` Method
===============================

In addition to the ``turn(...)`` and ``preprocessing(...)`` methods, the ``Player`` class also includes a ``postprocessing(...)`` method.
This method is called after the main game loop has completed and can be used to perform any final updates or clean-up tasks.
In this tutorial, we will explore how to implement the ``postprocessing(...)`` method in a custom player class.

An Example of Usage
-------------------

In this example, we will illustrate how the ``postprocessing(...)`` method can be used to analyze the moves made by an opponent player during the game.
We will not provide a complete implementation, but rather focus on the structure and purpose of the method.

Let's consider a match in 3 games between two players, where the first player to reach 2 wins is declared the overall winner.
A game script for this will use the ``game.reset(...)`` functions to allow players to store information across games.

Here is a possible class that uses the ``postprocessing(...)`` method to analyze the series of game states across the games, and to determine the opponent's strategy based on that.
Then, the ``turn(...)`` method has a different behavior depending on the conclusions found in the previous game.

.. code-block:: python

    class MyPlayer (Player):

        def __init__ ( self,
                       *args:    object,
                       **kwargs: object
                     ) ->        None:

            # Inherit from parent class
            super().__init__(*args, **kwargs)

            # Store the game states across the game
            self.all_game_states = None

            # Strategy to use
            self.strategy = None
        
        #######################################################################
        
        def preprocessing ( self,
                            maze:       Maze,
                            game_state: GameState,
                          ) ->          None:
            
            # Initialize the list of game states
            self.all_game_states = []

        #######################################################################

        def turn ( self,
                   maze:       Maze,
                   game_state: GameState,
                   ) ->          Action:

            # Store the current game state
            self.all_game_states.append(game_state)

            # Depending on the current strategy, we will choose a different action
            if self.strategy == "beat_greedy_opponent":

                # We determined in an earlier game that the opponent follows a greedy strategy
                # Therefore, we will try to outsmart them by choosing adapted actions
            
            elif self.strategy == "beat_density_opponent":

                # We determined in an earlier game that the opponent follows a density-based strategy
                # Therefore, we will try to outsmart them by choosing adapted actions

            else:

                # We do not have any particular information about the opponent's moves yet

            # Return the action to perform
            return # ...

        #######################################################################

        def postprocessing ( self,
                             maze:       Maze,
                             game_state: GameState,
                             stats:      dict[str, object],
                           ) ->          None:

            # When the game is over, we analyze the series of game states to determine the opponent's strategy
            # It can be something along these lines (probability_of_strategy is a placeholder for a function of yours)
            if probability_of_strategy(self.all_game_states, "greedy") > 0.8:
                self.strategy = "beat_greedy_opponent"
            elif probability_of_strategy(self.all_game_states, "density") > 0.8:
                self.strategy = "beat_density_opponent"

With this code, if your player determines that the opponent followed a greedy strategy during the game that just ended, it will set the ``self.strategy`` attribute accordingly.
Thus, in the next game, the ``turn(...)`` method will behave differently.

Other Possible Usages
---------------------

In addition to the example above, here are a few extra ideas you can implement using the ``postprocessing(...)`` method.

- Train a model with reinforcement.
- Remove some temporary files you may have created across the game.
- Close a connection to an external resource.
- Etc.