import string

class Node:
    def __init__(self, v1, op=None, v2=None):
        self.v1 = v1 if op else v1
        self.op = op
        self.v2 = v2 if op else None
    #
    def flatten(self):
        if isinstance(self.v1, Node):
            self.v1.flatten()
            if not self.v1.op:
                self.v1 = self.v1.v1
        if self.op:
            if isinstance(self.v2, Node):
                self.v2.flatten()
                if not self.v2.op:
                    self.v2 = self.v2.v1
    #
    def _simplify(self):
        r1 = r2 = False
        if isinstance(self.v1, Node):
            r1 = self.v1.simplify()
        if self.op:
            if isinstance(self.v2, Node):
                r2 = self.v2.simplify()
            if self.op == '*' and self.v2 == '0':
                self.v1 = 0
                self.op = None
                return True
        return r1 or r2
    #
    def simplify(self):
        while(self._simplify()):
            self.flatten()
    #
    def replace(self, old_val, new_val):
        if isinstance(self.v1, Node):
            self.v1.replace(old_val, new_val)
        else:
            #print(f'{(self.v1 == old_val)=}')
            if self.v1 == old_val:
                self.v1 = new_val
        if self.op:
            if isinstance(self.v2, Node):
                self.v2.replace(old_val, new_val)
            else:
                #print(f'{(self.v2 == old_val)=}')
                if self.v2 == old_val:
                    self.v2 = new_val
    #
    def size(self):
        if self.op:
            s1 = self.v1.size() if isinstance(self.v1, Node) else 1
            s2 = self.v2.size() if isinstance(self.v2, Node) else 1
            return s1 + s2
        else:
            return 1
    #
    def str2(self):
        v1 = self.v1.str2() if isinstance(self.v1, Node) else str(self.v1)
        if self.op:
            v2 = self.v2.str2() if isinstance(self.v2, Node) else str(self.v2)
            return f'({v1} {self.op} {v2})'
        else:
            return f'({v1})' # v1

"""
t = Node(1,'-',Node(Node(1,'+',2),'*',0))
t.str2()
t.simplify()
t.str2()

t = Node(1,'-',Node(Node(1,'+',2),'*',Node(Node(0))))
"""

tree = Node('z', '+', 'y')

var_cnt = 26
def uniq_var_name():
    global var_cnt
    var_cnt += 1
    var_indx = int(var_cnt / 26)
    res = string.ascii_lowercase[:26][26 - 1 - var_cnt%26]  # z to a
    if var_indx:
        res += str(var_indx)  # z1, a2, etc
    return res

def parse_number(v):
    try:
        v = int(v)
        return v
    except:
        return None

count_input = 0
def parse_line(line, current_equation, rename):
    global tree
    if line.startswith('inp '):
        _, v1 = line.split(' ')
        global count_input
        count_input += 1
        v1renamed = rename[v1] if v1 in rename else v1
        rename[v1] = uniq_var_name()
        tree.replace(v1renamed, f'input{count_input-1}')
        tree.simplify()
        return
        #return current_equation.replace(v1renamed, f'input{count_input-1}')
    cmd, v1, v2 = line.split(' ')
    #if not v1 in rename:
    #    return  # result is not used
    v1renamed = rename[v1] if v1 in rename else v1
    rename[v1] = uniq_var_name()
    v2 = rename[v2] if v2 in rename else v2
    v2 = parse_number(v2) if parse_number(v2) else v2
    if cmd =='add':
        op = '+'
    elif cmd == 'mul':
        op = '*'
        #if v2 == 0:
        #    return current_equation.replace(v1renamed, 0)
    elif cmd == 'div':
        op = '/'
    elif cmd == 'mod':
        op = '%'
    elif cmd == 'eql':
        op = '=='
    else:
        assert False, line
    #print(f'replace {v1renamed} {Node(rename[v1], op, v2).str2()}')
    tree.replace(v1renamed, Node(rename[v1], op, v2))
    tree.simplify()
    #return current_equation.replace(v1renamed, f'({rename[v1]} {op} {v2})')

#variables = {'z': 0}
rename = {'z':'z'}
current_equation = 'z = - y'
lines = [line.strip() for line in open('input24_.txt').readlines()]
lines = lines[-40:]
c = 0
for line in reversed(lines[:-1]):
    c += 1
    #print(c, len(current_equation))
    #print(current_equation)
    #current_equation =
    parse_line(line, current_equation, rename)
    print(c, tree.size(), line)

print(tree.str2())

#tree.simplify()
#print('\n\n\n', tree.str2())
#assert count_input == 14
#print(current_equation)
#print(rename)

c = [list() for _ in range(30)]
i=0
for line in open('input24.txt').readlines():
    line = line.strip()
    if line.startswith('inp'):
        i=0
    c[i].append(line)
    i+=1

for i in range(len(c)):
    if len(set(c[i])) == 1:
        continue
    print(i, c[i])



"""
mul y 0
add y w    y2=y3+w
add y 12   y1=y2+12
mul y x    y=y1*x
add z y    z+y=0



(((((((p2 + (((m2 + q2) + 10) * r2)) / 26) * ((((0) + 25) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) % 26) + -4) == input1) == 0)) + 1))
 + ((((0) + input1) + 14) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) % 26) + -4) == input1) == 0))) / 26) * ((((0) + 25) * ((((((0) +
  ((((p2 + (((m2 + q2) + 10) * r2)) / 26) * ((((0) + 25) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) % 26) + -4) == input1) == 0)) + 1)) + 
  ((((0) + input1) + 14) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) % 26) + -4) == input1) == 0)))) % 26) + -6) == input0) == 0)) + 1)) + 
  ((((0) + input0) + 12) * ((((((0) + ((((p2 + (((m2 + q2) + 10) * r2)) / 26) * ((((0) + 25) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) %
   26) + -4) == input1) == 0)) + 1)) + ((((0) + input1) + 14) * ((((((0) + (p2 + (((m2 + q2) + 10) * r2))) % 26) + -4) == input1) == 0))))
    % 26) + -6) == input0) == 0)))


inp w    w=input0
mul x 0  x=0
add x z  x=z
mod x 26  x=z%26
div z 1  z=z
add x 14  x=z%26+14
eql x w  x =  (z%26+14) == input0
eql x 0  x =  (z%26+14) != input0
mul y 0  y = 0
add y 25 y=25
mul y x  y = 25 x
add y 1  y = 25 x + 1
mul z y z=z*y
mul y 0 y = 0
add y w y=input0
add y 0
mul y x 
add z y


inp w
mul x 0
add x z
mod x 26
div z 1
add x 14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 0
mul y x
add z y


inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y

block1

(((m1 / 1) * ((((0) + 25) * ((((((0) + m1) % 26) + 14) == input0) == 0)) + 1)) + ((((0) + input0) + 0) *
 ((((((0) + m1) % 26) + 14) == input0) == 0)))


w, x, y, and z. These variables all start with the value 0

inp w   input1
mul x 0 x=0
add x z x=0
mod x 26 x=0
div z 1  z=0
add x 14 x=14
eql x w  x=0
eql x 0 x=1
mul y 0 y=0
add y 25 y=25
mul y x y=25
add y 1 y=26
mul z y z=0
mul y 0 y=0
add y w y=input1
add y 0
mul y x    y = input1*1
add z y    z=input1   y = input1  w = input1 x=1

inp w     w=input2     z=input1   y = input1 x=1
mul x 0   x=0
add x z   x=input1
mod x 26  x=input1 (%26)
div z 1   z=input1
add x 13  x=input1+13
eql x w   x=(input1+13) == w
eql x 0   x=(input1+13) != w
mul y 0   y=0
add y 25  y=25
mul y x   y=25 x
add y 1     y=25 x + 1
mul z y   z=input1*y
mul y 0   y=0
add y w   y=input2
add y 12    y=input2+12
mul y x     
add z y

"""


