# Gomoku AI in Python
A simple [Gomoku](https://en.wikipedia.org/wiki/Gomoku) (or also called Five-In-A-Row) AI implemented in Python from scratch. 

## Overview
Gomoku is a strategy board game with 2 players and on a 15x15 board. The objective of the game is to form an unbroken chain of 5 stones (vertically, horizontally, diagonally) and the first player to do that wins the game. In this project, you can play against the AI that uses the MiniMax algorithm with alpha beta prunning in order to make the next move. Everything is integrated with a GUI made through `pygame`.

## Requirement
In order to run this program, the `pygame` library must be installed first:
```
> pip install pygame
```

## Files Structure
```
├── assets
│   └── black_piece.png
│   └── board.jpg
│   └── button.png
│   └── menu_board.png
│   └── white_piece.png
├── gui
│   └── button.py
│   └── interface.py
├── source
│   └── AI.py
│   └── gomoku.py
│   └── utils.py
├── .gitignore
├── LICENSE
├── README.md
└── play.py
```

## Execution
For playing against the AI, run the following commands:
```
> git clone https://github.com/husus/gomokuAI-py
> cd gomokuAI-py
> python3 play.py
```


The image below is the starting screen of the game interface that would appear after the above-mentioned commands have been run correctly. The player can choose between black or white, and the other color will be assigned to the AI. Remember that according to the Gomoku rules, black always starts first.
<img width="541" alt="start_screen" src="https://user-images.githubusercontent.com/93041464/173566175-01f4e7cb-48ef-4a24-921d-eaa728baaaf3.png">
To make the moves, it is necessary to simply click on the empty intersections of the board. 


<br> </br>

-----------------------------------------------
### Disclaimer
This repository is part of the submission of the final project for the MSc course [20602 - COMPUTER SCIENCE (ALGORITHMS)](https://didattica.unibocconi.eu/ts/tsn_anteprima.php?cod_ins=20602&anno=2022&IdPag=) at Bocconi University.
