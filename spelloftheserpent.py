from rich.console import Console
import keyboard
from threading import Timer

# from rich.prompt import Prompt
# from rich.table import Table
import re
import os
import time
import shutil
import sys
import pyinputplus as pyip

# GAME RESOLUTION IS LOCKED IN, 42 COL x 18+1 ROWS


#!GLOBAL VARIABLES


# Pull the uitemplate.utf8ans file directly, return contents as variable.
def get_template():
    with open("data/System/uitemplate.utf8ans", "r") as file:
        contents = file.read()
    return contents


# Current render data. starting value is the contents of uitemplate.utf8ans.
rend = get_template()

# Holds a list of remaining round data, after a enemy.txt file has been loaded
pending_rounds = []

# Most recently loaded enemy file. Contains full .txt's contents
current_enemy = None

# An updating version of the current render frame. Rendering takes place in steps, so this
# changes rapidly before the final frame is rendered, and is overridden when a new frame
# needs to be processed.
current_frame = None

# Player's health. Number of mistakes player is allowed to make in the span of the session.
hp = 3


#! FUNCTIONS

#! SCREEN SIZE AND STANDARDIZATION SUBFUNCTIONS

# ? Disclosure: The terminal size commands were created by Chat GPT, and are thus, potentially plagiarization.


def resize_terminal(rows, columns):
    """Attempt to resize the terminal window."""
    if sys.platform != "win32":
        resize_command = f"\033[8;{rows};{columns}t"
        print(resize_command)
        os.system(
            f'echo -e "{resize_command}"'
        )  # Ensuring the escape sequence is correctly interpreted


def clear_terminal():
    """Clear the terminal window."""
    os.system("clear" if sys.platform != "win32" else "cls")


def move_cursor_to_top_left():
    """Move the cursor to the top-left corner of the terminal window."""
    print("\033[H", end="")


#! SCREEN SIZE REFORMATTING FUNCTION
def initial_setup():

    # Desired terminal size.
    #!Typical monospace console font is 2x tall as wide, so width should be double height.
    #! HOWEVER, ONE LINE IS RESERVED FOR TYPING, AS IF A RENDER IS PERFORMED, A NEW LINE
    #! WILL ALWAYS BE CREATED BELOW IT.
    desired_window_width = 42
    desired_window_height = 19

    # Attempt to resize the terminal
    resize_terminal(desired_window_height, desired_window_width)

    # Introduce a short delay to allow the terminal to resize,
    # inform user that loading is in progress
    print(
        "NOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING..."
    )
    time.sleep(0.4)  # 0.4 second delay

    # Move the cursor to the top-left corner
    move_cursor_to_top_left()

    # Clear existing contents of terminal in prep for our own rendering
    clear_terminal()

    # Verify the terminal size
    terminal_size = shutil.get_terminal_size()
    x = terminal_size.columns
    y = terminal_size.lines

    # Print the terminal size to verify
    print(f"x size of terminal is {x}")
    print(f"y size of terminal is {y}")

    # Check if the resize was successful
    if y == desired_window_height and x == desired_window_width:
        console.print("Terminal resized successfully.")
    else:
        console.print(
            "Failed to resize the terminal to the desired dimensions. Please manually set your terminal to the correct size. This program will now exit."
        )
        quit()


#! GAME FLOW/SYSTEM FUNCTIONS

# Pulls the information out of an enemy.txt file and parses it in prep for
# the function render_hook_textfield(). See ABOUT_enemy_txt.md for details on parsing method.
def load_enemy_file(dungeon, enemy):

    # Regex that parses a properly formatted enemy.txt file
    regex = r"!ROUND!\n([\s\S]*?)(?=\n!ROUND!|$)"

    # Get arguments for dungeon and enemy name, transform into a relative path and open file.
    with open(f"data/{dungeon}/enemies/{enemy}.txt", "r") as file:
        contents = file.read()

    # Update global variable current enemy with full contents of just-loaded enemy file.
    global current_enemy
    current_enemy = contents

    # Update global variable pending rounds with a list of rounds from this enemy file
    global pending_rounds
    pending_rounds = re.findall(regex, contents)

#! RENDERING FUNCTIONS

# With enemy data loaded, and a round in the pending_rounds variable, play a round of combat.
def play_next_round():

    try:
        current_round = pending_rounds.pop(0)

    except:
        print("ROUNDS LIST IS EMPTY!!!!! THIS SHOULD NEVER HAPPEN! BUG THIS!")

    # Extract all lines of the sprite from the top of the enemy file.
    sprite = current_enemy[0:77]

    # Split sprite into constituent rows to make a list of them.
    sprite_payloads = sprite.split("\n")

    # Turn each sprite row into it's lettercode variable
    a = sprite_payloads[0]
    b = sprite_payloads[1]
    c = sprite_payloads[2]
    d = sprite_payloads[3]
    e = sprite_payloads[4]
    f = sprite_payloads[5]

    # Get the next round in the queue, split into payload segments for screen rendering
    text_payloads = current_round.split("\n")

    # ? Usage of .center() in the next section is to ensure we don't end up short any chars
    # ? in rendering during the process of template replacement

    # Grab the 7th line of the loaded enemy file, which has the enemy display name, and
    # center it.
    g = current_enemy.splitlines()[6].center(14)

    # h through j are the 3 description lines, in order from top to bottom.
    h = text_payloads[0].center(31)
    i = text_payloads[1].center(31)
    j = text_payloads[2].center(31)

    # k is the player demand, which is left justified to match with where input occurs. 
    k = text_payloads[3].ljust(31)

    # l is the ACTUAL text input being looked for, which in *most* cases should
    # just be the same as k. tricky enemies might ask you to do one thing
    # and actually want you to do something else to win the fight.
    l = text_payloads[4]

    # The time limit for current typing challenge
    m = float(text_payloads[5])

    # With all elements parsed and split, send to render process for display.
    render_hook_textfield(a, b, c, d, e, f, g, h, i, j, k)

    #with render complete, perform current combat round. One try.
    type_attack(l,m)


# Replace all placeholder text sockets with current payload screen data.
# ?Please see uitemplate.utf8ans for reference on which textspace each letter
# ?corresponds to.
def render_hook_textfield(a, b, c, d, e, f, g, h, i, j, k):

    # Get template render to draw our data over
    new_frame = rend

    #? CHARACTER COUNTS FOR EACH SOCKET:
    #? sprite_row (a-f) 12
    #? enemy_socket (g) 14
    #? desc_1(h) 31
    #? desc_2(i) 31
    #? desc_3(j) 31
    #? demand(k) 31

    # Replace each line of the portrait
    new_frame = re.sub(r"aaaaaaaaaaaa", a, new_frame)
    new_frame = re.sub(r"bbbbbbbbbbbb", b, new_frame)
    new_frame = re.sub(r"cccccccccccc", c, new_frame)
    new_frame = re.sub(r"dddddddddddd", d, new_frame)
    new_frame = re.sub(r"eeeeeeeeeeee", e, new_frame)
    new_frame = re.sub(r"ffffffffffff", f, new_frame)

    # Enemy name
    new_frame = re.sub(r"gggggggggggggg", g, new_frame)

    # Top 3 grey lines of description
    new_frame = re.sub(r"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", h, new_frame)
    new_frame = re.sub(r"iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", i, new_frame)
    new_frame = re.sub(r"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", j, new_frame)

    # Typing demand section of text box (magenta text user has to type for attack)
    new_frame = re.sub(r"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", k, new_frame)

    render(new_frame)


# ? This is a bit silly, but it feels right to have this redundancy instead of printing
# ? directly
def render(frame):
    print(frame)


#!INPUT FUNCTIONS


#TODO, LINK THIS INTO THE PLAY NEXT ROUND FUNCTION
def type_attack(phrase, time=10, tries=1):

    #Hook to our player health variable
    global hp

    # Sanitize attack phrase
    phrase = sanitize_string(phrase)
    # print(f"sanitized phrase is {phrase}")
    # prompt user for text command based on params
    response = pyip.inputStr("  ", default="NULL", timeout=time, limit=tries)

    # Sanitize user response
    response = sanitize_string(response)
    # print(f"sanitized response is {response}")

    # Did they time out?
    if response == "NULL":
        print("YOU TOOK TOO LONG! -1 HP!")
        
        hp = hp - 1

    # Does attackphrase and user response match?
    elif response == phrase:
        print("hey good job you managed to type that right")

    else:
        print("ACTION FUMBLED! -1 HP!")
        hp = hp - 1


#!INPUT SUBFUNCTIONS


# Removes spaces, and allcaps-ifies strings, for use in type_attack() string
# comparisons.
def sanitize_string(string):
    # remove spaces
    string = string.replace(" ", "")
    string = string.upper()
    return string


# ? MAIN BODY

console = Console()
if __name__ == "__main__":

    # Get screen ready
    initial_setup()

    # Load enemy
    load_enemy_file("Tomb Of The Lost", "skeleton")


    while pending_rounds:
        if hp == 0:
            print("You have died! Game over!")
            quit()
        play_next_round()
    print("We have escaped the while loop of combat.")

    # time.sleep(2.0)
    # render_ui()
