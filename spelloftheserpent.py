from rich.console import Console

# from rich.prompt import Prompt
# from rich.table import Table
import re
import os
import time
import shutil
import sys


# FUNCTIONS

# SCREEN SIZE AND STANDARDIZATION SUBFUNCTIONS

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


# SCREEN SIZE REFORMATTING FUNCTION
def initial_setup():

    # Desired terminal size.
    #!Typical monospace console font is 2x tall as wide, so width should be double height.
    #!
    desired_window_width = 60
    desired_window_height = 30

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
            "Failed to resize the terminal to the desired dimensions. Please manually set your terminal to the correct size. This program will now exit"
        )
        quit()

    print("here is 2.5 seconds for you to look at formatting automatically achieved.")
    time.sleep(2.5)


console = Console()
if __name__ == "__main__":
    print("runs, anyway.")

    initial_setup()

    # # Desired terminal size.
    # #!Typical monospace console font is 2x tall as wide, so width should be double height.
    # desired_window_width = 60
    # desired_window_height = 30

    # # Attempt to resize the terminal
    # resize_terminal(desired_window_height, desired_window_width)

    # # Introduce a short delay to allow the terminal to resize,
    # # inform user that loading is in progress
    # print("NOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...\nNOW LOADING...")
    # time.sleep(0.4)  # 0.4 second delay

    #   # Move the cursor to the top-left corner
    # move_cursor_to_top_left()

    # #Clear existing contents of terminal in prep for our own rendering
    # clear_terminal()

    # # Verify the terminal size
    # terminal_size = shutil.get_terminal_size()
    # x = terminal_size.columns
    # y = terminal_size.lines

    # # Print the terminal size to verify
    # print(f"x size of terminal is {x}")
    # print(f"y size of terminal is {y}")

    # # Check if the resize was successful
    # if y == desired_window_height and x == desired_window_width:
    #     console.print("Terminal resized successfully.")
    # else:
    #     console.print("Failed to resize the terminal to the desired dimensions. Please manually set your terminal to the correct size. This program will now exit")
    #     quit()

    # print("here is 2.5 seconds for you to look at formatting automatically achieved.")
    # time.sleep(2.5)
