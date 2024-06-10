# Spell-of-the-Serpent

Spell of the Serpent is a solo midterm project by Casey Glidewell.

## What It Is and How It Is Played

Spell of the Serpent is going to be a typing-centered fantasy combat game, that takes place completely within the command line interface.

Core features of the game will include:
A combat flow, where an enemy action is described, and a time limit is given to type out text displayed on how your character counteracts the enemy action. For example:

```
Skeleton does an overhead swing!
```
 > ***Block with your shield***
In this example, the player has 7 seconds to type, exactly, the words "Block with your shield" case insensitive, or they will take damage. After this, the roles will switch, and the player now must type a displayed offensive action.
```
Skeleton reels backwards!
```
 > ***Spinning axe swing***
If the player succeeds in typing this new phrase before the timer runs out, they will do damage to the enemy.

With enough damage dealt to the enemy, the player will be allowed to move on to face against a new enemy, with new attacks they will need to defend against, and attack with. This cycle repeats a few times, until the more complicated "boss of the dungeon" appears. If the player wins this battle, they win the game.

## Core Systems

### Enemies

Enemies are planned be dynamically loaded from a text file present in the game directory's data/enemies folder.
The text file itself will have all of the details of what attacks the enemy can choose from (the attacks will be chosen randomly) what inputs the player needs to make to survive attacks/deal damage, and how many successful attack made on the enemy need to be performed to move on.

This setup will allow for rapid prototyping of new enemies, and as a bonus, will allow players to invent their own if they can understand the formatting used for the enemies already present in the directory.

Enemies will also be sorted by Dungeon, and enemy files called BOSS_example.txt will always be the Boss Of The Dungeon, and the finale of the game.

### Dungeons

The player will be able to pick from at least 2 dungeons, by making a selection on the game's main menu. Enemies will only be pulled from the enemy list of the selected dungeon. Menu should be modular enough to support potentially more than 2 dungeons being included, again, to facilitate rapid development of new content, and allowing savvy users to create their own.

### Interface

The full game will be run in the CLI, taking advantage of various libraries that allow precise control of font size and CLI resolution/aspect ratio, to ensure that the player sees the game's visuals as they are intended to. Rich text console and other text decoration libraries will also be used for "prettifying" the game's interface. All graphics however are intended, and planned to be consisting only of ascii supported by a standard CLI.

A minimum resolution of monitor will be required, and no plans for dynamic scaling of the game screen will be made.

## Project Planning

> What are the key strengths of each person on the team?
My core strengths come from rapid iterative design, the ability to format a segment of the project in a way that variables can be tweaked up and down, so that any changes needed from testing can be done with only a couple variable edits. Precise and detailed commenting is another strength of mine that is a must for larger scale projects such as this.

> How can you best utilize these strengths in the execution of your project?
Careful planning of what aspects of the project can be made modular, and how to separate the different loops and functions is a must. This project will involve several moving parts that need to work in harmony, and must function correctly one after another.

> In which professional competencies do you each want to develop greater strength?
This project will involve me using libraries not recommended for me by the class curriculum, and involve several manipulations of the CLI that I was uncertain if was even possible, prior to the initial research on this project's concept.


## Conflict Plan

> What will be your group’s process to resolve conflict, when it arises?
While I will not have fellow group members, I will be requesting help from a former system administrator family member if the need arises, to prevent complete deadlock. I also have access to several tech-oriented friends who have assisted me before with blockers.

> What will your team do if one person is taking over the project and not letting the other members contribute?
Not applicable with a solo project.

> How will you approach each other and the challenges of the project knowing that it is impossible for all members to be at the exact same place in understanding and skill level?
Mostly not applicable. I will be taking on every aspect of this assignment, so I will need to manage having little understanding of some elements, and strong understanding of others.

> How will you raise concerns to members who are not adequately contributing?
Another family member has been acting as my accountability partner, and will keep me on task for this project.

> How and when will you escalate the conflict if your resolution attempts are unsuccessful?
Speaking with family, the tech friends I mentioned above, and if all else fails, submission of a TA help ticket.

## Communication plan

> What hours will you be available to communicate?
I come into class most days including weekends sometime after 4 or 5 PM PT. I will try to make sure I am frequently in the virtual classroom during these times.

> What platforms will you use to communicate (ie. Slack, phone …)?
Slack and virtual classroom for anything involving TAs or faculty, Discord for assistance from tech friends, and in person for assistance from family.

> How often will you take breaks?
I usually take a brief break every approximately hour and a half.

> What is your plan if you start to fall behind?
Pick back up, make earlier use of requesting assistance from my friends family and peers, and potentially discuss with faculty/TAs on if the scale of the project needs to change.

> How will you communicate after hours and on the weekend?
I can be emailed, and direct messages from slack will also be sent to my email to notify me.

> What is your strategy for ensuring everyone’s voice is heard?
Communication with faculty and TAs to make sure that my project's trajectory is acceptable.
> How will you ensure that you are creating a safe environment where everyone feels comfortable speaking up?
I intend to be polite for any assistance requests I make. The project itself will also be suitable for all ages, and should have no more objectionable content than "the snake dies!" or such.

## Work Plan

> How you will identify tasks, assign tasks, know when they are complete, and manage work in general?
I am currently considering a trello board, and perhaps other whiteboard/todo list software, that consists of the vital aspects of the project as top priority, where work toward a minimum viable product is the first, and only task. All items on the trello board will be in service of achieving MVP, and only after that will the "wrapping" around the project be polished and improved.

MVP first, no questions asked.

> What project management tool will be used?
Trello board, as mentioned above.

## Git Process

> What components of your project will live on GitHub?
The full source code is planned to live on github, with sensible .gitignore practices followed for the basic things such as the virtual environment. This project will not need secret files or keys.
> How will you share the repository with your teammates?
I will share the github link with anyone who requests to see, faculty or friends. With the full contents of the project more or less being present on the git repository, this should be acceptable.

> What is your Git flow?
Create a branch for work on a core project feature, and upload/merge into dev branch as work either completes on that feature, or a significant **and stable** milestone is reached in relation to that feature.

Upon MVP being achieved, dev branch is merged into main, and then work begins on tuning. Depending on how things look at this phase of the project, changes and tuning may become more spread out and holistic, so the feature-restricted git flow may no longer make sense, but that is something that will simply have to be seen when it arrives.

