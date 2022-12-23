import matplotlib.pyplot as plt
import sys
import os

YEAR = 2022
DAY = 22
YEAR = sys.argv[1]
DAY = sys.argv[2]

MINUTES_RANGE = 3 * 60 + 20

FONT_SIZE = 12

plt.title(f'Advent of Code {YEAR} day {DAY}')
plt.ylabel('submissions per minute')
plt.xlabel('minutes')

ax = plt.axes()
ax.grid()

plt.text(0.8, 0.75, 'Bold text numbers \nnext to graphs mean \nrank at the time.',
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes, weight="bold")

def diff(lst):
    return [b - a for a, b in zip(lst, lst[1:])]

fsts = []
snds = []
for line in open(f'{YEAR}/d{DAY}.txt').readlines():
    line = line.strip()
    # 19:49:01 delay 1 fst 2765 snd 5170
    _, _, _, _, fst, _, snd = line.split(' ')
    fst = int(fst)
    snd = int(snd)
    fst += snd
    fsts.append(fst)
    snds.append(snd)

diff_snds = diff(snds)

def plot_submissions(submissions, label, color):
    diffs = diff(submissions)
    diffs = [0] + diffs[:MINUTES_RANGE]
    # smooth
    avg = lambda i: (diffs[i - 1] + diffs[i] + diffs[i + 1]) / 3
    diffs = [0] + [avg(i) for i in range(1, len(diffs) - 1)]
    xs = list(range(len(diffs)))
    plt.plot(xs, diffs, label=label)
    #
    for i in range(len(submissions)):
        if submissions[i] > 100:
            break
    leaderboard_index = i
    plt.text(xs[leaderboard_index] + 1, diffs[leaderboard_index] + 1, '100',
             fontsize=11, weight="bold", color=color)
    #
    #
    mx = max(diffs)
    mx_indx = diffs.index(mx)
    plt.text(xs[mx_indx] + 1, diffs[mx_indx] - 1, str(submissions[mx_indx]), fontsize=FONT_SIZE, weight="bold", color=color)
    half = mx_indx // 2
    if abs(half - leaderboard_index) > half // 2:
        plt.text(xs[mx_indx - half] + 1, diffs[mx_indx - half] + 1, str(submissions[mx_indx - half]),
             fontsize=FONT_SIZE, weight="bold", color=color)
    plt.text(xs[mx_indx + half] + 1, diffs[mx_indx + half] + 1, str(submissions[mx_indx + half]),
             fontsize=FONT_SIZE, weight="bold", color=color)
    if mx_indx * 2 < len(diffs):
        plt.text(xs[mx_indx * 2] + 1, diffs[mx_indx * 2] + 1, str(submissions[mx_indx * 2]),
             fontsize=FONT_SIZE, weight="bold", color=color)
    #
    plt.legend(loc="upper right")


plot_submissions(fsts, 'Part 1', 'blue')
plot_submissions(snds, 'Part 2', 'red')

plt.savefig(f'{YEAR}{os.sep}advent_{YEAR}_day_{DAY}.png')
plt.show()