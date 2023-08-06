from collections import deque

import numpy as np

cdef tuple WHAT_NAMES = ("call", "exception", "line", "return", "c_call", "c_exception", "c_return", "opcode")

cdef class Tracer:
    def __init__(self):
        self.blacklist = [
            "py_pal.tracer",
            "importlib._bootstrap",
            "importlib._bootstrap_external"
        ]

        self.call_id = 0
        self.calls = [(self.call_id, 0, '__main__', 0, '<module>', None, None, None, None, None, None, None, None)]
        self.opcodes = {}
        self.f_weight_map = {}
        self.call_stack = [(self.call_id, 0)]
        self.call_id += 1

    def __call__(self, frame, what, arg):
        if frame.f_globals.get('__name__', '') not in self.blacklist:
            # Do not measure inside of tracing machinery
            PyEval_SetTrace(<Py_tracefunc> trace_func, <PyObject *> self)

        return self

    def trace(self):
        PyEval_SetTrace(<Py_tracefunc> trace_func, <PyObject *> self)
        return self

    def stop(self):
        PyEval_SetTrace(NULL, NULL)

    cpdef get_call_stats(self):
        return np.asarray(self.calls)

    cpdef get_opcode_stats(self):
        return np.asarray([(*k, v) for k, v in self.opcodes.items()])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

# TODO: options to improve profiling performance:
#   - profile, identify bottlenecks
#   - sampling (problem with the way statistics are captured, must be at the root of the tree...)

cdef get_func_in_mro(obj, code):
    """Attempt to find a function in a side-effect free way.

    This looks in obj's mro manually and does not invoke any descriptors.
    """

    # TODO: replace getattr with getattr_static
    val = getattr(obj, code.co_name, None)
    if val is None:
        return None
    if isinstance(val, (classmethod, staticmethod)):
        candidate = val.__func__
    elif isinstance(val, property) and (val.fset is None) and (val.fdel is None):
        candidate = val.fget
    else:
        candidate = val
    return if_same_code(candidate, code)

cdef object if_same_code(object func, CodeType code):
    while func is not None:
        func_code = getattr(func, '__code__', None)
        if func_code is code:
            return func
        # Attempt to find the decorated function
        func = getattr(func, '__wrapped__', None)
    return None

cdef object get_function_object(FrameType frame):
    cdef CodeType code = frame.f_code

    if code.co_name is None:
        return None

    # First, try to find the function in globals
    candidate = frame.f_globals.get(code.co_name, None)
    func = if_same_code(candidate, code)
    # If that failed, as will be the case with class and instance methods, try
    # to look up the function from the first argument. In the case of class/instance
    # methods, this should be the class (or an instance of the class) on which our
    # method is defined.
    if func is None and code.co_argcount >= 1:
        first_arg = frame.f_locals.get(code.co_varnames[0])
        func = get_func_in_mro(first_arg, code)
    # If we still can't find the function, as will be the case with static methods,
    # try looking at classes in global scope.
    if func is None:
        for v in frame.f_globals.values():
            if not isinstance(v, type):
                continue
            func = get_func_in_mro(v, code)
            if func is not None:
                break

    # TODO: return module if function name is not present and rename to 'get_call_object'
    return func

cdef int last_lineno

cdef int trace_func(Tracer self, FrameType frame, int what, PyObject *arg) except -1:
    """
    The events are emitted after opcode execution.
    Use the call and return events to structure the calls into a hierarchy.
    """
    frame.f_trace_opcodes = 1
    frame.f_trace_lines = 0

    global last_lineno

    #if frame.f_globals.get('__name__', '') in self.blacklist:
    #    return 0

    # if what == 1:
    #    print(<str> arg)
    # self.stop()

    if what == 0:
        # event: call

        # Add call as row (module, function, args, kwargs, children)
        self.call_stack.append((self.call_id, last_lineno))

        PyFrame_FastToLocals(frame)
        _args, kwonlyargs, _varargs, _varkw = _getfullargs(frame.f_code)

        if isinstance(_args, list):
            _args = tuple(_args)

        if isinstance(kwonlyargs, list):
            kwonlyargs = tuple(kwonlyargs)

        if isinstance(_varargs, list):
            _varargs = tuple(_varargs)

        if isinstance(_varkw, list):
            _varkw = tuple(_varkw)

        args = tuple(map(lambda x: frame.f_locals[x], _args)) if _args else ()
        kwargs = tuple(map(lambda x: frame.f_locals[x], kwonlyargs)) if kwonlyargs else ()
        varargs = frame.f_locals[_varargs] if _varargs else ()
        varkw = frame.f_locals[_varkw].values() if _varkw else ()

        self.calls.append((
            self.call_id,
            id(frame.f_code),
            frame.f_code.co_filename,
            frame.f_lineno,
            frame.f_code.co_name,
            _args,
            tuple(map(lambda x: get_input_factor(x), args)) if args else None,
            kwonlyargs,
            tuple(map(lambda x: get_input_factor(x), kwargs)) if kwargs else None,
            _varargs,
            tuple(map(lambda x: get_input_factor(x), varargs)) if varargs else None,
            _varkw,
            tuple(map(lambda x: get_input_factor(x), varkw)) if varkw else None
        ))
        self.call_id += 1

    elif what == 3:
        # event: return
        if len(self.call_stack) > 1:
            child = self.call_stack.pop()

        # Add opcode weight to parent call
        parent = self.call_stack[len(self.call_stack) - 1]
        value = self.f_weight_map.get(child[0], 0)
        parent_weight = self.opcodes.get(parent, 0)
        self.opcodes.update({parent: parent_weight + value})

        _value = self.f_weight_map.get(parent[0], 0)
        self.f_weight_map.update({parent[0]: _value + value})

    elif what == 7:
        # event: opcode
        # Anything in here should cause minimal overhead
        last_lineno = frame.f_lineno

        # Save opcode weight per line in current call
        call = self.call_stack[len(self.call_stack) - 1][0]
        key = (call, frame.f_lineno)
        value_line = self.opcodes.get(key, 0)
        self.opcodes.update({key: value_line + 1})

        # Keep track of all opcodes executed within call
        value = self.f_weight_map.get(call, 0)
        self.f_weight_map.update({call: value + 1})

        return 0

        # TODO: Insert opcode metric
        # TODO: if oparg of opcode is needed use: 'get_arg' from frameobject.c !

        """
        op = frame.f_code.co_code[frame.f_lasti]
        last_op = opname[op]

        if op == 81:
            # WITH_CLEANUP_START
            pass

        elif op == 143:
            # SETUP_WITH
            pass

        elif op == 93:
            # FOR_ITER
            pass

        elif op == 86:
            # YIELD_VALUE
            pass

        elif op == 83:
            # RETURN_VALUE
            pass

        elif op == 68:
            # GET_ITER
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, 1)

            # Make a copy because generators cannot be copied, may be needed in CALL_FUNCTION_EX
            if not isinstance(valuestack[-1], GeneratorType):
                self.last_gen = iter(valuestack[-1])

        elif op == 131:
            # CALL_FUNCTION

            # TODO: Look into cpython's 'ceval.c' and use already implemented
            #  functionality to determine arguments for opcode weight calculation

            argc = get_argval(frame.f_code, frame.f_lasti)
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 1)
            f_last = (valuestack[0], valuestack[1:], None)

            # (valuestack[0], valuestack[1:], None)

        elif op == 141:
            # CALL_FUNCTION_KW
            argc = get_argval(frame.f_code, frame.f_lasti)
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)

            kw = valuestack[-1]
            args = valuestack[-(argc + 1):-1]
            kwargs = {k: v for k, v in zip(kw, args[::-1])}
            args = args[:-len(kw)]

            # (valuestack[0], args, kwargs)

        elif op == 142:
            # CALL_FUNCTION_EX
            argc = get_argval(frame.f_code, frame.f_lasti)

            if argc:
                valuestack = <list> get_valuestack(<PyFrameObject*> frame, 3)
                kwargs = valuestack[-1]
                args = valuestack[-2]
                function = valuestack[-3]
            else:
                valuestack = <list> get_valuestack(<PyFrameObject*> frame, 2)
                kwargs = {}
                args = valuestack[-1]
                function = valuestack[-2]

            f_last = (
                function,
                args if not isinstance(args, GeneratorType) else self.last_gen,
                kwargs
            )

            #(
            #    function,
            #    args if not isinstance(args, GeneratorType) else self.last_gen,
            #    kwargs
            #)

        elif op == 151:
            # BUILD_MAP_UNPACK_WITH_CALL
            argc = get_argval(frame.f_code, frame.f_lasti)
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)

            m = valuestack[-argc:]
            args = {}
            for _m in m:
                args.update(_m)

            # (valuestack[0], args, None)

        elif op == 158:
            # BUILD_TUPLE_UNPACK_WITH_CALL
            argc = get_argval(frame.f_code, frame.f_lasti)
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 1)
            t = valuestack[-argc:]
            args = tuple(chain(*t))

            # (valuestack[0], args, None)

        elif op == 161:
            # CALL_METHOD
            argc = get_argval(frame.f_code, frame.f_lasti)
            valuestack = <list> get_valuestack(<PyFrameObject*> frame, argc + 2)
            method = valuestack[0]
            instance = valuestack[1]
            args = ()
            if argc > 0:
                args = valuestack[-1:]
            if not method:
                method = instance

            #(method, args, None)
        """
    return 0

cdef Py_ssize_t get_input_factor(arg):
    """
    Proxy for input arguments. Is used to infer complexity with the least squares algorithm.
    Therefore all returned values have to be positive and greater than zero.
    """
    if arg is None or NULL or isinstance(arg, (bool, np.bool)):
        return 1

    elif isinstance(arg, np.ndarray):
        return sum(arg.shape)

    elif isinstance(arg, np.generic):
        value = abs(int(arg))
        return value if value > 0 else 1

    elif isinstance(arg, int):
        # The memory size of an ``int`` object is constant.
        # Return ``int`` value to be able to derive simple algorithms.
        if arg == 0:
            return 1
        return abs(arg)

    elif isinstance(arg, (list, dict, set, deque, str, tuple)):
        # Length of collections
        l = len(arg)
        return l if l > 0 else 1

    else:
        return sizeof(arg)

cdef _getfullargs(co):
    nargs = co.co_argcount
    names = co.co_varnames
    nkwargs = co.co_kwonlyargcount
    args = list(names[:nargs])
    kwonlyargs = list(names[nargs:nargs + nkwargs])

    nargs += nkwargs
    varargs = None
    if co.co_flags & 4:
        varargs = co.co_varnames[nargs]
        nargs = nargs + 1
    varkw = None
    if co.co_flags & 8:
        varkw = co.co_varnames[nargs]
    return args, kwonlyargs, varargs, varkw
