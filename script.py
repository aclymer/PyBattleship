# PyBattleship
# Simple python battle ship game
# By A.Clymer

from subprocess import call
from random import randint

board = []
ships = []
min_turns = 0
ship_char = u'\u25A0'
hit_char = u'\u25A1'
miss_char = u'\u25CC'

def cls():
  call("clear")

def print_board(board):
  i = 0
  print
  print "  1 2 3 4 5 6 7 8 9 10"  
  for row in board:
    print " ".join([chr(i+65)] + row)
    i += 1    

def random_row(board):
  return randint(0, len(board) - 1)

def random_col(board):
  return randint(0, len(board[0]) - 1)

def ship_out_of_range(board, ship):
  row = ship[0]
  col = ship[1]
  size = ship[2]
  vert = ship[3]
  
  if row < 0 or row >= len(board) or col < 0 or col >= len(board[0]):
    return 1
  elif size == 0:
    return 0
  
  if board[row][col] == ship_char:
    return 1
    
  if vert == 1:
    return ship_out_of_range(board, [row + 1, col, size - 1, vert])
  else:
    return ship_out_of_range(board, [row, col + 1, size - 1, vert])

def create_ship(board, ship):
  row = ship[0]
  col = ship[1]
  size = ship[2]
  vert = ship[3]
  points = []
  
  for i in range(size):
    point = []
    if vert == 1:
      board[row + i][col] = ship_char
      points.append([row + i, col])
    else:
        board[row][col + i] = ship_char
        points.append([row, col + i])
            
  return points
  
def ship_hit(board, ships, loc):
  board[guess_row][guess_col] = hit_char
  print "Hit!"
  
  for ship in ships:
    if loc in ship:
      ship.remove(loc)
    if len(ship) == 0:
      print "You sunk my battleship!"   
      ships.remove(ship)
  
# Game Logic
for x in range(10):
  board.append(["-"] * 10)

ship_sizes = [5,4,3,3,2]
print "Ships:"

for i in range(5):
  ship_len = ship_sizes[i]
  ship_dir = randint(0,1)
  ship_row = random_row(board)
  ship_col = random_col(board)
  
  ship_text = ""
  for a in range(ship_len):
    ship_text += " " + ship_char
  
  print ship_text
  
  while ship_out_of_range(board, [ship_row, ship_col, ship_len, ship_dir]) == 1:
    ship_dir = randint(0,1)
    ship_row = random_row(board)
    ship_col = random_col(board)
	 
  ships.append(create_ship(board, [ship_row, ship_col, ship_len, ship_dir]))
  min_turns += ship_len
  
print_board(board)

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(min_turns * 2):
  # Print (turn + 1) here!
  print "Turn", turn + 1

  guess = str(raw_input("Target Coordinate (eg A0): ")).upper()
  cls()
  guess_row = ord(guess[0]) - 65
  guess_col = int(guess[1:]) - 1
  
  if (guess_row < 0 or guess_row >= len(board)) or (guess_col < 0 or guess_col >= len(board[0])):
    print "Oops, that's not even in the ocean."
    turn -= 1
  elif board[guess_row][guess_col] == ship_char:
    ship_hit(board, ships, [guess_row, guess_col])
  elif board[guess_row][guess_col] == miss_char or board[guess_row][guess_col] == hit_char:
    print "You guessed that one already."
  else:
    print "You missed my battleship!"
    board[guess_row][guess_col] = miss_char

  print_board(board)
  
  if len(ships) == 0:
    print "You win!"
    break
    
  if turn == min_turns * 2:
    print "Game Over"
    break
