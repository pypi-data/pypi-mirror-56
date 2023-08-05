from test import quick_sort, merge_sort, bubble_sort

for f in [merge_sort, quick_sort, bubble_sort]:
    f([1, 2, 3, 23123, 323, 3, 222])
    f([1, 2, 3, 23123, 323, 3, 222] * 10)
    f([1, 2, 3, 23123, 323, 3, 222] * 20)
