# You can make your own enemy text files

lets take a look at an example.

```
XXXXXXXXXXXX
XXXXXNOXXXXX
XXXIMAGEXXXX
XXXXDATAXXXX
XXXFOUNDXXXX
XXXXXXXXXXXX
SKELETON
!ROUND1!
The skeleton swings overhead!


BLOCK WITH SHIELD
5
!ROUND2!
SKELETON readies a kick!


TWIST BODY TO THE SIDE
8
!ROUND3!
You see an opening!


SHIELDBASH RIBCAGE
6
!ROUND4!
The skeleton loses balance!


POMMEL STRIKE SKELETON SKULL
9
```

The game, upon loading your enemy, will look at the first 6 lines for the sprite art. each row is 12 characters.

It will then look at the next line to find the enemy name for display. Max 14 characters.

It will then print the **three lines** below it in grey text in the text box. max character count per line is 31. If you only need one line, fill in only the top line, but **make sure to keep the empty lines present like in the example above.**

After the three lines is the COMMAND, which is what the game demands you type, and is written in magenta. Max character count 31.

below the COMMAND in this file is a number, which is the number of seconds the player has to input the COMMAND.

If the player succeeds, the game will go down the list to find the word !ROUND! again, and the process repeats.

If there's no more !ROUND!'s present, then the player has won the fight, and moves on.