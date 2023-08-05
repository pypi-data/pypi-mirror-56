def gen(low, high, next):
    current = low
    cnt = low
    while cnt < high:
        yield current
        current = next(current)
        cnt = cnt + 1


def summation(low, high, f, next):
    #current = low
    #values = []
    #cnt = low
    #while cnt < high:
    #    cnt = cnt + 1
    #    values.append(current)
    #    current = next(current)
    #return sum((f(x) for x in values))
    return sum((f(x) for x in gen(low, high, next)))


def calcPi():
    for x in range(100):
        summation(1, 100, lambda x: 1.0/x**2, lambda y: y+2)
    return (8 * summation(1, 10, lambda x: 1.0/x**2, lambda x: x+2))**0.5


def main():
    print(calcPi())

if __name__ == "__main__":
    main()