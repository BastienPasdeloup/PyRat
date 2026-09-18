# Expansion of the short links written in the .dot files into the pages and anchors of the documentation.
#     HREF="Game"             ->  the page of the class
#     HREF="Game#add_player"  ->  the anchor of the member on that page (Sphinx names anchors after the full Python path)
# The same short forms are accepted in the URL, headURL, tailURL and labelURL attributes of edges, which make their labels clickable.
# Paths are given from the root of the documentation, behind the @DOCS_ROOT@ placeholder that the Makefile replaces.
# All the pages embedding a diagram, as well as the _static directory holding the full-size files, are one level below the root.
# This file uses extended regular expressions (sed -E), and ~ as the delimiter of substitutions.
#
# Classes of the library
s~(HREF|URL|headURL|tailURL|labelURL)="Game#~\1="@DOCS_ROOT@pyrat/Game.html#pyrat.src.game.game.Game.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Game"~\1="@DOCS_ROOT@pyrat/Game.html#pyrat.src.game.game.Game"~g
s~(HREF|URL|headURL|tailURL|labelURL)="GameState#~\1="@DOCS_ROOT@pyrat/GameState.html#pyrat.src.game.game_state.GameState.~g
s~(HREF|URL|headURL|tailURL|labelURL)="GameState"~\1="@DOCS_ROOT@pyrat/GameState.html#pyrat.src.game.game_state.GameState"~g
s~(HREF|URL|headURL|tailURL|labelURL)="PyRatException#~\1="@DOCS_ROOT@pyrat/PyRatException.html#pyrat.src.game.exceptions.PyRatException.~g
s~(HREF|URL|headURL|tailURL|labelURL)="PyRatException"~\1="@DOCS_ROOT@pyrat/PyRatException.html#pyrat.src.game.exceptions.PyRatException"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Player#~\1="@DOCS_ROOT@pyrat/Player.html#pyrat.src.players.player.Player.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Player"~\1="@DOCS_ROOT@pyrat/Player.html#pyrat.src.players.player.Player"~g
s~(HREF|URL|headURL|tailURL|labelURL)="FixedPlayer#~\1="@DOCS_ROOT@pyrat/FixedPlayer.html#pyrat.src.players.fixed_player.FixedPlayer.~g
s~(HREF|URL|headURL|tailURL|labelURL)="FixedPlayer"~\1="@DOCS_ROOT@pyrat/FixedPlayer.html#pyrat.src.players.fixed_player.FixedPlayer"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Graph#~\1="@DOCS_ROOT@pyrat/Graph.html#pyrat.src.mazes.graph.Graph.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Graph"~\1="@DOCS_ROOT@pyrat/Graph.html#pyrat.src.mazes.graph.Graph"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Maze#~\1="@DOCS_ROOT@pyrat/Maze.html#pyrat.src.mazes.maze.Maze.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Maze"~\1="@DOCS_ROOT@pyrat/Maze.html#pyrat.src.mazes.maze.Maze"~g
s~(HREF|URL|headURL|tailURL|labelURL)="RandomMaze#~\1="@DOCS_ROOT@pyrat/RandomMaze.html#pyrat.src.mazes.random_maze.RandomMaze.~g
s~(HREF|URL|headURL|tailURL|labelURL)="RandomMaze"~\1="@DOCS_ROOT@pyrat/RandomMaze.html#pyrat.src.mazes.random_maze.RandomMaze"~g
s~(HREF|URL|headURL|tailURL|labelURL)="BigHolesRandomMaze#~\1="@DOCS_ROOT@pyrat/BigHolesRandomMaze.html#pyrat.src.mazes.big_holes_random_maze.BigHolesRandomMaze.~g
s~(HREF|URL|headURL|tailURL|labelURL)="BigHolesRandomMaze"~\1="@DOCS_ROOT@pyrat/BigHolesRandomMaze.html#pyrat.src.mazes.big_holes_random_maze.BigHolesRandomMaze"~g
s~(HREF|URL|headURL|tailURL|labelURL)="UniformHolesRandomMaze#~\1="@DOCS_ROOT@pyrat/UniformHolesRandomMaze.html#pyrat.src.mazes.uniform_holes_random_maze.UniformHolesRandomMaze.~g
s~(HREF|URL|headURL|tailURL|labelURL)="UniformHolesRandomMaze"~\1="@DOCS_ROOT@pyrat/UniformHolesRandomMaze.html#pyrat.src.mazes.uniform_holes_random_maze.UniformHolesRandomMaze"~g
s~(HREF|URL|headURL|tailURL|labelURL)="HolesOnSideRandomMaze#~\1="@DOCS_ROOT@pyrat/HolesOnSideRandomMaze.html#pyrat.src.mazes.holes_on_side_random_maze.HolesOnSideRandomMaze.~g
s~(HREF|URL|headURL|tailURL|labelURL)="HolesOnSideRandomMaze"~\1="@DOCS_ROOT@pyrat/HolesOnSideRandomMaze.html#pyrat.src.mazes.holes_on_side_random_maze.HolesOnSideRandomMaze"~g
s~(HREF|URL|headURL|tailURL|labelURL)="MazeFromDict#~\1="@DOCS_ROOT@pyrat/MazeFromDict.html#pyrat.src.mazes.maze_from_dict.MazeFromDict.~g
s~(HREF|URL|headURL|tailURL|labelURL)="MazeFromDict"~\1="@DOCS_ROOT@pyrat/MazeFromDict.html#pyrat.src.mazes.maze_from_dict.MazeFromDict"~g
s~(HREF|URL|headURL|tailURL|labelURL)="MazeFromMatrix#~\1="@DOCS_ROOT@pyrat/MazeFromMatrix.html#pyrat.src.mazes.maze_from_matrix.MazeFromMatrix.~g
s~(HREF|URL|headURL|tailURL|labelURL)="MazeFromMatrix"~\1="@DOCS_ROOT@pyrat/MazeFromMatrix.html#pyrat.src.mazes.maze_from_matrix.MazeFromMatrix"~g
s~(HREF|URL|headURL|tailURL|labelURL)="RenderingEngine#~\1="@DOCS_ROOT@pyrat/RenderingEngine.html#pyrat.src.rendering.rendering_engine.RenderingEngine.~g
s~(HREF|URL|headURL|tailURL|labelURL)="RenderingEngine"~\1="@DOCS_ROOT@pyrat/RenderingEngine.html#pyrat.src.rendering.rendering_engine.RenderingEngine"~g
s~(HREF|URL|headURL|tailURL|labelURL)="ShellRenderingEngine#~\1="@DOCS_ROOT@pyrat/ShellRenderingEngine.html#pyrat.src.rendering.shell_rendering_engine.ShellRenderingEngine.~g
s~(HREF|URL|headURL|tailURL|labelURL)="ShellRenderingEngine"~\1="@DOCS_ROOT@pyrat/ShellRenderingEngine.html#pyrat.src.rendering.shell_rendering_engine.ShellRenderingEngine"~g
s~(HREF|URL|headURL|tailURL|labelURL)="PygameRenderingEngine#~\1="@DOCS_ROOT@pyrat/PygameRenderingEngine.html#pyrat.src.rendering.pygame_rendering_engine.PygameRenderingEngine.~g
s~(HREF|URL|headURL|tailURL|labelURL)="PygameRenderingEngine"~\1="@DOCS_ROOT@pyrat/PygameRenderingEngine.html#pyrat.src.rendering.pygame_rendering_engine.PygameRenderingEngine"~g
# Enumerations of the library
s~(HREF|URL|headURL|tailURL|labelURL)="Action"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.Action"~g
s~(HREF|URL|headURL|tailURL|labelURL)="GameMode"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.GameMode"~g
s~(HREF|URL|headURL|tailURL|labelURL)="RenderMode"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.RenderMode"~g
s~(HREF|URL|headURL|tailURL|labelURL)="PlayerSkin"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.PlayerSkin"~g
s~(HREF|URL|headURL|tailURL|labelURL)="RandomMazeAlgorithm"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.RandomMazeAlgorithm"~g
s~(HREF|URL|headURL|tailURL|labelURL)="StartingLocation"~\1="@DOCS_ROOT@pyrat/enums.html#pyrat.src.game.enums.StartingLocation"~g
# Players of the workspace
s~(HREF|URL|headURL|tailURL|labelURL)="TemplatePlayer#~\1="@DOCS_ROOT@workspace/players/TemplatePlayer.html#TemplatePlayer.TemplatePlayer.~g
s~(HREF|URL|headURL|tailURL|labelURL)="TemplatePlayer"~\1="@DOCS_ROOT@workspace/players/TemplatePlayer.html"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random1#~\1="@DOCS_ROOT@workspace/players/Random1.html#Random1.Random1.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random1"~\1="@DOCS_ROOT@workspace/players/Random1.html"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random2#~\1="@DOCS_ROOT@workspace/players/Random2.html#Random2.Random2.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random2"~\1="@DOCS_ROOT@workspace/players/Random2.html"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random3#~\1="@DOCS_ROOT@workspace/players/Random3.html#Random3.Random3.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random3"~\1="@DOCS_ROOT@workspace/players/Random3.html"~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random4#~\1="@DOCS_ROOT@workspace/players/Random4.html#Random4.Random4.~g
s~(HREF|URL|headURL|tailURL|labelURL)="Random4"~\1="@DOCS_ROOT@workspace/players/Random4.html"~g
# Games of the workspace
s~(HREF|URL|headURL|tailURL|labelURL)="sample_game"~\1="@DOCS_ROOT@workspace/games/sample_game.html"~g
s~(HREF|URL|headURL|tailURL|labelURL)="visualize_random_players"~\1="@DOCS_ROOT@workspace/games/visualize_random_players.html"~g
