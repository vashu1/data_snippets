input_test = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
input_test = input_test.split('\n')

input_full = open('d07.txt').readlines()

class Directory:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.size = 0
        self.dirs = {}
        self.files = {}

input = [line.strip() for line in input_full]  # input_test input_full
input = input[1:]
# parse directory tree
indx = 0
tree = Directory(None, '/')
pointer = tree
while indx < len(input) and input[indx]:
    assert input[indx][0] == '$'
    cmd = input[indx][2:]
    if cmd.startswith('cd'):
        indx += 1
        name = cmd[3:]
        if name == '..':
            assert pointer.parent
            pointer = pointer.parent
        else:
            assert name in pointer.dirs
            pointer = pointer.dirs[name]
    elif cmd.startswith('ls'):
        indx2 = indx + 1
        while indx2 < len(input) and input[indx2] and not input[indx2].startswith('$'):
            indx2 += 1
        for i in range(indx + 1, indx2):
            if input[i].startswith('dir '):
                name = input[i][4:]
                assert name not in pointer.dirs
                pointer.dirs[name] = Directory(pointer, name)
            else:
                data = input[i].split(' ')
                assert data[1]
                sz = int(data[0])
                name = ' '.join(data[1:])
                pointer.files[name] = sz
        indx = indx2

# get dir sizes
sm = 0
filtered_dirs = []
def set_sizes(dr):
    for d in dr.dirs:
        dr.size += set_sizes(dr.dirs[d])
    for f in dr.files:
        dr.size += dr.files[f]
    if dr.size <= 100_000:
        global sm, filtered_dirs
        sm += dr.size
        filtered_dirs += [dr.name]
    return dr.size


set_sizes(tree)
print(filtered_dirs)
print(sm)

dir2delete = tree
space = 70_000_000 - tree.size
def go_over(dr):
    if space + dr.size >= 30_000_000:
        global dir2delete
        if dir2delete != tree:
            assert dir2delete.size != dr.size
        if dir2delete.size > dr.size:
            dir2delete = dr
    for d in dr.dirs:
        go_over(dr.dirs[d])

go_over(tree)
print(dir2delete.name, dir2delete.size)