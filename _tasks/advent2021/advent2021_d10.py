# https://adventofcode.com/2021/day/10

test = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

lines = test.split('\n')
#
lines = [line.strip() for line in open('input').readlines()]

opening = '[(<{'
closing = '])>}'
reverse_elem = {k: v for k, v in zip(opening+closing, closing+opening)}
opening = set(list(opening))
closing = set(list(closing))

points = {k:v for k, v in zip(list(')]}>'), [3, 57, 1197, 25137])}

def corrupted_line_score_or_stack(line):
    stack = []
    for ch in line:
        if ch in opening:
            stack.append(ch)
        elif ch in closing:
            if not stack:
                print('chank starts with closing')
                return points[ch], None
            elif stack[-1] == reverse_elem[ch]:
                _ = stack.pop()
            else:
                return points[ch], None  # corrupted
        else:
            assert False
    return 0, stack

print(sum([corrupted_line_score_or_stack(line)[0] for line in lines]))

# part2

completion_scores = {k:v for k, v in zip(list(')]}>'), [1,2,3,4])}

scores = []
for line in lines:
    corruption_score, stack = corrupted_line_score_or_stack(line)
    if corruption_score > 0:
        continue
    score = 0
    for ch in [reverse_elem[el] for el in reversed(stack)]:
        score *= 5
        score += completion_scores[ch]
    scores.append(score)

scores.sort()

print(len(scores)%2==1)
print(scores[int(len(scores)/2)])
