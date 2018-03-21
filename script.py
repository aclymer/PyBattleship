# PyBattleship
# Simple python battle ship game
# By A.Clymer

from subprocess import call
from random import randint
from copy import deepcopy

player_board = []
computer_board = []
ships = []
hits = []
min_turns = 0
ship_char = u'\u25A0'
hit_char = u'\u25A1'
miss_char = u'\u25CC'
sunk_char = u'\u25CB'

def cls():
  for i in range(120):
    print chr(12)

def print_board(board, ships):
  print "Ships remaining:"
  for ship in ships:
    text = ""
    for loc in ship:
      text += ship_char + " "
    
    print text
      
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
  
def ship_hit(board, player_board, ships, hits, loc):  
  board[loc[0]][loc[1]] = hit_char
  print "Hit!"
  
  for ship in range(len(hits)):
    if loc in hits[ship]:
      hits[ship].remove(loc)
      if len(hits[ship]) == 0:
        print "You sunk my battleship!"
        for coords in ships[ship]:
          player_board[coords[0]][coords[1]] = sunk_char
        ships.remove(ships[ship])
        hits.remove(hits[ship])
    	break

# Game Logic
for x in range(10):
  player_board.append(["-"] * 10)
  computer_board.append(["-"] * 10)

ship_sizes = [5,4,3,3,2]

for i in range(5):
  ship_len = ship_sizes[i]
  ship_dir = randint(0,1)
  ship_row = random_row(player_board)
  ship_col = random_col(player_board)
      
  while ship_out_of_range(computer_board, [ship_row, ship_col, ship_len, ship_dir]) == 1:
    ship_dir = randint(0,1)
    ship_row = random_row(player_board)
    ship_col = random_col(player_board)
	 
  ships.append(create_ship(computer_board, [ship_row, ship_col, ship_len, ship_dir]))
  min_turns += ship_len
  
print_board(player_board, ships)
turns = min_turns * 2
hits = deepcopy(ships)

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
for turn in range(1, turns):
  # Print (turn + 1) here!
  print "Turn", turn, "/", turns

  guess = str(raw_input("Target Coordinate (eg A0): ")).upper()
  cls()
  guess_row = ord(guess[0]) - 65
  guess_col = int(guess[1:]) - 1
  
  if (guess_row < 0 or guess_row >= len(computer_board)) or (guess_col < 0 or guess_col >= len(computer_board[0])):
    print "Oops, that's not even in the ocean."
    turn -= 1
  elif computer_board[guess_row][guess_col] == ship_char:
    player_board[guess_row][guess_col] = hit_char
    ship_hit(computer_board, player_board, ships, hits, [guess_row, guess_col])
  elif computer_board[guess_row][guess_col] == miss_char or computer_board[guess_row][guess_col] == hit_char:
    print "You guessed that one already."
  else:
    print "You missed!"
    computer_board[guess_row][guess_col] = miss_char
    player_board[guess_row][guess_col] = miss_char

  print_board(player_board, ships)
      
  if len(ships) == 0:
    print "You win!"
    print "Score: %i" % round(100 - float(turn)/turns*100.0)
    break
    
  if turn == turns:
    print "Game Over"
    break
