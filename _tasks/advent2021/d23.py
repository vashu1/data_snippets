
test = '''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''

input = '''#############
#...........#
###A#D#A#B###
  #C#C#D#B#
  #########'''

# Four types of amphipods live there: Amber (A), Bronze (B), Copper (C), and Desert (D).
# They live in a burrow that consists of a hallway and four side rooms.

# The side rooms are initially full of amphipods, and the hallway is initially empty.

# locations of each amphipod (A, B, C, or D, each of which is occupying an otherwise open space), walls (#), and open space (.).

# organize every amphipod into side rooms so that each side room contains one type of amphipod and the types are sorted A-D going left to right

# Each type of amphipod requires a different amount of energy to move one step: Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper amphipods require 100, and Desert ones require 1000

# never stop on the space immediately outside any room.
# will never move from the hallway into a room unless that room is their destination room and that room
# contains no amphipods which do not also have that room as their own destination

# Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.

moves = ['R1', 'R2', 'R3', 'R4', '']


print('task 1', 0)  # 12521