# SFNOC Car Racing Game - Installation & Running Instructions

## Requirements
- Python 3.8 or newer
- pip (Python package manager)

## Dependencies
- pygame

## Installation Steps

1. **Download the Game Files**
   - Download all files in the project directory, including `car_racing.py`, `requirements.txt`, and the README files.

2. **Install Python**
   - Download and install Python from: https://www.python.org/downloads/
   - Make sure to check the box to add Python to your PATH during installation.

3. **Install pip (if not already installed)**
   - pip is included with most Python installations. You can check by running:
     ```sh
     pip --version
     ```

4. **Install Dependencies**
   - Open a terminal or command prompt in the project directory.
   - Run:
     ```sh
     pip install -r requirements.txt
     ```

5. **Run the Game**
   - In the same terminal, run:
     ```sh
     python car_racing.py
     ```

6. **Enjoy!**
   - The game will open in a new window. Follow the on-screen instructions to play.

## Troubleshooting
- If you get an error about `pygame` not found, make sure you installed the requirements with pip.
- If double-clicking the `.py` file does not work, use the terminal method above.
- For any issues, ensure you are using Python 3 and not Python 2.

--- 




# SFNOC Car Racing Game - Gameplay & Details

## Game Overview
SFNOC Car Racing is a fast-paced, arcade-style racing game where you steer a taxi down a busy road, avoiding obstacles and collecting coins. The game gets faster as you collect more coins, challenging your reflexes and lane-changing skills!

## How to Play
- **Start the Game:**
  - When you launch the game, you'll see a welcome screen with instructions.
  - Enter your name to track your score on the leaderboard.
- **Controls:**
  - Use the **left** and **right arrow keys** on your keyboard to steer the car between lanes.
- **Objective:**
  - Avoid crashing into obstacles (other cars) in any lane.
  - Collect as many coins as possible to increase your score and climb the leaderboard.

## Scoring & Coins
- **Score:**
  - Your score increases as you survive longer and collect coins.
  - Each coin collected increases your coin count (displayed on screen).
- **Coins:**
  - Coins appear randomly in lanes and can be collected by driving over them.
  - Coins never overlap with obstacles, so you can always collect them safely if you reach them.
- **Speed Increases:**
  - The game gets faster as you collect more coins:
    - Normal speed: up to 29 coins
    - Faster: 30–59 coins
    - Fastest: 60+ coins

## Leaderboard
- After each game, your name and coin score are saved to a persistent leaderboard.
- The leaderboard displays the top scores and player names.
- If you achieve a new high score, it will be highlighted.
- Only the highest score per player is kept on the leaderboard.

## Game Over
- The game ends if your car crashes into an obstacle.
- You can restart the game or quit from the game over screen.

## Tips
- Always keep an eye on upcoming obstacles and plan your lane changes early.
- The gaps between obstacles are designed to always allow a fair escape route—use quick reflexes to switch lanes!
- As the game speeds up, focus on smooth, timely movements to survive longer and collect more coins.

---
Enjoy racing and aim for the top of the leaderboard! 
