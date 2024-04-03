from tkinter import *
import tkinter.messagebox as messagebox
import random

# Define global variables (outside any function)
board = [' ' for _ in range(9)]
current_player = None  # Initially undecided
winner = None

def display_board():
  """Updates the text labels on the GUI to reflect the board state"""
  for i in range(3):
    for j in range(3):
      button_text = board[i*3 + j]
      buttons[i*3 + j].config(text=button_text, state=DISABLED if button_text != ' ' else NORMAL)

def is_valid_move(move):
  """Checks if the chosen position is empty"""
  return board[move] == ' '

def make_move(move, player):
  """Updates the board with the player's move"""
  global board
  board[move] = player

def is_winner(player):
  """Checks for winning conditions"""
  win_conditions = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6))
  for row in win_conditions:
    if all(board[i] == player for i in row):
      return True
  return False

def is_board_full():
  """Checks if all positions are filled"""
  return all(x != ' ' for x in board)

def switch_player():
  """Alternates players"""
  global current_player
  current_player = 'O' if current_player == 'X' else 'X'

def end_game():
  """Handles game end logic (displays winner or tie message)"""
  if winner:
    messagebox.showinfo("Game Over", f"Player {winner} Wins!")
  else:
    messagebox.showinfo("Game Over", "It's a Tie!")
  # Disable all buttons to prevent further moves
  for button in buttons:
    button.config(state=DISABLED)

def buttons_by_vaishnav(button_number):
  """Handles button clicks on the GUI for human player"""
  if not current_player:
    messagebox.showerror("Choose Symbol", "Please choose X or O to play first.")
    return
  if not is_valid_move(button_number):
    messagebox.showerror("Invalid Move", "Please choose an empty position.")
    return

  make_move(button_number, current_player)
  display_board()

  global winner
  winner = is_winner(current_player)
  if winner or is_board_full():
    end_game()
    return

  # Computer's turn (easy AI - random empty move)
  computer_move = random.choice([i for i in range(9) if is_valid_move(i)])
  make_move(computer_move, 'O' if current_player == 'X' else 'X')
  display_board()

  winner = is_winner('O' if current_player == 'X' else 'X')  # Check for computer's win
  if winner or is_board_full():
    end_game()
    return

#   switch_player()
#   # Display current player's turn after successful move
#   status_label.config(text=f"Player {current_player}'s Turn")

def choose_symbol(symbol):
  """Sets the player's symbol and starts the game"""
  global current_player
  current_player = symbol
  messagebox.showinfo("Let's Play!", f"You chose {symbol}. Good luck!")
  status_label.config(text=f"Player {current_player}'s Turn")
  # Enable buttons after symbol selection
  for button in buttons:
    button.config(state=NORMAL)

# Create the main window
root = Tk()
root.title("Tic Tac Toe (vs. Computer)")

# Buttons to choose X or O
symbol_buttons = []
symbol_choices = ['X', 'O']
for i, symbol in enumerate(symbol_choices):
    button = Button(root, text=symbol, font=("Arial", 40), width=2, height=1, command=lambda s=symbol: choose_symbol(s))
    button.grid(row=1, column=i)
    symbol_buttons.append(button)

# Buttons for the game board
buttons = []
for i in range(3):
  for j in range(3):
    button = Button(root, text=' ', font=("Arial", 40), width=3, height=1, command=lambda n=i*3+j: buttons_by_vaishnav(n))
    button.grid(row=i+2, column=j)
    buttons.append(button)

# Create a label to display the current player's turn
status_label = Label(root, text="Choose X or O to start", font=("Arial", 20))
status_label.grid(row=5, columnspan=3)

# Start the main event loop
root.mainloop()
