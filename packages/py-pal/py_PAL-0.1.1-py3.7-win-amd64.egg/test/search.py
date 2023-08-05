# O(log n)
def binary_search(data, value):
    n = len(data)
    left = 0
    right = n - 1
    while left <= right:
        middle = round((left + right) / 2)
        if value < data[middle]:
            right = middle - 1
        elif value > data[middle]:
            left = middle + 1
        else:
            return middle
    return -1


# O(n)
def linear_search(data, value):
    for index in range(len(data)):
        if value == data[index]:
            return index
    return -1
