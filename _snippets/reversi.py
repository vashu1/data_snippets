'''
2021? dataset from https://www.kaggle.com/datasets/andrefpoliveira/othello-games/code
all the standard games played by the TOP 100 players on eOthello. No Random Openings, no Anti, no Hexa and no Grand.
'''

def initialize_board():
    board = [['.' for _ in range(8)] for _ in range(8)]
    board[3][3] = board[4][4] = 'W'
    board[3][4] = board[4][3] = 'B'
    return board

def chess_to_index(chess_coord):
    row = int(chess_coord[1]) - 1
    col = ord(chess_coord[0].lower()) - ord('a')
    return row, col


def print_game(board):
    return
    for i in board:
        print(''.join(i))


def valid_move(board, row, col, player, opponent):
    # Directions: N, NE, E, SE, S, SW, W, NW
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                  (1, 0), (1, -1), (0, -1), (-1, -1)]
    flips = []
    for dr, dc in directions:
        path = []
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            path.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            flips.extend(path)
    return flips

def apply_move(board, row, col, player):
    opponent = 'B' if player == 'W' else 'W'
    flips = valid_move(board, row, col, player, opponent)
    for r, c in flips:
        board[r][c] = player
    if flips:
        board[row][col] = player
    #print(row,col, len(flips))
    print_game(board)
    return len(flips)

def count_flips(game_moves):
    board = initialize_board()
    player_turn = 'B'
    total_flips = 0
    for move in game_moves:
        row, col = chess_to_index(move)
        total_flips += apply_move(board, row, col, player_turn)
        player_turn = 'W' if player_turn == 'B' else 'B'
    return total_flips

'''
game_moves = "f5d6c4d3e6f4e3f6c5b4e7f3c6d7b5a5c3b3g5h5g4h4e2g6b6d8c7c8a4a6a7f1a3c2d2b2e1b7g3h3f2d1a1a2b1a8c1g1f7g8e8f8b8g7h8h7h6h2g2h1"
moves = []
for i in range(len(game_moves)):
    if i % 2 == 1:
        continue
    moves.append(game_moves[i:i+2])
print(moves)
print("Total Flips:", count_flips(moves))
'''
flips = []
for line in open('datasets/othello_dataset.csv').readlines()[1:]:
    line = line.strip()
    line = line.split(',')[-1]
    moves = []
    for i in range(len(line)):
        if i % 2 == 1:
            continue
        moves.append(line[i:i+2])
    flips.append(count_flips(moves))


print(f'{max(flips)=} {min(flips)=} {len(flips)=} {sum(flips)/len(flips)}')

'''
max(flips)=177 min(flips)=20 len(flips)=25657 128.08687687570642
'''