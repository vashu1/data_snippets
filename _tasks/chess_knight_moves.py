'''
Quick Knight
Have the function QuickKnight(str) read str which will be a string consisting of the 
location of a knight on a standard 8x8 chess board with no other pieces on the board 
and another space on the chess board. The structure of str will be the following: "(x y)(a b)" 
where (x y) represents the position of the knight with x and y ranging from 1 to 8 and (a b) 
represents some other space on the chess board with a and b also ranging from 1 to 8. 
Your program should determine the least amount of moves it would take the knight to go 
from its position to position (a b). For example if str is "(2 3)(7 5)" then your program 
should output 3 because that is the least amount of moves it would take for the knight to 
get from (2 3) to (7 5) on the chess board.

Examples
Input: "(1 1)(8 8)"
Output: 6
'''

def position_from_str(s): # str to tuple of ints, i.e. '0 1' -> (0, 1)
  return tuple(map(int, s.split(' ')))

def knight_moves_from_position(pos): # all valid moves from position
  x,y = pos
  moves  = [(xp,yp) for xp in [x-1, x+1] for yp in [y-2, y+2]] # vertical moves
  moves += [(xp,yp) for xp in [x-2, x+2] for yp in [y-1, y+1]] # horizontal moves
  is_coord_legal = lambda x: 1 <= x <=8
  is_position_legal = lambda pos: is_coord_legal(pos[0]) and is_coord_legal(pos[1])
  return list(filter(is_position_legal, moves))

def QuickKnight(strParam):
  start, end = strParam[1:-1].split(')(')
  current_positions = set([position_from_str(start)])
  end_position = position_from_str(end)
  flatten = lambda l: [item for sublist in l for item in sublist]
  move_number = 0
  while True:
    if end_position in current_positions:
      return move_number
    moves = [knight_moves_from_position(position) for position in current_positions]
    current_positions = set(flatten(moves))
    move_number += 1

# keep this function call here 
print(QuickKnight('(1 1)(8 8)')) # should be 6
