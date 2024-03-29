import truthtables as tt

primes = []
for num in range(2, 1000):
    if all(num % i != 0 for i in range(2, num)):
        primes += [num]

p1 = ''
for i in range(1 << 12):
    di = format(i, "012b")
    d1 = int(di[0:4], 2)
    d2 = int(di[4:8], 2)
    d3 = int(di[8:12], 2)

    if d1 > 9 or d2 > 9 or d3 > 9:
        p1 += 'x'
    elif i in primes:
        p1 += '1'
    else:
        p1 += '0'

p2 = ''.join([str(int(i in primes)) for i in range(1000)])

p3 = ''
for i in range(1 << 8):
    di = format(i, "08b")
    d1 = int(di[0:4], 2)
    d2 = int(di[4:8], 2)
    p = 10 * d1 + d2
    if d1 > 9 or d2 > 9:
        p3 += 'x'
    elif p in primes:
        p3 += '1'
    else:
        p3 += '0'

p4 = ''.join([str(int(i in primes)) for i in range(100)])

p5 = ''
for i in range(1 << 7):
    di = format(i << 1, "08b")
    d1 = int(di[0:4], 2)
    d2 = int(di[4:8], 2)
    p = 10 * d1 + d2
    if d1 > 9 or d2 > 9:
        p5 += 'x'
    elif p + 1 in primes:
        p5 += '1'
    else:
        p5 += '0'

print(p5)

# P3 IS BEST!
ptt = tt.TT(p5)
ptt.formula()
print(ptt)




