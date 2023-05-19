import random
import tkinter as tk
from tkinter import messagebox

# Constants
BOARD_SIZE = 100
NUM_SNAKES = 8
NUM_LADDERS = 8

# Define snakes and ladders positions
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91}

# Function to roll the dice
def roll_dice():
    return random.randint(1, 6)

# Function to check if a player has won
def check_win(position):
    return position >= BOARD_SIZE

# Function to check for snakes and ladders
def check_snake_ladder(position):
    if position in snakes:
        messagebox.showinfo("Snake", "Oops! You got swallowed by a snake.")
        return snakes[position]
    elif position in ladders:
        messagebox.showinfo("Ladder", "Yay! You found a ladder.")
        return ladders[position]
    else:
        return position

# Function to update player position and check for win
def update_position(player):
    dice_roll = roll_dice()
    messagebox.showinfo("Dice Roll", f"{player['name']}, you rolled a {dice_roll}.")
    player['position'] += dice_roll

    if player['position'] > BOARD_SIZE:
        player['position'] = BOARD_SIZE - (player['position'] - BOARD_SIZE)

    player['position'] = check_snake_ladder(player['position'])
    messagebox.showinfo("Position", f"{player['name']}, your current position is {player['position']}.")

    if check_win(player['position']):
        messagebox.showinfo("Congratulations", f"Congratulations! {player['name']} wins!")
        reset_game()

    # Update player position on the game board
    update_board()

# Function to update the game board
def update_board():
    # Clear the board
    for row in cells:
        for cell in row:
            cell.config(text="", bg="white")

    # Update snake positions on the board
    for start, end in snakes.items():
        row1, col1 = get_cell_coordinates(start)
        row2, col2 = get_cell_coordinates(end)
        cells[row1][col1].config(text="S", bg="red")
        cells[row2][col2].config(text="S", bg="red")

    # Update ladder positions on the board
    for start, end in ladders.items():
        row1, col1 = get_cell_coordinates(start)
        row2, col2 = get_cell_coordinates(end)
        cells[row1][col1].config(text="L", bg="green")
        cells[row2][col2].config(text="L", bg="green")

    # Update player positions on the board
    for player in players:
        row, col = get_cell_coordinates(player['position'])
        cells[row][col].config(text=player['name'][0], fg=player['color'], bg=player['color'])

# Function to get the row and column coordinates of a cell on the game board
def get_cell_coordinates(position):
    row = (position - 1) // 10
    if row % 2 == 0:
        col = (position - 1) % 10
    else:
        col = 9 - (position - 1) % 10
    return row, col

# Function to handle player turns
def handle_turn():
    global current_player
    player = players[current_player]
    update_position(player)
    current_player = 1 - current_player  # Switch turns

# Function to reset the game
def reset_game():
    global current_player
    current_player = 0
    for player in players:
        player['position'] = 0
    # Clear the board
    for row in cells:
        for cell in row:
            cell.config(text="", bg="white")

# Create the GUI
root = tk.Tk()
root.title("Snake and Ladder Game")

# Game board
board_frame = tk.Frame(root)
board_frame.pack()

cells = []
for i in range(10):
    row = []
    for j in range(10):
        cell = tk.Label(board_frame, text="", width=4, height=2, relief=tk.RIDGE)
        cell.grid(row=i, column=j)
        row.append(cell)
    cells.append(row)

# Players
players = [
    {'name': 'Player 1', 'position': 0, 'color': 'red'},
    {'name': 'Player 2', 'position': 0, 'color': 'blue'}
]

# Player labels
player_labels = []
for player in players:
    label = tk.Label(root, text=f"{player['name']}: {player['position']}", fg=player['color'])
    label.pack()
    player_labels.append(label)

# Button for rolling the dice
button_frame = tk.Frame(root)
button_frame.pack()

button = tk.Button(button_frame, text="Roll Dice", command=handle_turn)
button.pack(pady=10)

# Initialize the current player
current_player = 0

# Start the game
messagebox.showinfo("Welcome", "Welcome to Snake and Ladder Game!")
update_board()  # Initialize the game board
root.mainloop()
