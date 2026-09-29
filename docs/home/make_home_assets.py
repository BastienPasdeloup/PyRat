##########################################################################################
########################################## INFO ##########################################
##########################################################################################

# This script produces the video and the images shown on the home page of the documentation.
# It is run by hand, with "make home" from the "docs" directory (requires the "ffmpeg" command).
# The files it produces are committed, so that neither the CI nor the readers need ffmpeg.

"""
Produces the files shown on the home page of the documentation, in ``source/_static/home``.

The video is a match between two greedy players, as the PyRat window shows it, recorded without opening any window.
The game is first played without rendering, keeping each of its states.
These states are then replayed in the real window of PyRat, drawn off screen, and each image it presents is sent to ffmpeg.
The clock of the window is replaced by a virtual one, so that the video has exactly the pace of the real interface, however slow the machine is.

The images are drawings of the game, reduced to the size at which the page shows them, as the originals are far too large for a web page.
"""

##########################################################################################
######################################### IMPORTS ########################################
##########################################################################################

# External imports
import copy
import heapq
import os
import subprocess

# Pygame must draw off screen and stay silent, which is decided before it is imported
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

# PyRat imports
from pyrat import Game, Player, Maze, GameState, Action, PlayerSkin, RenderMode, StartingLocation, RenderingEngine
import pyrat.src.game.game as game_module
import pyrat.src.rendering.gui.window as window_module
import pyrat.src.rendering.gui.animation as animation_module

##########################################################################################
######################################## CONSTANTS #######################################
##########################################################################################

# Size and pace of the video
VIDEO_SIZE = (1600, 900)
VIDEO_FPS = 30

# Time the final screen, with the medals, stays in the video, in seconds
FINAL_SCREEN_DURATION = 3.0

# Where the files are written
OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "_static", "home")
OUTPUT_NAME = "home_match"

# Drawings of the game shown on the page, with the height they are reduced to (twice the displayed size, for high-density screens)
GUI_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pyrat", "gui")
IMAGES = {"pyrat_go.png": (os.path.join("drawings", "pyrat_go.png"), 640),
          "rat.png": (os.path.join("players", "rat", "east.png"), 120),
          "python.png": (os.path.join("players", "python", "avatar.png"), 160),
          "cheese.png": (os.path.join("cheese", "cheese.png"), 120),
          "mud.png": (os.path.join("mud", "mud.png"), 120),
          "flag.png": (os.path.join("flag", "flag.png"), 120),
          "medal.png": (os.path.join("endgame", "first.png"), 160)}

# Game shown in the video, fixed so that the video can be recorded again identically
GAME_CONFIG = {"random_seed": 31,
               "maze_width": 11,
               "maze_height": 8,
               "cell_percentage": 85.0,
               "wall_percentage": 55.0,
               "mud_percentage": 15.0,
               "nb_cheese": 15}

##########################################################################################
######################################### CLASSES ########################################
##########################################################################################

class GreedyPlayer (Player):

    """
    *(This class inherits from* ``Player`` *).*

    A player that always heads to the closest piece of cheese, taking mud into account.
    It only exists to make the video lively, and is not one of the players of the workspace.
    """

    ##################################################################################

    def turn ( self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
        *(This method redefines the method of the parent class with the same name).*

        Runs Dijkstra's algorithm from the current location, and moves towards the closest piece of cheese.

        Args:
            maze:       An object representing the maze in which the player plays.
            game_state: An object representing the state of the game.

        Returns:
            The first move towards the closest piece of cheese.
        """

        # Explore the maze by increasing distance, until a piece of cheese is found
        source = game_state.player_locations[self.get_name()]
        distances = {source: 0}
        parents = {}
        heap = [(0, source)]
        while heap:
            distance, cell = heapq.heappop(heap)
            if cell in game_state.cheese:
                while parents.get(cell) != source and cell != source:
                    cell = parents[cell]
                return maze.locations_to_action(source, cell)
            if distance > distances[cell]:
                continue
            for neighbor in maze.get_neighbors(cell):
                new_distance = distance + maze.get_weight(cell, neighbor)
                if new_distance < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_distance
                    parents[neighbor] = cell
                    heapq.heappush(heap, (new_distance, neighbor))
        return Action.NOTHING

##########################################################################################

class StateRecorder (RenderingEngine):

    """
    *(This class inherits from* ``RenderingEngine`` *).*

    A rendering engine that shows nothing, and keeps the states of the game it is given.
    """

    states = []

    def render ( self,
                 players:    list[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:

        """
        *(This method redefines the method of the parent class with the same name).*

        Keeps a copy of the state of the game.

        Args:
            players:    Players of the game.
            maze:       Maze of the game.
            game_state: State of the game.
        """

        StateRecorder.states.append(copy.deepcopy(game_state))

##########################################################################################

class VirtualClock ():

    """
    A clock that only advances when someone sleeps, so that recording the window takes as long as needed, and never skips an image.
    """

    def __init__ (self) -> None:
        self.now = 0.0

    def perf_counter (self) -> float:
        return self.now

    def sleep ( self,
                duration: float
              ) ->        None:
        self.now += max(duration, 0.0)

##########################################################################################

class StateFeeder ():

    """
    Stands for the queue through which the window receives the states of the game, and hands it the recorded ones.
    Once they are all given, it lets the final screen stay for a while, then tells the window that the game is gone.
    """

    def __init__ ( self,
                   states: list[GameState],
                   clock:  VirtualClock
                 ) ->      None:
        self.states = list(states)
        self.clock = clock
        self.end_time = None

    def get ( self,
              timeout: float
            ) ->       GameState:
        if self.states:
            return self.states.pop(0)
        if self.end_time is None:
            self.end_time = self.clock.now + FINAL_SCREEN_DURATION
        if self.clock.now >= self.end_time:
            raise EOFError
        self.clock.sleep(timeout)
        raise window_module.queue.Empty

##########################################################################################
######################################## FUNCTIONS #######################################
##########################################################################################

def play_game () -> tuple[Maze, list[GameState], list[Player]]:

    """
    Plays the game without rendering it, and keeps each of its states.

    Returns:
        The maze of the game, its successive states (the initial one first), and its players.
    """

    # The game builds its rendering engine from the name it imports, which we replace by our recorder
    game_module.RenderingEngine = StateRecorder
    game = Game(render_mode=RenderMode.NO_RENDERING, **GAME_CONFIG)
    players = [GreedyPlayer(name="Rat", skin=PlayerSkin.RAT), GreedyPlayer(name="Python", skin=PlayerSkin.PYTHON)]
    game.add_player(players[0], team="Team Ratz", location=StartingLocation.TOP_LEFT)
    game.add_player(players[1], team="Team Pythonz", location=StartingLocation.BOTTOM_RIGHT)
    stats = game.start()
    print(f"Game played in {stats['turns']} turns, final scores {StateRecorder.states[-1].get_score_per_team()}")
    return game._Game__maze, StateRecorder.states, players

##########################################################################################

def record ( maze:    Maze,
             states:  list[GameState],
             players: list[Player]
           ) ->       tuple[list[tuple[float, bytes]], float]:

    """
    Replays the states in the window of PyRat, drawn off screen, and keeps each image it presents with the instant it is presented.

    Args:
        maze:    Maze of the game.
        states:  Successive states of the game, the initial one first.
        players: Players of the game.

    Returns:
        The images presented by the window, as instants (in seconds) and raw RGB pixels, and the instant the window closed.
    """

    # The window reads the time from these modules, so they are given the virtual clock
    clock = VirtualClock()
    for module in [window_module, animation_module]:
        module.time.perf_counter = clock.perf_counter
        module.time.sleep = clock.sleep

    # The window is opened at the size of the video, rather than at a size depending on the screen
    window_module.GameWindow._GameWindow__open_window = lambda self: pygame.display.set_mode(VIDEO_SIZE)

    # Each image presented is kept, with the instant it is presented at
    frames = []
    original_flip = pygame.display.flip
    def recording_flip () -> None:
        original_flip()
        frames.append((clock.now, pygame.image.tobytes(pygame.display.get_surface(), "RGB")))
    pygame.display.flip = recording_flip

    # Show the preprocessing image for a moment, as the real game does, then play the turns
    window = window_module.GameWindow(maze, states[0], players, False, False, 0, 1.0)
    clock.sleep(1.0)
    window.run(StateFeeder(states[1:], clock))
    return frames, clock.now

##########################################################################################

def encode ( frames:   list[tuple[float, bytes]],
             duration: float
           ) ->        None:

    """
    Encodes the images as videos at a constant pace, each instant of the video showing the last image presented before it.
    Two formats are written, so that every browser can play one of them.

    Args:
        frames:   The images presented by the window, as instants (in seconds) and raw RGB pixels.
        duration: Duration of the video, in seconds, which lasts after the last image while the final screen stays.
    """

    # Resample the images at the pace of the video
    nb_video_frames = int(duration * VIDEO_FPS) + 1
    resampled = []
    j = 0
    for i in range(nb_video_frames):
        t = i / VIDEO_FPS
        while j + 1 < len(frames) and frames[j + 1][0] <= t:
            j += 1
        resampled.append(frames[j][1])
    print(f"Encoding {nb_video_frames} images ({duration:.1f} seconds)")

    # One video for each format, plus a poster image shown before the video plays
    raw_input = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}", "-r", str(VIDEO_FPS), "-i", "-"]
    outputs = {"webm": ["-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "40", "-row-mt", "1", "-pix_fmt", "yuv420p"],
               "mp4": ["-c:v", "libx264", "-crf", "28", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]}
    for extension, codec in outputs.items():
        path = os.path.join(OUTPUT_DIRECTORY, f"{OUTPUT_NAME}.{extension}")
        process = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", *raw_input, "-an", *codec, path], stdin=subprocess.PIPE)
        for frame in resampled:
            process.stdin.write(frame)
        process.stdin.close()
        process.wait()
        print(f"Written {os.path.normpath(path)}")

    # The poster is taken in the middle of the game, when there is action on screen
    poster = pygame.image.frombytes(resampled[len(resampled) // 3], VIDEO_SIZE, "RGB")
    path = os.path.join(OUTPUT_DIRECTORY, f"{OUTPUT_NAME}_poster.jpg")
    pygame.image.save(poster, path)
    print(f"Written {os.path.normpath(path)}")

##########################################################################################

def reduce_images () -> None:

    """
    Writes the drawings of the game shown on the page, reduced to the height at which the page needs them.
    """

    # A drawing is never enlarged, as it would only get blurry
    for name, (source, height) in IMAGES.items():
        image = pygame.image.load(os.path.join(GUI_DIRECTORY, source))
        if image.get_height() > height:
            image = pygame.transform.smoothscale(image, (round(image.get_width() * height / image.get_height()), height))
        path = os.path.join(OUTPUT_DIRECTORY, name)
        pygame.image.save(image, path)
        print(f"Written {os.path.normpath(path)}")

##########################################################################################
########################################### GO! ##########################################
##########################################################################################

if __name__ == "__main__":

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    reduce_images()
    maze, states, players = play_game()
    frames, duration = record(maze, states, players)
    encode(frames, duration)

##########################################################################################
##########################################################################################
