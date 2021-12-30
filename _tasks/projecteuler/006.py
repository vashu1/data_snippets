
squares_sum = 0
n_sum = 0
sum_square = 0
diff = 0

N = 100
for n in range(1, N+1):
    n2 = n**2
    #squares_sum += n2
    #sum_square += n_sum*2*n + n2
    diff += n_sum * 2 * n
    n_sum += n


print(sum(range(N+1))**2-sum([n**2 for n in range(N+1)]))
print(diff)

'''
squares_sum = squares_sum_1 + n**2
n_sum**2 = n_sum_1**2 + 2*n_sum_1*n+n**2
n_sum**2 - squares_sum +=

(n+1) * (n+1) = n2 + 2n1 + 1

'''