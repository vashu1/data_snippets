
v = 600_851_475_143

# about 1e12, so factor below 1e6

print(v)
while v > 1:
    for i in range(2, int(1e6)):
        if v%i == 0:
            v //= i
            print(v, i)
            break

print(i)