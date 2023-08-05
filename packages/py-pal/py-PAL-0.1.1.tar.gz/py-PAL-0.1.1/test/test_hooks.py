from pyPAL.refactoring import profile, profiling

# Example usage
"""
@wrap
def foo():
    a = [1, 2, 3]
    a.append(4)
    print('asd')


t = Tracer().trace()

a = [1, 2, 3]
a.append(4)
print('asd')

t.stop()

print('------------------')

with trace():
    a = [1, 2, 3]
    a.append(4)
    print('asd')

print('------------------')
foo()

"""


@profile
def foo(a):
    a.append(4)
    t = a[2:len(a)]
    if len(a) < 6:
        foo(a)
    sorted(t, key=None)


@profile
def foo2(a):
    a.append(4)
    t = a[2:len(a)]
    if len(a) < 6:
        foo2(a)
    sorted(t, key=None)


foo([1, 2, 3])
foo2([1, 2, 3])
foo([1]*2)