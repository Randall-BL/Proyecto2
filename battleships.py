"""
Battleships Game

Two player battleships game.
Not familiar with the battleships game? Check e.g. Wikipedia:
https://en.wikipedia.org/wiki/Battleship_(game)

Best played on two monitors, but also works on a single monitor due to the
ability to hide your playing field.

Certain programming choices may have been made with a more featureful game
in mind, but ran I out of time.
Still, this is a fully functional first version of the game

Start off by naming both players and choosing if you want ships to sink
from one hit.
By default ships sink once each part (size = parts) of them is hit.


Then the first player starts placing in their battleships.
The second player stands by meanwhile.
Number of battleships, and their size, is hardcoded for now:
    1x Carrier      (size 5)
    1x Battleship   (size 4)
    2x Cruiser      (size 3)
    2x Destroyer    (size 2)
    2x Submarine    (size 1)

Ships are placed by clicking a corresponding button on the play field.
Start from the top left corner of the ship.

Ship can be placed horizontally and vertically.
Ships can't overlap or touch, but you don't have to worry about this, the game
window doesn't allow invalid placements.
In some rules even corners of ships can't touch, but in these rules they can.

If your chosen placement has both horizontal and vertical placements available,
choose the orientation by pressing the button next to, or under, the first
button you pressed.

If only one orientation is available at your chosen placement, the whole rest
of the ship is automatically placed in.

Once you have placed in all your ships, the second player and start placing
their ships.


Once the second player finishes their ship placements, the two main game
windows are opened. The players' own fields are hidden by default, be sure to
unhide them when appropriate by unchecking the checkbox.

Drag the other game window to your second monitor and face the monitors away
from each other and start playing. If you don't have a second monitor, work
with the field hiding checkbox.

Fire shots by clicking on the buttons on the left of your game window.
Color codes indicate what happened to your shots.
See your own ship placements and opponent's shots from the grid on the right
(But be sure to unhide the field first!)

Winner is the first person to destroy all each of the opponent's ships.
Or a player can also forfeit.

Enjoy the game!
"""

from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

from random import randrange
from functools import partial
import webbrowser
import os.path


# global constants:
X_FIELDS = list("ABCDEFGHIJ")

SHIP_PLACE_ORDER = ("Carrier,Battleship" + ",Cruiser" * 2 + ",Destroyer" * 2 +
                    ",Submarine" * 2).split(",")

BATTLESHIP_SIZES = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Destroyer": 2,
    "Submarine": 1
}

PLAYING_FIELD_COLORS = {
    "water": "#3eb2fa",
    "ship": "green",
    "hit": "#ff8c8c",
    "miss": "#d9c532"
}

EXIT_APPLICATION = False

ICON_MISSING = False

# to be set
GAME_LOGIC = None

# contain the Player objects for both players
PLAYERS = []


class Player:
    """
    Models a player for this game
    """

    def __init__(self, name):
        """
        Constructor, creates a player object
        :param name: str, player's name
        """

        self.__name = name
        self.__battleships = {}
        self.__shots_fired = 0
        self.__shots_hit = 0
        self.__hits_taken = 0
        self.__ships_left = 8

        # to be set
        self.__game_window = None

        # 10x10 matrix intialized with zeros
        # 0 = water
        # 1 = ship part
        # 2 = hit ship
        # 3 = missed shot
        self.__playing_field = [[0 for _ in range(10)] for _ in range(10)]

    def increment_shots(self):
        """
        Increments the amount of shots this player has fired
        """

        self.__shots_fired += 1

    def increment_hits(self):
        """
        Increments the amount of shots this player has hit
        """

        self.__shots_hit += 1

    def increment_hits_taken(self):
        """
        Increments the amount of hits this player has taken
        """

        self.__hits_taken += 1

    def decrease_ship_count(self):
        """
        Decreases the amount of ships this player has left and returns
        the new count of ships
        :return:    int, count of ships left
        """

        self.__ships_left -= 1
        return self.__ships_left

    def add_battleship(self, battleship, vertical, coords):
        """
        Adds a battleship to this player's battleships
        :param battleship:  str,    name of battleship to add
        :param vertical:    bool,   True  = placed vertically
                                    False = placed horizontally
        :param coords:      tuple,  tuple of the x and y coordinates
                                    for ship's origin
        """

        # set or append depending on if a the player already has
        # the type of battleship
        if battleship not in self.__battleships:
            self.__battleships[battleship] = [Battleship(battleship, vertical,
                                                         coords)]
        else:
            self.__battleships[battleship].append(
                Battleship(battleship, vertical, coords))

        x = coords[0]
        y = coords[1]

        # mark all the ship's parts to the player's playing field object
        for i in range(BATTLESHIP_SIZES[battleship]):
            if vertical:
                self.__playing_field[y + i][x] = 1
            else:
                self.__playing_field[y][x + i] = 1

    def get_battleships(self):
        """
        Returns this player's battleships
        :return:    dict, dict of battleship objects
        """

        return self.__battleships

    def set_game_window(self, game_window):
        """
        Assigns a GameWindow object to this player
        :param game_window: GameWindow, game window object
        """

        self.__game_window = game_window

    def update_playing_field(self, x, y, hit):
        """
        Updates hits and misses to this player's playing field
        :param x:       int,    playing field x coordinate
        :param y:       int,    playing field y coordinate
        :param hit:     bool,   True  = ship was hit here
                                False = missed shot here
        """

        self.__playing_field[y][x] = 2 if hit else 3

    def get_game_window(self):
        """
        Returns this player's game window object
        :return: GameWindow, game window object
        """

        return self.__game_window

    def get_playing_field(self):
        """
        Returns this player's playing field object
        :return:    2d array, the playing field
        """

        return self.__playing_field

    def ships_left(self):
        """
        Returns the amount of ships this player has left
        :return:    int, count
        """

        return self.__ships_left

    def shots_fired(self):
        """
        Returns the amount of shots this player has fired
        :return:    int, count
        """

        return self.__shots_fired

    def shots_hit(self):
        """
        Returns the amount of shots this player has hit
        :return:    int, count
        """

        return self.__shots_hit

    def hits_taken(self):
        """
        Returns the amount of hits this player has taken
        :return:    int, count
        """

        return self.__hits_taken

    def __str__(self):
        """
        Returns the string representation of this object (player's name)
        :return: str, player's name
        """

        return self.__name


class Battleship:
    """
    Models a battleship
    """

    def __init__(self, ship_type, vertical, coords):
        """
        Constructor, creates a battleship object
        :param ship_type:   str,    type of battleship to create
        :param vertical:    bool,   True  = placed vertically
                                    False = placed horizontally
        :param coords:      tuple,  tuple of the x and y coordinates
                                    for ship's origin
        """

        self.__ship_type = ship_type
        self.__size = BATTLESHIP_SIZES[ship_type]
        self.__vertical = vertical
        self.__hits_taken = 0

        # array of tuples containing all the ship's part's coordinates
        self.__coords = []

        # which parts of the ship haven't been hit
        # same as above at start
        self.__parts_left = []

        # generate all of the ship's parts
        x = coords[0]
        y = coords[1]
        for i in range(self.__size):
            if vertical:
                self.__coords.append((x, y + i))
                self.__parts_left.append((x, y + i))
            else:
                self.__coords.append((x + i, y))
                self.__parts_left.append((x + i, y))

    def assign_hit(self, x, y, sink_from_one):
        """
        Marks a part of this ship hit and returns
        how many parts left it has
        :param x:               int,   playing field x coordinate
        :param y:               int,   playing field y coordiante
        :param sink_from_one:   bool,  True  = ships sink from one hit
                                       False = ships sink once each part is hit
        :return:                int,   amount of parts left in ship
        """

        self.__hits_taken += 1

        # whole ship is gone from one hit
        if sink_from_one:
            self.__parts_left.clear()

        # ship no longer has this part
        else:
            self.__parts_left.remove((x, y))

        # return amount of parts left in ship
        return len(self.__parts_left)

    def get_coords(self):
        """
        Returs this battleship's coordinates
        :return:    array, array of tuples
        """

        return self.__coords

    def parts_left(self):
        """
        Returns the amount of parts this battleship has left
        :return:    int, count
        """

        return len(self.__parts_left)

    def get_size(self):
        """
        Returns the size of this battleship
        :return:    int, size
        """

        return self.__size

    def hits_taken(self):
        """
        Returns the amount of hits this battleship has taken
        :return:    int, count
        """

        return self.__hits_taken

    def __str__(self):
        """
        Returns the string representation of this object (battleships's type)
        :return: str, battleship's type
        """

        return self.__ship_type


class SettingsWindow:
    """
    A class to model the settings gui that appears on program startup
    """

    def __init__(self):
        """
        Constructor, creates the settings gui and its controls
        """

        self.__main_window = Tk()

        # 250x150 non-resizeable window
        self.__main_window.geometry("250x155")
        self.__main_window.resizable(False, False)

        # set title and icon
        self.__main_window.title("Battleships")
        if not ICON_MISSING:
            self.__main_window.iconbitmap("icon.ico")

        # create a menu
        menu = Menu(self.__main_window)
        options_menu = Menu(menu, tearoff=0)
        options_menu.add_command(label="Exit Application",
                                 command=self.__main_window.destroy)
        menu.add_cascade(label="Options", menu=options_menu)

        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="Game Rules", command=game_rules)
        helpmenu.add_command(label="GitHub Repository", command=github_link)
        helpmenu.add_command(label="About...", command=about)
        menu.add_cascade(label="Help", menu=helpmenu)

        self.__main_window.config(menu=menu)

        # player 1 name input
        self.__player1_entry = Entry(self.__main_window)
        self.__player1_entry.pack(pady=(15, 0))
        self.__player1_entry.insert(END, "Player 1")

        # player 2 name input
        self.__player2_entry = Entry(self.__main_window)
        self.__player2_entry.pack(pady=(5, 0))
        self.__player2_entry.insert(END, "Player 2")

        # checkbox to select an option
        self.__sink_from_one = IntVar(self.__main_window)
        sink_option = Checkbutton(self.__main_window,
                                  text="Sink ships from one hit",
                                  variable=self.__sink_from_one)
        sink_option.pack(pady=(5, 0))

        # frame to contain next two buttons
        button_frame = Frame(self.__main_window)
        button_frame.pack(pady=(10, 0))

        # start game button
        start_game_button = Button(button_frame,
                                   text="Start Game",
                                   command=self.start_game)
        start_game_button.grid(row=0, column=0, padx=(0, 5))

        # quit button
        quit_button = Button(button_frame,
                             text="Quit",
                             command=self.__main_window.destroy)
        quit_button.grid(row=0, column=1, padx=(5, 0))

        self.__main_window.mainloop()

    def start_game(self):
        """
        Starts the Battleships game based off the settings set in the gui
        """

        # empty names default to Player X
        p1_name = self.__player1_entry.get()
        if not p1_name:
            p1_name = "Player 1"

        p2_name = self.__player2_entry.get()
        if not p2_name:
            p2_name = "player 2"

        # disallow same name due to the gui elements being
        # very confusing if you can't tell players apart from name
        if p1_name == p2_name:
            messagebox.showerror("Error", "Players can't have the same name!")
            return

        self.__main_window.destroy()

        # create ship placements window for player 1 and wait for it to exit
        ArrangeShipsWindow(Player(p1_name))

        # if window was terminanted without finishing ship placements
        # return to the settings window as opposed to continuing to
        # player 2's ship placements
        if not PLAYERS:
            # if exit application was chosen by the user
            if not EXIT_APPLICATION:
                SettingsWindow()
            return

        # create ship placements window for player 2 and wait for it to exit
        ArrangeShipsWindow(Player(p2_name))
        
        # if player 2's window was closed without finishing ship placements
        # clear the PLAYERS global and return to settings screen
        if len(PLAYERS) == 1:
            if EXIT_APPLICATION:
                return 
            PLAYERS.clear()
            SettingsWindow()

        player1 = PLAYERS[0]
        player2 = PLAYERS[1]

        global GAME_LOGIC
        # initialize game logic and store the object to the GAME_LOGIC global
        GAME_LOGIC = GameLogic(self.__sink_from_one.get(), player1, player2)

        # create player 1's game window
        game_window1 = GameWindow(player1)
        # assign a game window to player
        player1.set_game_window(game_window1)

        # Create player 1's game window
        game_window2 = GameWindow(player2)
        player2.set_game_window(game_window2)

        # start the game
        GAME_LOGIC.start_game()


class ArrangeShipsWindow:
    """
    A class to model the gui where a player arranges their playing field
    """

    def __init__(self, player):
        """
        Constructor, creates the gui and controls for arranging ships on your
        playing field
        :param player: Player, Player object for the player arranging ships
        """

        self.__player = player

        # matrix to contain all the buttons for selecting battleship placements
        # initialize 10 empty rows
        self.__field_buttons = [[] for _ in range(10)]

        # which battleship type is being placed and which part of it
        self.__placing_ship = SHIP_PLACE_ORDER[0]
        self.__choosing_orientation = False
        self.__ships_placed = 0

        # a tuple for the origin of ship that's being placed
        self.__current_ship_origin = (0, 0)

        # 10x10 matrix for ship parts in the playing field
        # initialize with false (no battleship part placed here)
        self.__ship_parts = [[False for _ in range(10)] for _ in range(10)]

        self.__main_window = Tk()

        # 500x615 non-resizeable window
        self.__main_window.geometry("500x615")
        self.__main_window.resizable(False, False)

        # set title and icon
        self.__main_window.title(f"{self.__player} Arrange Field")
        if not ICON_MISSING:
            self.__main_window.iconbitmap("icon.ico")

        # create a menu
        menu = Menu(self.__main_window)
        options_menu = Menu(menu, tearoff=0)
        options_menu.add_command(label="Exit To Main Menu",
                                 command=self.exit_main_menu)
        options_menu.add_separator()
        options_menu.add_command(label="Exit Application",
                                 command=self.exit_application)
        menu.add_cascade(label="Options", menu=options_menu)

        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="Game Rules", command=game_rules)
        helpmenu.add_command(label="GitHub Repository", command=github_link)
        helpmenu.add_command(label="About...", command=about)
        menu.add_cascade(label="Help", menu=helpmenu)

        self.__main_window.config(menu=menu)

        self.__now_placing_label = Label(self.__main_window,
                                         text=f"{self.__player}, place "
                                              "your battleships!\nNow placing:"
                                              " Carrier (size 5)",
                                         justify=LEFT,
                                         font=("Arial", 15))
        self.__now_placing_label.pack(padx=(20, 0), pady=(10, 0), anchor="w")

        info_label = Label(self.__main_window,
                           text="Place one part at a time by pressing "
                                "a button.\nStart from the TOP LEFT "
                                "corner of the barrleship!",
                           justify=LEFT,
                           font=("Arial", 10))
        info_label.pack(padx=(20, 0), pady=(10, 20), anchor="w")

        # 10x10 matrix of buttons
        # one button for each playing field spot
        # associate each button with a function and
        # predetermined arguments (x, y)
        button_frame = Frame(self.__main_window)
        button_frame.pack(padx=10)
        for y in range(10):
            for x in range(10):
                # store each button for future configuration
                self.__field_buttons[y].append(
                    Button(button_frame,
                           text=field_name(x, y),
                           command=partial(self.field_button, x, y),
                           bg=PLAYING_FIELD_COLORS["water"],
                           width=4))
                self.__field_buttons[y][x].grid(row=y, column=x, padx=2,
                                                pady=2)

        # frame to contain color code labels
        color_codes_frame = Frame(self.__main_window)
        color_codes_frame.pack()

        water_color_code = Label(color_codes_frame,
                                 text="Water",
                                 justify=LEFT,
                                 font=("Arial", 11),
                                 fg=PLAYING_FIELD_COLORS["water"])
        water_color_code.grid(row=0, column=0, padx=10)

        invalid_placement_color_code = Label(color_codes_frame,
                                             text="Invalid Placement",
                                             justify=LEFT,
                                             font=("Arial", 11),
                                             fg=PLAYING_FIELD_COLORS["hit"])
        invalid_placement_color_code.grid(row=0, column=1, padx=10)

        ship_color_code = Label(color_codes_frame,
                                text="Ship Part",
                                justify=LEFT,
                                font=("Arial", 11),
                                fg=PLAYING_FIELD_COLORS["ship"])
        ship_color_code.grid(row=0, column=3, padx=10)

        # frame to contain the bottom part of the window
        bottom_frame = Frame(self.__main_window)
        bottom_frame.pack(padx=(20, 0), pady=(10, 20))
        ship_list_label = Label(bottom_frame,
                                text="Ship List:\n"
                                     "1x Carrier (size 5)\n"
                                     "1x Battleship (size 4)\n"
                                     "2x Cruiser (size 3)\n"
                                     "2x Destroyer (size 2)\n"
                                     "2x Submarine (size 1)",
                                justify=LEFT,
                                font=("Arial", 10))
        ship_list_label.grid(row=0, column=0, sticky=W)

        # frame to contain the right part of bottom frame
        bottom_right_frame = Frame(bottom_frame)
        bottom_right_frame.grid(row=0, column=1, padx=(20, 0))

        instruction_label = Label(bottom_right_frame,
                                  text="Ships can not touch or overlap.\n"
                                       "First choose ship's top left corner,\n"
                                       "then orientation (if available)\n"
                                       "Place all ships to continue",
                                  justify=LEFT,
                                  font=("Arial", 10))
        instruction_label.grid(row=0)

        clear_placements_button = Button(bottom_right_frame,
                                         text="Clear Ship Placements",
                                         command=self.clear_everything)
        clear_placements_button.grid(row=1, pady=(10, 0))

        # color all buttons appropriately
        self.update_button_states()

        # start mainloop
        self.__main_window.mainloop()

    def field_button(self, coord_x, coord_y):
        """
        A ship consists of 1-5 parts, this command gets ran when a part
        of a ship gets placed into the playing field by one of the buttons
        :param coord_x: int, playing field x-coordinate
        :param coord_y: int, playing field y-coordinate
        """

        # turn the corresponding button to ship color
        self.__field_buttons[coord_y][coord_x]\
            .config(bg=PLAYING_FIELD_COLORS["ship"], state=DISABLED)

        # check orientations
        self.ship_orientation_check(coord_x, coord_y)

        # if we just placed the last ship, we're done
        if self.__ships_placed == len(SHIP_PLACE_ORDER):
            return

        # Set a ship part as existing
        self.__ship_parts[coord_y][coord_x] = True

        self.update_button_states()

    def ship_orientation_check(self, coord_x, coord_y):
        """
        Checks which ship orientations (horizontal and vertical) are
        available at the specified x and y coordinates.
        If both are available, just note that down.
        If only one orientation is available, place the ship right away
        :param coord_x: int, playing field x-coordinate
        :param coord_y: int, playing field y-coordinate
        """

        ship_size = BATTLESHIP_SIZES[self.__placing_ship]

        # if placing the first part of a ship
        if not self.__choosing_orientation:
            # mark as ship's origin
            self.__current_ship_origin = (coord_x, coord_y)

            # get possible placement orientations at coords
            placement = self.check_placement(coord_x, coord_y, ship_size)
            orientations = placement["valid_orientations"]

            # if both orientations are available we're done
            # processing in this function
            if orientations == 0b11:
                self.__choosing_orientation = True
                return

            # if only horizontal orientation is available,
            # place the ship right away
            elif orientations & 0b10:
                for i in range(ship_size):
                    # mark each ship part and config buttons
                    self.__ship_parts[coord_y][coord_x + i] = True
                    self.__field_buttons[coord_y][coord_x + i].config(
                        bg=PLAYING_FIELD_COLORS["ship"],
                        state=DISABLED)

            # same for vertical
            else:
                for i in range(ship_size):
                    self.__ship_parts[coord_y + i][coord_x] = True
                    self.__field_buttons[coord_y + i][coord_x].config(
                        bg=PLAYING_FIELD_COLORS["ship"],
                        state=DISABLED)

            self.__choosing_orientation = False

            # finished placing, add the ship to the player
            self.__player.add_battleship(self.__placing_ship,
                                         orientations & 0b01 == 1,
                                         self.__current_ship_origin)
            # start placing the next ship
            self.place_next_ship()

        # choosing orientation
        else:
            # if origin y is smaller than current y
            # vertical orientation was chosen
            is_vertical = self.__current_ship_origin[1] < coord_y
            if is_vertical:
                for i in range(ship_size - 1):
                    # add all ship parts
                    self.__ship_parts[coord_y + i][coord_x] = True
                    # color all buttons corresponding to added ship parts
                    self.__field_buttons[coord_y + i][coord_x].config(
                        bg=PLAYING_FIELD_COLORS["ship"],
                        state=DISABLED)

            # horizontal orientation chosen
            else:
                for i in range(ship_size - 1):
                    self.__ship_parts[coord_y][coord_x + i] = True
                    self.__field_buttons[coord_y][coord_x + i].config(
                        bg=PLAYING_FIELD_COLORS["ship"],
                        state=DISABLED)

            self.__choosing_orientation = False
            self.__player.add_battleship(self.__placing_ship,
                                         is_vertical,
                                         self.__current_ship_origin)
            self.place_next_ship()

    def place_next_ship(self):
        """
        Updates the gui and logic for placing the next ship
        """

        self.__ships_placed += 1

        # if all ships have been placed
        if self.__ships_placed == len(SHIP_PLACE_ORDER):
            if messagebox.askyesno("Proceed?", "All battleships placed.\n"
                                               "Do you wish to proceed?\n\n"
                                               "Choosing no clears all your "
                                               "ship placements"):
                self.__main_window.destroy()

                # add player is now all set
                # add them to the global
                PLAYERS.append(self.__player)
                return
            else:
                # player chose to not accept his ship placements
                # start all over again
                self.clear_everything()
                return
        self.__placing_ship = SHIP_PLACE_ORDER[self.__ships_placed]
        self.__choosing_orientation = False

        self.__now_placing_label.config(text=f"{self.__player}, place your "
                                             "battleships!\nNow placing: "
                                             f"{self.__placing_ship} (size "
                                             f"{BATTLESHIP_SIZES[self.__placing_ship]})")

    def update_button_states(self):
        """
        Enables and disables buttons based on where the user is allowed
        to place a part of a ship or choose a rotation.
        """

        # always reset every non-ship-part button
        for x in range(10):
            for y in range(10):
                if not self.__ship_parts[y][x]:
                    self.__field_buttons[y][x].config(state=NORMAL,
                                                      bg=PLAYING_FIELD_COLORS[
                                                          "water"])

        # if we're starting to place a new ship
        if not self.__choosing_orientation:
            size = BATTLESHIP_SIZES[self.__placing_ship]

            for x in range(10):
                for y in range(10):
                    # color and disable all invalid placements buttons
                    if not self.__ship_parts[y][x] \
                            and not self.check_placement(x, y, size)[
                            "valid_placement"]:
                        self.__field_buttons[y][x]\
                            .config(state=DISABLED,
                                    bg=PLAYING_FIELD_COLORS["hit"])

        # if not starting to place new ship, we're choosing orientation
        else:
            origin_x = self.__current_ship_origin[0]
            origin_y = self.__current_ship_origin[1]
            for x in range(10):
                for y in range(10):
                    # color and disable all buttons, but orientation
                    # choosing buttons and ship part buttons
                    if not self.__ship_parts[y][x] \
                            and (x, y) != (origin_x + 1, origin_y) \
                            and (x, y) != (origin_x, origin_y + 1):
                        self.__field_buttons[y][x]\
                            .config(state=DISABLED,
                                    bg=PLAYING_FIELD_COLORS["hit"])

    def check_placement(self, x, y, size):
        """
        Checks if the placement for the specified ship size at the specified
        coordinates is possible both horizontally and vertically.
        Ships can't overlap or touch
        TODO: come up with better/clearer logic for this
        :param x:       int,    x-coordinate
        :param y:       int,    y-coordinate
        :param size:    int,    size of battleship to be placed
        :return:        dict,   dict containing the vailidity and orientations
                                of the palcement
                                key                 value
                                valid_placement     bool,   True  = valid
                                                            False = invalid
                                valid_orientations  int,    high bit set for
                                                            horizonal placement
                                                            low bit set for
                                                            vertical placement
        """

        parts = self.__ship_parts
        placement = {
            "valid_placement": False,
            "valid_orientations": 0
        }

        # first check if a vertical placement is possible

        # last element to check on the middle check
        # +1 if the ship's last part isnt on the on the last row
        middle_end = y + size - 1 + (1 if y + size < 10 else 0)
        # on the middle check, check an extra element above if there is one
        one = 1 if y > 0 else 0

        # if statement short circuted to the max
        # first check if ship can fit vertically
        # then check the column left of x (if needed)
        # then check the column x is on
        # then check the column right of x (if needed)
        # we're looking for occurences of already placed ship parts
        # if one is found, the placement is invalid
        if y + size <= 10 \
                and (
                x == 0 or not any(get_column(parts, x - 1, y, y + size - 1))) \
                and not any(get_column(parts, x, y - one, middle_end)) \
                and (
                x == 9 or not any(get_column(parts, x + 1, y, y + size - 1))):
            placement["valid_placement"] = True
            placement["valid_orientations"] = 0b01  # low bit

        # if ship is of size one, we're good to return already
        if size == 1:
            return placement

        # check if horizontal placement is possible
        # same logic as in the vertical check, just done horizonally
        middle_end = x + size + (1 if x + size < 9 else 0)
        one = 1 if x > 0 else 0

        if x + size <= 10 \
                and (y == 0 or not any(parts[y - 1][x:x + size])) \
                and not any(parts[y][x - one:middle_end]) \
                and (y == 9 or not any(parts[y + 1][x:x + size])):
            placement["valid_placement"] = True
            placement["valid_orientations"] |= 0b10  # high bit

        return placement

    def clear_everything(self):
        """
        Clears everything related to the current player's ship placements by
        just destroying the gui and starting from the beginning with a new gui
        """

        self.__main_window.destroy()
        ArrangeShipsWindow(Player(str(self.__player)))

    def exit_main_menu(self):
        """
        Exits to main menu
        """
        if messagebox.askyesno("Are you sure?", "Are you sure you want "
                                                "to exit to the main menu?"):
            PLAYERS.clear()
            self.__main_window.destroy()

    def exit_application(self):
        """
        Exits the whole application
        """
        if messagebox.askyesno("Are you sure?", "Are you sure you want "
                                                "to exit the application?"):
            self.__main_window.destroy()
            global EXIT_APPLICATION
            EXIT_APPLICATION = True


class GameWindow:
    """
    A class to model the actual game window.
    One object for each player
    """

    def __init__(self, player):
        """
        Constructor, creates the game screen gui and its controls.
        :param player:   Player,    player object for this player
        """

        self.__player = player
        self.__opponent = GAME_LOGIC.get_opponent(player)
        self.__destroyed = False
        self.__main_window = Tk()

        # 830x600 non-resizeable window
        self.__main_window.geometry("830x600")
        self.__main_window.resizable(False, False)

        # set title and icon
        self.__main_window.title(f"Battleships | {player}")
        if not ICON_MISSING:
            self.__main_window.iconbitmap("icon.ico")

        # create a menu
        menu = Menu(self.__main_window)
        options_menu = Menu(menu, tearoff=0)
        options_menu.add_command(label="Forfeit Game",
                                 command=self.forfeit_game)
        options_menu.add_command(label="Exit To Main Menu",
                                 command=self.exit_main_menu)
        options_menu.add_separator()
        options_menu.add_command(label="Exit Application",
                                 command=self.exit_application)
        menu.add_cascade(label="Options", menu=options_menu)

        helpmenu = Menu(menu, tearoff=0)
        helpmenu.add_command(label="Game Rules", command=game_rules)
        helpmenu.add_command(label="GitHub Repository", command=github_link)
        helpmenu.add_command(label="About...", command=about)
        menu.add_cascade(label="Help", menu=helpmenu)

        self.__main_window.config(menu=menu)

        # matrix to contain all the buttons and labels for opponent playing
        # field and own playing field
        # initialize 10 empty rows
        self.__field_buttons = [[] for _ in range(10)]
        self.__field_labels = [[] for _ in range(10)]

        player_name_label = Label(self.__main_window,
                                  text="Player: "
                                       f"{self.__player}",
                                  justify=LEFT,
                                  font=("Arial", 15))
        player_name_label.grid(row=0, column=0, sticky=W)

        opponent_field_label = Label(self.__main_window,
                                     text="Opponent's field:",
                                     justify=LEFT,
                                     font=("Arial", 13))
        opponent_field_label.grid(row=1, column=0, sticky=W, padx=(10, 0),
                                  pady=(10, 0))

        my_field_label = Label(self.__main_window,
                               text="Your field:",
                               justify=LEFT,
                               font=("Arial", 13))
        my_field_label.grid(row=1, column=1, sticky=W, padx=(5, 0),
                            pady=(10, 0))

        # 10x10 matrix of buttons corresponding to the opponent's playing field
        # associate each button with a function and
        # predetermined arguments (x, y)
        opponent_field_frame = Frame(self.__main_window)
        opponent_field_frame.grid(row=2, column=0, padx=(10, 0))
        for y in range(10):
            for x in range(10):
                # store each button for future configuration
                self.__field_buttons[y].append(
                    Button(opponent_field_frame,
                           text=field_name(x, y),
                           command=partial(self.field_button, x, y),
                           bg=PLAYING_FIELD_COLORS["water"],
                           width=4))
                self.__field_buttons[y][x].grid(row=y, column=x, padx=2,
                                                pady=2)

        # 10x10 matrix of labels corresponding to own playing field
        my_field_frame = Frame(self.__main_window)
        my_field_frame.grid(row=2, column=1, padx=(0, 10), sticky=N + E)
        for y in range(10):
            for x in range(10):
                # store each label for future configuration
                self.__field_labels[y].append(
                    Label(my_field_frame,
                          text=field_name(x, y), width=4,
                          bg=self.get_field_color(x, y)))
                self.__field_labels[y][x].grid(row=y, column=x, padx=2, pady=2)

        # checkbox to toggle the visibility of own game field
        self.__hidden_field = IntVar(my_field_frame, 1)
        toggle_hide_field = Checkbutton(my_field_frame,
                                        text="Hide Own Playing field",
                                        variable=self.__hidden_field,
                                        command=self.toggle_hide_field)
        toggle_hide_field.grid(row=10, column=0, columnspan=10)
        # start off as selected (hidden field)
        toggle_hide_field.select()
        # hide the playing field by running the method
        self.toggle_hide_field()

        # frame to contain four color code labels
        color_codes_frame = Frame(self.__main_window)
        color_codes_frame.grid(row=3, column=0)

        water_color_code = Label(color_codes_frame,
                                 text="Water",
                                 justify=LEFT,
                                 font=("Arial", 11),
                                 fg=PLAYING_FIELD_COLORS["water"])
        water_color_code.grid(row=0, column=0, padx=10)

        hit_color_code = Label(color_codes_frame,
                               text="Hit Ship",
                               justify=LEFT,
                               font=("Arial", 11),
                               fg=PLAYING_FIELD_COLORS["hit"])
        hit_color_code.grid(row=0, column=1, padx=10)

        miss_color_code = Label(color_codes_frame,
                                text="Missed Shot",
                                justify=LEFT,
                                font=("Arial", 11),
                                fg=PLAYING_FIELD_COLORS["miss"])
        miss_color_code.grid(row=0, column=2, padx=10)

        ship_color_code = Label(color_codes_frame,
                                text="Your Ship",
                                justify=LEFT,
                                font=("Arial", 11),
                                fg=PLAYING_FIELD_COLORS["ship"])
        ship_color_code.grid(row=0, column=3, padx=10)

        # scrolled text widget to contain the game log
        self.__log_field = scrolledtext.ScrolledText(self.__main_window,
                                                     font=("Arial", 8),
                                                     width=60, height=10)
        self.__log_field.grid(row=4, column=0, padx=(10, 0), pady=(5, 20),
                              sticky=N + W)

        self.__stats_label = Label(self.__main_window,
                                   justify=LEFT,
                                   font=("Arial", 10))
        self.__stats_label.grid(row=4, column=1, padx=(0, 10), pady=(10, 0),
                                sticky=N + W + E)

        # event handler for the user closing the window with
        self.__main_window.protocol("WM_DELETE_WINDOW", self.forfeit_game)

    def field_button(self, x, y):
        """
        Gets ran when the player presses a button (fires a shot)
        on the opponent's field.
        Handles the coloring of gui elements for hits and misses
        :param x: int, playing field x coordinate
        :param y: int, playing field y coordinate
        """

        # ingore press if game has already ended
        if GAME_LOGIC.game_ended():
            return

        # disable buttons since player's turn ends
        self.disable_buttons()

        # fire a shot and return whether it was a hit or not
        hit = GAME_LOGIC.fire_shot(x, y, self.__player)

        if hit:
            color = PLAYING_FIELD_COLORS["hit"]
        else:
            color = PLAYING_FIELD_COLORS["miss"]

        opponent_game_window = self.__opponent.get_game_window()

        # if hit and ships sink from one hit
        if hit and GAME_LOGIC.sink_from_one():

            # get the hit ship
            hit_ship = GAME_LOGIC.get_ship(x, y, self.__opponent)

            # for each ship's part's coordinate
            for coord in hit_ship.get_coords():
                coord_x = coord[0]
                coord_y = coord[1]

                # mark each button/label with the correct color
                self.__field_buttons[coord_y][coord_x].config(state=DISABLED,
                                                              bg=color)
                if not opponent_game_window.hidden_field():
                    opponent_game_window.set_label_color(coord_x, coord_y,
                                                         color)
        else:
            self.__field_buttons[y][x].config(state=DISABLED, bg=color)
            if not opponent_game_window.hidden_field():
                opponent_game_window.set_label_color(x, y, color)

        if not GAME_LOGIC.game_ended():
            # enable opponent's buttons since their turn starts
            self.__opponent.get_game_window().enable_buttons()

    def toggle_hide_field(self):
        """
        Toggles the visibility of own game field
        Runs when checked state of the associated checkbox is changed
        """

        # Set each field to water color
        if self.__hidden_field.get() == 1:
            for x in range(10):
                for y in range(10):
                    self.__field_labels[y][x].config(
                        bg=PLAYING_FIELD_COLORS["water"])

        # set each field back to correct color
        else:
            for x in range(10):
                for y in range(10):
                    color = self.get_field_color(x, y)
                    self.__field_labels[y][x].config(bg=color)

    def disable_buttons(self):
        """
        Disables all game field buttons
        Used when a player finishes their turn
        """

        for x in range(10):
            for y in range(10):
                self.__field_buttons[y][x].config(state=DISABLED)

    def enable_buttons(self):
        """
        Enables all (expect already used) buttons
        Used when a player gets their turn
        """

        opponent_field = self.__opponent.get_playing_field()

        for x in range(10):
            for y in range(10):
                playing_field_state = opponent_field[y][x]
                # if water or a non-hit ship
                if playing_field_state == 0 or playing_field_state == 1:
                    self.__field_buttons[y][x].config(state=NORMAL)

    def forfeit_game(self):
        """
        Handles the user wanting to forfeit
        Gets ran when the user presses the forfeir option or closes the window
        """

        # ingore press if game has already ended
        if GAME_LOGIC.game_ended():
            self.destroy()

        if messagebox.askyesno("Are you sure?", "Are you sure you want "
                                                "to forfeit the game?"):
            GAME_LOGIC.forfeit_game(self.__player)
            self.destroy()

    def exit_main_menu(self):
        """
        Exits to main menu
        """
        if messagebox.askyesno("Are you sure?", "Are you sure you want "
                                                "to exit to the main menu?"):
            PLAYERS.clear()
            self.destroy()
            self.__opponent.get_game_window().destroy()
            SettingsWindow()

    def exit_application(self):
        """
        Exits the whole application
        """
        if messagebox.askyesno("Are you sure?", "Are you sure you want "
                                                "to exit the application?"):
            self.destroy()
            self.__opponent.get_game_window().destroy()

    def append_log(self, msg):
        """
        Appends the specified message to the log
        :param msg:     string, message to append
        """

        # insert at end
        self.__log_field.insert(END, msg + "\n---\n")
        self.__log_field.yview(END)  # scroll to end

    def update_stats(self, stats):
        """
        Updates the statistics label
        :param stats:   string, stats to update with
        """

        self.__stats_label.config(text=stats)

    def set_label_color(self, x, y, color):
        """
        Sets a color to your own playing field
        :param x:       int, own playing field x coordinate
        :param y:       int, own playing field y coordinate
        :param color:   str, color to be set
        """

        self.__field_labels[y][x].config(bg=color)

    def get_field_color(self, x, y):
        """
        Get the appropriate field color for the specified x y coordinates
        :param x:   int,    field x coordinate
        :param y:   int,    field y coordinate
        :return:    string, word or hex representation of the color
        """

        field = self.__player.get_playing_field()[y][x]

        if field == 0:
            return PLAYING_FIELD_COLORS["water"]

        if field == 1:
            return PLAYING_FIELD_COLORS["ship"]

        if field == 2:
            return PLAYING_FIELD_COLORS["hit"]

        if field == 3:
            return PLAYING_FIELD_COLORS["miss"]

    def hidden_field(self):
        """
        Returns whether or not the label game field is currently hidden
        :return: bool,  True  = game field hidden
                        False = game field visible
        """

        return self.__hidden_field.get() == 1

    def mainloop(self):
        """
        Starts the gui mainloop
        """

        self.__main_window.mainloop()

    def destroy(self):
        """
        Destroys the gui
        """

        if not self.__destroyed:
            self.__main_window.destroy()
            self.__destroyed = True


class GameLogic:
    """
    A class to handle the game logic
    """

    def __init__(self, sink_option, player1, player2):
        """
        Constructor, creates the game logic object
        :param sink_option:   bool,   True  = ships sink from one hit
                                      False = ships sink once all parts are hit
        :param player1:       Player, player object for first player
        :param player2:       Player, player object for second player
        """

        self.__sink_from_one = sink_option
        self.__player1 = player1
        self.__player2 = player2
        self.__game_ended = True

    def sink_from_one(self):
        """
        Returns whether or not the game option for ships
        sinking for one hit is enabled
        :return:    bool,   True    = enabled
                            False   = disabled
        """

        return self.__sink_from_one

    def get_opponent(self, player):
        """
        Returns the opponent of the specified player
        :param player:  Player, player object identifying the caller
        """

        # we can simply indentify by name,
        # since same name was disallowed
        if str(self.__player1) == str(player):
            return self.__player2
        else:
            return self.__player1

    def start_game(self):
        """
        Starts the game
        """

        self.__game_ended = False

        # randomly get which player starts the game
        player = [self.__player1, self.__player2][randrange(2)]

        self.get_opponent(player).get_game_window().disable_buttons()

        msg = f"Welcome to Battleships!\n{player} starts the game."

        # add log message to both game windows
        self.__player1.get_game_window().append_log(msg)
        self.__player2.get_game_window().append_log(msg)

        self.update_statistics()

    def forfeit_game(self, player):
        """
        Handle the specified player forfeiting the game
        :param player: Player,  the loser's player object
        """

        opponent = self.get_opponent(player)

        # add log message to winner's game window
        opponent.get_game_window().append_log(f"{player} has forfeited the "
                                              f"game.\n{opponent} is the "
                                              f"winner!")
        self.__game_ended = True

    def game_ended(self):
        """
        Returns whether the game has ended or not
        :return: bool,  True    = game ended
                        False   = game running
        """

        return self.__game_ended

    def declare_winner(self, player):
        """
        Declare the specified player as the winner of the game
        :param player: Player, winner's player object
        """

        self.update_statistics()

        msg = f"{player} has won the game!"

        # add log message to both game windows
        self.__player1.get_game_window().append_log(msg)
        self.__player2.get_game_window().append_log(msg)

        self.__game_ended = True

    def fire_shot(self, x, y, firer):
        """
        Fires a shot on the opponents playing field
        Returns whether it was a hit or not
        :param x:       int,    opponent playing field x coordinate
        :param y:       int,    opponent playing field y coordinate
        :param firer:   Player, who fired the shot
        :return:        bool,   True  = hit
                                False = miss
        """

        opponent = self.get_opponent(firer)

        # when we're checking this, the field could only possibly be
        # water or a ship part
        hit = opponent.get_playing_field()[y][x] == 1

        firer.increment_shots()

        opponent.update_playing_field(x, y, hit)

        if hit:
            firer.increment_hits()
            opponent.increment_hits_taken()

            # get ship under these coordinates
            ship = self.get_ship(x, y, opponent)

            # if ship has no parts left
            if ship.assign_hit(x, y, self.__sink_from_one) == 0:
                # if the last ship was destroyed
                if opponent.decrease_ship_count() == 0:
                    self.announce_shot(firer, x, y, hit, ship)
                    self.declare_winner(firer)
                    return hit

            self.announce_shot(firer, x, y, hit, ship)
        else:
            self.announce_shot(firer, x, y, hit)

        self.update_statistics()

        return hit

    def announce_shot(self, firer, x, y, hit, ship=None):
        """
        Announces a hit or a miss to the game windows' logs
        :param firer:   Player,     player object of the firer
        :param x:       int,        playing field x coordinate
        :param y:       int,        playing field x coordinate
        :param hit:     bool,       True  = hit,    False = miss
        :param ship:    Battleship, battleship object if there was a hit
                                    defaults to None
        """

        msg = f"{firer} fired a shot on {field_name(x, y)}..."
        if hit:
            opponent = self.get_opponent(firer)
            msg += f"\n{opponent}'s {ship} was HIT!"

            # how many parts left in the ship
            parts_left = ship.get_size() - ship.hits_taken()
            if parts_left == 1:
                msg += f"\nOne more hit and the {ship} will be destroyed!"
            elif parts_left == 0:
                ships_left = opponent.ships_left()

                # add "only" if less than 3 ships, and don't add "s"
                # to "ships" if only one ship left
                msg += f"\n{ship} got destroyed! " \
                       f"{'Only ' if ships_left < 3 else ''}{ships_left} " \
                       f"ship{'s' if ships_left > 1 else ''} left!"
        else:
            msg += "\nMISS!"

        # add log message to both game windows
        self.__player1.get_game_window().append_log(msg)
        self.__player2.get_game_window().append_log(msg)

    def update_statistics(self):
        """
        Produces the statistics to display for each player
        """

        # two players, update both statistics
        for i in range(2):
            player = [self.__player1, self.__player2][i]

            shots_fired = player.shots_fired()
            shots_hit = player.shots_hit()
            shots_missed = shots_fired - shots_hit

            if shots_fired == 0:
                hit_percent = f"0 %"
                miss_percent = f"0 %"
            else:
                hit_percent = f"{int(shots_hit / shots_fired * 100)} %"
                miss_percent = f"{int(shots_missed / shots_fired * 100)} %"

            hits_taken = player.hits_taken()
            ships_left = player.ships_left()

            # for each ship type, for each ship in ship type
            ship_parts_left = \
                sum([sum([ship.parts_left() for ship in ship_type])
                     for ship_type in player.get_battleships().values()])

            stats = f"Shots fired: {shots_fired}\n" \
                    f"Shots hit: {shots_hit} ({hit_percent})\n" \
                    f"Shots missed: {shots_missed} ({miss_percent})\n" \
                    f"Hits taken: {hits_taken}\n" \
                    f"Ships left: {ships_left}\n" \
                    f"Ship parts left: {ship_parts_left}"

            player.get_game_window().update_stats(stats)

    def get_ship(self, x, y, owner):
        """
        Gets the ship at these xy coordinates
        Optionally get the opponent's ship
        :param x:           int,        x coordinate
        :param y:           int,        y coordinate
        :param owner:       Player,     player object, owner of the ship
        :return:            Battleship, battleship object
        """

        battleships = owner.get_battleships()
        coord = (x, y)

        # check all ships for a matching coordinate
        for ship_type in battleships:
            # there can be more than one ship per ship type
            for ship in battleships[ship_type]:
                if coord in ship.get_coords():
                    return ship


def get_column(array, x, start, end):
    """
    Gets values from a column in a matrix/2d array
    :param array:   array, array to get values from
    :param x:       int, x coordinate
    :param start:   int, zero-based y start value
    :param end:     int, zero-based y end value
    :return:        array, values from the column
    """
    return [row[x] for row in array[start:end + 1]]


def field_name(x, y):
    """
    Returns the name of a playing field field from its x and y coordinates
    e.g. A7, G8, B3,..
    :param x:   int, playing field x coordinate
    :param y:   int, playing field y coordinate
    :return:    str, name of field
    """

    return f"{X_FIELDS[x]}{y + 1}"


def game_rules():
    """
    Opens the Battleships wikipedia page in default browser
    """

    webbrowser.open("https://en.wikipedia.org/wiki/Battleship_(game)")

def github_link():
    """
    Opens the GitHub repository for this program
    """
    
    webbrowser.open("https://github.com/0x464e/battleships-py")

def about():
    """
    Displays information about this applications
    """

    messagebox.showinfo("About", "Battleships game v0.1\n\n"
                                 "Made by Otto for\nTampere "
                                 "University programming\n"
                                 "course COMP.CS.100\n\n"
                                 "8th of December 2020")


def main():
    """
    Entrypoint to the program
    """

    # if program icon is not found
    if not os.path.exists("icon.ico"):
        global ICON_MISSING
        ICON_MISSING = True

    SettingsWindow()


if __name__ == "__main__":
    main()
