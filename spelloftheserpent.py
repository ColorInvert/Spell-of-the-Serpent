
#? Project created by Casey Glidewell.
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

# Creates a baseline blank version of the ui, without the textfield hooks.
def create_blank():

    global template
    blank = template

    sprite_row_blank = "            "
    enemy_blank = "              "
    desc_blank = "                               "

    blank = blank.replace("aaaaaaaaaaaa", sprite_row_blank)
    blank = blank.replace("bbbbbbbbbbbb", sprite_row_blank)
    blank = blank.replace("cccccccccccc", sprite_row_blank)
    blank = blank.replace("dddddddddddd", sprite_row_blank)
    blank = blank.replace("eeeeeeeeeeee", sprite_row_blank)
    blank = blank.replace("ffffffffffff", sprite_row_blank)


    # Enemy name
    blank = blank.replace("gggggggggggggg",enemy_blank)

    # Top 3 grey lines of description
    blank = blank.replace("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", desc_blank)
    blank = blank.replace("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", desc_blank)
    blank = blank.replace("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", desc_blank)

    # Typing demand section of text box (magenta text user has to type for attack)
    blank = blank.replace("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", desc_blank)
    return blank

# Template render data. value is uitemplate.utf8ans. never changes.
template = get_template()

# Blank version of template data. To be rendered first, with text being subbed in.
blank_template = create_blank()

# Holds a list of remaining round data, after a enemy.txt file has been loaded
pending_rounds = []

# Most recently loaded enemy file. Contains full .txt's contents
current_enemy = None

# An updating version of the current render frame. Rendering takes place in steps, so this
# changes rapidly before the final frame is rendered, and is overridden when a new frame
# needs to be processed.
current_frame = None

# Saves all template screen's text entry sockets into a list. A socket is a tuple of string
# start and end position where the text can go.
socket_list = []

def get_hook_sockets():

    # Get template render to find sockets of
    global template

    global socket_list

    # Individual rows of enemy sprites
    socket_list.append(re.search(r"aaaaaaaaaaaa", template).span())
    socket_list.append(re.search(r"bbbbbbbbbbbb", template).span())
    socket_list.append(re.search(r"cccccccccccc", template).span())
    socket_list.append(re.search(r"dddddddddddd", template).span())
    socket_list.append(re.search(r"eeeeeeeeeeee", template).span())
    socket_list.append(re.search(r"ffffffffffff", template).span())
    
    # Enemy name
    socket_list.append(re.search(r"gggggggggggggg", template).span())

    # Top 3 grey lines of description
    socket_list.append(re.search(r"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", template).span())
    socket_list.append(re.search(r"iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii", template).span())
    socket_list.append(re.search(r"jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", template).span())
    
    # Typing demand section of text box (magenta text user has to type for attack)
    socket_list.append(re.search(r"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk", template).span())

get_hook_sockets()


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
        print("Terminal resized successfully.")
    else:
        print(
            "Failed to resize the terminal to the desired dimensions. Please manually set your terminal to the correct size. This program will now exit."
        )
        quit()

    get_hook_sockets()

#! GAME FLOW/SYSTEM FUNCTIONS

# Pulls the information out of an enemy.txt file and parses it in prep for
# the function render_game(). See ABOUT_enemy_txt.md for details on parsing method.
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

    #Set current round to the next queued item in the pending_rounds list
    try:
        current_round = pending_rounds.pop(0)

    except:
        print("ROUNDS LIST IS EMPTY!!!!! THIS SHOULD NEVER HAPPEN! BUG THIS!")


    payload_list = []
    # Extract all lines of the sprite from the top of the enemy file.
    sprite = current_enemy[0:77]

    # Split sprite into constituent rows to make a list of them.
    sprite_payloads = sprite.split("\n")

    #add each row of the sprite to the payload list
    for i in range(len(sprite_payloads)):
        payload_list.append(sprite_payloads[i])

    
    # Get the next round in the queue, split into payload segments for screen rendering
    text_payloads = current_round.split("\n")

    # ? Usage of .center() in the next section is to ensure we don't end up short any chars
    # ? in rendering during the process of template replacement

    # Grab the 7th line of the loaded enemy file, which has the enemy display name, and
    # center it.
    payload_list.append(current_enemy.splitlines()[6].center(14))

    # h through j are the 3 description lines, in order from top to bottom.
    payload_list.append(text_payloads[0].center(31))
    payload_list.append(text_payloads[1].center(31))
    payload_list.append(text_payloads[2].center(31))

    # k is the player demand, which is left justified to match with where input occurs. 
    payload_list.append(text_payloads[3].ljust(31))

    # l is the ACTUAL text input being looked for, which in *most* cases should
    # just be the same as k. tricky enemies might ask you to do one thing
    # and actually want you to do something else to win the fight.
    demand = (text_payloads[4])

    # The time limit for current typing challenge
    time_limit = (float(text_payloads[5]))

    # With all elements parsed and split, send to render process for display.
    render_game(payload_list)

    #With render complete, perform combat round with data from last 2items of payload list.
    type_attack(demand, time_limit)

        







# Rendering subfunction. Finds all of the sockets where custom text goes, and collates them
# into a list, in alphabetical order.


# Subfunction of play_next_round.
# Renders the frame repeatedly, each time with one more text line visible.
# ?Please see uitemplate.utf8ans for reference on which textspace each letter corresponds to.
def render_game(payload_list):

    # Get the BLANK template to draw our data over
    global current_frame
    current_frame = blank_template


    for i in range(len(payload_list)):

        # Extract tuple's first and second values
        start, end = socket_list[i]
        # Get replacement text to go over the blank
        replacement = payload_list[i]

        # Replace the characters between start and end with the characters in replacement.
        current_frame = current_frame[:start] + replacement + current_frame[end:]

        # Add a lil bit of sleep between each render step for that sweet sweet gamefeel
        time.sleep(.16)

        #Render our frame to the screen
        print(current_frame)




# ? This is a bit silly but it feels right to have this redundancy instead of printing directly
def render(frame):
    print(frame)


#!INPUT FUNCTIONS

# Subfunction of play_next_round that handles the typing challenge input aspects.
def type_attack(phrase, timelimit=10, tries=1):

    #Hook to our player health variable
    global hp

    # Sanitize attack phrase
    phrase = sanitize_string(phrase)
    # prompt user for text command based on params
    response = pyip.inputStr("  ", default="NULL", timeout=timelimit, limit=tries)

    # Sanitize user response
    response = sanitize_string(response)

    # Did they time out?
    if response == "NULL":
        print("  YOU TOOK TOO LONG! -1 HP!")
        time.sleep(2)
        hp = hp - 1

    # Does attackphrase and user response match?
    elif response == phrase:
        print("  Success!")
        time.sleep(2)

    else:
        print("  ACTION FUMBLED! -1 HP!")
        time.sleep(2)
        hp = hp - 1


#!INPUT SUBFUNCTIONS


# Removes spaces, and allcaps-ifies strings, for use in type_attack() string comparisons.
def sanitize_string(string):
    # remove spaces
    string = string.replace(" ", "")
    string = string.upper()
    return string


# ? MAIN BODY

if __name__ == "__main__":

    # Get screen ready
    initial_setup()

    # Load enemy
    load_enemy_file("Tomb Of The Lost", "skeleton")
   

    #Burn through all current rounds after enemy file loading.
    while pending_rounds:
        if hp == 0:
            print("You have died! Game over!")
            quit()
        play_next_round()

    print("Congratulations! You won the fight!")











    #print(blank_template)
    #print(pending_rounds)
    #print(socket_list)

    # get_hook_sockets()



    # print("Combat won!")

    # time.sleep(2.0)
    # render_ui()
