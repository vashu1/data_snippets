
lines = open('input2.txt').readlines()
paper_area = 0
ribbon_len = 0
for line in lines:
    data = line.strip().split('x')
    a,b,c = map(int, data)
    assert a>0 and b>0 and c>0
    ribbon_len += (a+b+c - max(a,b,c))*2 + a*b*c
    a,b,c = a*b, b*c, c*a
    paper_area += 2 * (a+b+c) + min(a,b,c)

print(paper_area)
print(ribbon_len)