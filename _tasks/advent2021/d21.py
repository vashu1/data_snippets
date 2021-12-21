
# single die, two pawns, and a game board with a circular track containing ten spaces marked 1 through 10 clockwise.
# starting space is chosen randomly (your puzzle input)
# rolls the die three times and adds up the results
# After each player moves, they increase their score by the value of the space their pawn stopped on
# The game immediately ends as a win for any player whose score reaches at least 1000.
# This die always rolls 1 first, then 2, then 3, and so on up to 100

dice100_state = 100
roll_count = 0
def dice100():
    global dice100_state, roll_count
    roll_count += 1
    dice100_state = dice100_state % 100 + 1
    return dice100_state

#for i in range(1, 100):
#    assert dice100() == i, i

#dice100() == 1

# what do you get if you multiply the score of the losing player by the number of times the die was rolled during the game?

p1, p2 = 4, 8  # test
p1, p2 = 10, 4  # input

score1, score2 = 0, 0

while True:
    s = dice100() + dice100() + dice100()
    p1 = (p1 + s - 1) % 10 + 1
    score1 += p1
    if score1 >= 1000:
        break
    s = dice100() + dice100() + dice100()
    p2 = (p2 + s - 1) % 10 + 1
    score2 += p2
    if score2 >= 1000:
        break

print('task 1', min(score1, score2) * roll_count)

# rolling the die always splits the universe into three copies: one where the outcome of the roll was 1, one where it was 2, and one where it was 3.
# game now ends when either player's score reaches at least 21.
# Find the player that wins in more universes; in how many universes does that player win?

from collections import Counter, defaultdict

p1, p2 = 4, 8  # test
p1, p2 = 10, 4  # input

state = defaultdict(Counter)
state[0][(p1, p2, 0, 0)] = 1

# import itertools
# roll_results = Counter([sum(v) for v in itertools.combinations([1,2,3], 3)])
roll_results = Counter()
for i1 in range(1,3+1):
    for i2 in range(1, 3 + 1):
        for i3 in range(1, 3 + 1):
            roll_results[i1+i2+i3] += 1

i = 1  # half step number
while state[i-1]:
    for (p1, p2, s1, s2), prev_count in state[i - 1].most_common():
        if s1 >= 21 or s2 >= 21:
            continue
        for s, roll_count in roll_results.most_common():
            if i%2 == 1:
                p1_ = (p1 + s - 1) % 10 + 1
                s1_ = s1 + p1_
                state[i][(p1_, p2, s1_, s2)] += roll_count * prev_count
            else:
                p2_ = (p2 + s - 1) % 10 + 1
                s2_ = s2 + p2_
                state[i][(p1, p2_, s1, s2_)] += roll_count * prev_count
    i += 1

c1, c2 = 0, 0
for i in state:
    for (_, _, s1, s2), count in state[i].most_common():
        assert not ((s1 >= 21) and (s2 >= 21))
        if s1 >= 21:
            c1 += count
        if s2 >= 21:
            c2 += count

print('task2', max(c1, c2))