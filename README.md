![blockparty](https://github.com/user-attachments/assets/84570eb6-10bd-47b2-96fc-a20f5f6c9288)

# BlockParty
BlockParty is a 2-player Python game using the PyGame module whereby strategy is used to achieve more territory than the opposing player.

## Table of Contents
- [Installation](#installation)
- [Game Rules](#game-rules)
- [Game Controls](#game-controls)
- [Game Modes](#game-modes)
- [How to Play](#how-to-play)
- [Scoring](#scoring)
- [License](#license)

## Installation

1. Ensure you have Python installed on your system.
2. Install the required dependencies using pip:
    ```sh
    pip install pygame
    ```
3. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/BlockParty.git
    ```
4. Navigate to the project directory:
    ```sh
    cd BlockParty
    ```

## Game Rules

BlockParty is a game where players take turns to perform actions on a grid of blocks. The goal is to achieve the highest score based on specific objectives.

### Objectives

There are two types of goals:
1. **Perimeter Goal**: Outline the greatest amount of the game board's perimeter with your target color.
2. **Blob Goal**: Create the largest collection or "blob" of adjacent squares of your target color.

### Actions

Players can perform the following actions:
- **Rotate Clockwise**: Rotate a block and its descendants clockwise.
- **Rotate Counterclockwise**: Rotate a block and its descendants counterclockwise.
- **Swap Horizontally**: Swap the child blocks of a block horizontally.
- **Swap Vertically**: Swap the child blocks of a block vertically.
- **Smash**: Sub-divide a block into four randomly generated children.
- **Combine**: Turn a block into a leaf based on the majority color of its children.
- **Paint**: Change a block's color to the player's target color.
- **Pass**: Skip the turn without performing any action.

## Game Controls

### Human Player Controls

- **Increase Level**: `S`
- **Decrease Level**: `W`
- **Rotate Clockwise**: `D`
- **Rotate Counterclockwise**: `A`
- **Swap Horizontally**: `Q`
- **Swap Vertically**: `E`
- **Smash**: `SPACE`
- **Combine**: `C`
- **Paint**: `R`
- **Pass**: `TAB`

### Non-Human Player Controls

- **Click Mouse to Continue**

## Game Modes

You can play BlockParty in several configurations:

- **Auto Game**: Two computer players of different difficulty levels.
- **Two Player Game**: Two human players.
- **Solitaire Game**: One human player.
- **Sample Game**: One human player, one random player, and one smart player.

## How to Play

1. Run the game by executing the `game.py` file:
    ```sh
    python game.py
    ```
2. Choose the desired game mode by uncommenting the corresponding line in the `if __name__ == '__main__':` section of `game.py`.
3. The game will start, and players will take turns performing actions to achieve their goals.

## Scoring

Each player has a specific goal, and their score is calculated based on how well they achieve that goal. The score is adjusted by penalties for certain actions:

- **Smash**: 3 points penalty
- **Combine**: 1 point penalty
- **Paint**: 1 point penalty
- **Pass**: No penalty

The player with the highest score at the end of the game wins.
