# Battleships

A Python Tkinter GUI game for the classic [Battleships game](https://en.wikipedia.org/wiki/Battleship_(game)).  
I made this game for the final project of my university's *introduction to programming* -course.  
The assignment was to create some GUI program with Tkinter.

---

The game is best played on two monitors, but also works on a single monitor due to the ability to hide your playing field.

Certain programming choices may have been made with a more featureful game in mind, but ran I out of time.
Still, this is a fully functional first version of the game

Start off by naming both players and choosing if you want ships to sink from one hit.  
By default ships sink once each part (size = parts) of them is hit.

Then the first player starts placing in their battleships.  
The second player stands by meanwhile.  
Number of battleships, and their size, is hardcoded for now:  
* 1x Carrier      (size 5)
* 1x Battleship   (size 4)
* 2x Cruiser      (size 3)
* 2x Destroyer    (size 2)
* 2x Submarine    (size 1)

Ships are placed by clicking a corresponding button on the play field.  
Start from the top left corner of the ship.

Ship can be placed horizontally and vertically. Ships can't overlap or touch, but you don't have to worry about this, the game window doesn't allow invalid placements.  
In some rules even corners of ships can't touch, but in these rules they can.

If your chosen placement has both horizontal and vertical placements available,
choose the orientation by pressing the button next to, or under, the first
button you pressed.  
If only one orientation is available at your chosen placement, the whole rest of the ship is automatically placed in.

Once you have placed in all your ships, the second player and start placing
their ships.

Once the second player finishes their ship placements, the two main game windows are opened.  
The players' own fields are hidden by default, be sure to unhide them when appropriate by unchecking the checkbox.

Drag the other game window to your second monitor and face the monitors away from each other and start playing.  
If you don't have a second monitor, work with the field hiding checkbox.

Fire shots by clicking on the buttons on the left of your game window.  
Color codes indicate what happened to your shots.  
See your own ship placements and opponent's shots from the grid on the right  
(But be sure to unhide the field first!)

Winner is the first person to destroy all each of the opponent's ships.  
Or a player can also forfeit.

![image](https://i.imgur.com/TJymvgC.gif)

## Installing & Running
* Install [Python 3+](https://www.python.org/)
* Clone this repository  
`git clone https://github.com/0x464e/battleships-py`
* Run `battleships.py` with e.g the command line command  
`python3 battleships.py`