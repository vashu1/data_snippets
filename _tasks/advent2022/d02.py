
# 1st column A for Rock, B for Paper, and C for Scissors
# The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors
# The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
# plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

input = """A Y
B X
C Z""".split('\n')

input = open('d02.txt').readlines()

convert_yours = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
}

wins = {
    'A': 'C',
    'B': 'A',
    'C': 'B',
}

def score(his, yours):
    if yours == 'A':
        score = 1
    elif yours == 'B':
        score = 2
    else:
        score = 3
    if his == yours:
        score += 3
    elif wins[yours] == his:
        score += 6
    return score

acc = 0
for line in input:
    his, yours = line.strip().split(' ')
    yours = convert_yours[yours]
    acc += score(his, yours)
    #print(score(his, yours))

print(acc)

acc = 0
for line in input:
    his, yours = line.strip().split(' ')
    if yours == 'X':
        yours = wins[his]
    elif yours == 'Y':
        yours = his
    elif yours == 'Z':
        yours = wins[wins[his]]
    acc += score(his, yours)
    #print(his, yours, score(his, yours))

print(acc)