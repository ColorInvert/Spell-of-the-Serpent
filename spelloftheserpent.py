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


#! FUNCTIONS

#! SCREEN SIZE AND STANDARDIZATION SUBFUNCTIONS

# ? Disclosure: The terminal size commands were created by Chat GPT, and are thus, potentially in violation of copyright. Let me know if you are a holder and have issue with any of these, I am open to dialog, and changes that achieve equivalence.


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


#! RENDERING FUNCTIONS


# Pulls the information out of an enemy.txt file and parses it in prep for
# the function render_hook_textfield(). See ABOUT_enemy_txt.md for details on parsing method.
def get_enemy_data(dungeon,enemy):

    regex = r'!ROUND!\n([\s\S]*?)(?=\n!ROUND!|$)'
    
    with open(f"data/{dungeon}/enemies/{enemy}.txt", "r") as file:
        contents = file.read()
    
    round_list = re.findall(regex, contents)
    print(f"roundlist is {round_list}")


# Replace all placeholder text sockets with current payload screen data.
# ?Please see uitemplate.utf8ans for reference on which textspace each letter
# ?corresponds to.
def render_hook_textfield(a, b, c, d, e, f, g, h, i, j, k):

    # Get template render to draw our data over
    new_frame = rend

    #! CHARACTER COUNTS FOR EACH SOCKET:
    # sprite_row (a-f) 12
    # enemy_socket (g) 14
    # desc_1(h) 31
    # desc_2(i) 31
    # desc_3(j) 31
    # demand(k) 31

    # Replace each line of the portrait
    new_frame = re.sub(r"aaaaaaaaaaaa", a)
    new_frame = re.sub(r"bbbbbbbbbbbb", b)
    new_frame = re.sub(r"cccccccccccc", c)
    new_frame = re.sub(r"dddddddddddd", d)
    new_frame = re.sub(r"eeeeeeeeeeee", e)
    new_frame = re.sub(r"ffffffffffff", f)

    # Enemy name
    new_frame = re.sub(r"gggggggggggggg", g)

    # Top 3 grey lines of description
    new_frame = re.sub(r"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", h)
    new_frame = re.sub(r"iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", i)
    new_frame = re.sub(r"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", j)

    # Typing demand section of text box (magenta text user has to type for attack)
    new_frame = re.sub(r"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", k)

    return new_frame


# ?To be called after all screenspace text replacements are complete for the frame
def render_ui():

    with open("data/System/uitemplate.utf8ans", "r") as file:
        contents = file.read()
        print(contents)


# ? Disclosure, these next two were chat GPT as well.
def clear_screen():
    os.system('printf "\033[?7l"')  # Disable line wrap
    # ANSI escape code to clear the entire screen
    print("\033[2J")


def move_cursor(row, col):
    # ANSI escape code to move the cursor to a specific position
    print(f"\033[{row};{col}H", end="")


def hide_cursor():
    print("\033[?25l", end="")  # ANSI escape code to hide the cursor


def show_cursor():
    print("\033[?25h", end="")  # ANSI escape code to show the cursor


def enable_line_wrap():
    os.system('printf "\033[?7h"')  # Enable line wrap


#!INPUT FUNCTIONS


# Run a pyinputplus timed input prompt, default timeout 10 seconds default attempts 1.
# input will be compared after allcapsing and space-removing their entry AND the
# type attack's entry. This allows type attack phrase to have spaces or unusual caps
def type_attack(phrase, time=10, tries=1):

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

    # Does attackphrase and user response match?
    elif response == phrase:
        print("hey good job you managed to type that right")

    else:
        print("ACTION FUMBLED! -1 HP!")


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

    initial_setup()



    render_ui()


    # type_attack("B aSh    With SHIELD  ", 5)
    time.sleep(3.5)
    get_enemy_data("Tomb Of The Lost", "skeleton")
    time.sleep(3.5)
    



