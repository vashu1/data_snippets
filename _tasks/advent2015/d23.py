import parse
import os

test = """inc a
jio a, +2
tpl a
inc a"""

program = []
registries = {
    'a': 1,
    'b': 0,
}

txt_name = __file__.split(os.sep)[-1].replace('.py', '.txt')
#for line in test.split('\n'):
for line in open(txt_name).readlines():
    line = line.strip()
    if ',' in line:
        c, a, b = parse.parse('{} {}, {:d}', line)
        program.append((c, a, b))
    else:
        c, a = parse.parse('{} {}', line)
        if c == 'jmp':
            a = int(a)
        program.append((c, a))

cmd = 0
while True:
    if cmd < 0 or cmd >= len(program):
        print(registries)
        exit()
    c = program[cmd]
    if c[0] == 'hlf':
        registries[c[1]] //= 2
    elif c[0] == 'tpl':
        registries[c[1]] *= 3
    elif c[0] == 'inc':
        registries[c[1]] += 1
    elif c[0] == 'jmp':
        cmd += c[1]
        continue
    elif c[0] == 'jie':
        if registries[c[1]] % 2 == 0:
            cmd += c[2]
            continue
    elif c[0] == 'jio':
        if registries[c[1]] == 1:
            cmd += c[2]
            continue
    else:
        assert False
    cmd += 1
