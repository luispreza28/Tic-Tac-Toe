# Tic-Tac-Toe Multiplayer Game with AI
This project is a multiplayer Tic-Tac-Toe game built using Python's socket library for network communication and pygame for rendering the game. It supports both multiplayer mode and single-player mode with an AI opponent. The game is designed for two players and allows playing over a network, with a simple game state management system to handle turns, board updates, and game resets.

## Features
- Multiplayer support: Two players can play remotely via a network connection.
- Single-player mode with AI: Play against a simple AI opponent in single-player mode.
- Game state management: The game tracks turns, validates moves, checks for a winner, and handles game resets.
- Graphical User Interface (GUI): Implemented with pygame for drawing the game board, symbols (X and O), and handling user interactions.
- Music and Sound Effects: Background music for both the main menu and in-game experience.

## Project Structure


├── ai_logic.py         # AI logic for single-player mode

├── client.py           # Client-side code handling user input and rendering the game with Pygame

├── game.py             # Core game logic and state management

├── network.py          # Network logic for managing player moves and game updates

├── server.py           # Server-side code for handling connections and broadcasting game state

├── assets              # Folder containing background images, win/lose screens, and music

│   ├── main_menu_background3.jpeg

│   ├── win_screen.jpg

│   ├── loss_screen.jpeg

│   ├── draw_screen.jpg

│   ├── in_game_music.mp3

│   └── goofy_main_menu_music.mp3

└── README.md           # This file


## Installation
To run this project, you need to have Python installed on your machine. Additionally, you need to install the required Python packages:

Clone the repository:
```git clone https://github.com/your-username/tic-tac-toe.git```
```cd tic-tac-toe```
Install dependencies using pip:
```pip install pygame```

## Usage
### Running the Server
To start the server, run the following command:
```python server.py```
This will start the game server on 127.0.1.1:5555. The server listens for incoming connections from players.

Running the Client
To start the client and join a game, run the following command:

```python client.py```
The client connects to the server at 127.0.1.1:5555 and allows you to start playing.

You can connect two clients to play a multiplayer game.

## Game Modes
### Single Player
In the Single Player mode, you play against an AI opponent. The AI will randomly pick a move when it is the AI's turn.

To start Single Player mode, press 1 on the main menu.

### Multiplayer
In Multiplayer mode, two players can connect to the server from different clients and play against each other.

To start Multiplayer mode, press 2 on the main menu.
Once both players are connected, the game will begin, alternating turns between player X and player O.

### Controls
Mouse: Click on the grid to make your move.
Escape Key: Return to the main menu during the game.
### Dependencies
The project requires the following dependencies:

- Pygame: Used for rendering the game interface and handling user input. Install it with:

```pip install pygame```
Socket: Built-in Python library for handling networking.

Ensure that your machine has Python installed with version 3.6+.

Enjoy your game! Feel free to contribute or suggest improvements.
