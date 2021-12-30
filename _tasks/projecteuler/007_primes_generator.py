# what is 10_001'th prime

def primes_generator():
    primes = [2]
    yield primes[-1]
    n = 3
    while True:
        n_sqrt = int(n ** 0.5) + 1
        indx = 0
        is_prime = True
        while indx < len(primes) and primes[indx] <= n_sqrt:
            if n % primes[indx] == 0:
                is_prime = False
                break
            indx += 1
        if is_prime:
            primes.append(n)
            yield n
        n += 2

if __name__ == '__main__':
    print([p for _, p in zip(range(10_001), primes_generator())][-1])