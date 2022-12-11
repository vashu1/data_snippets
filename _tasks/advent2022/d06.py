input_test = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

input_full = open('d06.txt').readlines()
input_full = input_full[0].strip()

input = input_full
HEADER_LEN = 14
for indx in range(len(input)-HEADER_LEN):
    if len(set(input[indx:indx+HEADER_LEN])) == HEADER_LEN:
        print(indx+HEADER_LEN)
        break

