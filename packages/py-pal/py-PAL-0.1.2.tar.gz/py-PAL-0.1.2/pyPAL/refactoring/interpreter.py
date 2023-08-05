import inspect
import types
from copy import deepcopy
from ctypes import pythonapi, py_object
from itertools import chain


def get_awaitable(o):
    if inspect.iscoroutine(o) or inspect.isgenerator(o):
        return o
    else:
        return o.__await__()


class BytecodeInterpreter(object):
    """
    Incomplete Python bytecode interpreter. Used if the underlying interpreter does not expose `f_valuestack` on frames.
    This function is used to interpret bytecode instructions within single frames.

    This interpreter uses the same set of opcodes as the CPython equivalent.
    https://github.com/python/cpython/blob/master/Python/ceval.c
    https://docs.python.org/3/library/dis.html

    While the instructions are the same this interpreters only purpose is the emulation of the evaluation stack.
    """
    locals = {}
    globals = {}
    builtins = {}

    def __init__(self, bytecode, instr, locals, globals, builtins):
        self.bytecode = bytecode
        self.target = instr

        self.bytecode_counter = -1

        self.eval_stack = []

        if locals:
            self.locals.update(locals)
        if globals:
            self.globals.update(globals)
        if builtins:
            self.builtins.update(builtins)

    def next_oparg(self):
        self.bytecode_counter += 1

    @property
    def oparg(self):
        return self.bytecode[self.bytecode_counter]

    def target_index(self, target_offset):
        # Return ``bytecode_counter`` at target opcode offset minus one
        return self.bytecode.index(filter(lambda x: x.offset == target_offset, self.bytecode).__next__()) - 1

    def evaluation_stack(self):
        while True:
            self.next_oparg()

            if self.oparg == self.target:
                # Return the evaluation stack before the target opcode is executed
                return self.eval_stack

            # General instructions

            if self.oparg.opname == 'NOP':
                continue

            if self.oparg.opname == 'POP_TOP':
                self.eval_stack.pop()
                continue

            if self.oparg.opname == 'ROT_TWO':
                self.eval_stack[-1], self.eval_stack[-2] = self.eval_stack[-2], self.eval_stack[-1]
                continue

            if self.oparg.opname == 'ROT_THREE':
                self.eval_stack[-1], self.eval_stack[-2], self.eval_stack[-3] = self.eval_stack[-1], self.eval_stack[
                    -2], self.eval_stack[-1]
                continue

            if self.oparg.opname == 'DUP_TOP':
                self.eval_stack.append(self.eval_stack[-1])
                continue

            if self.oparg.opname == 'DUP_TOP_TWO':
                self.eval_stack.extend(self.eval_stack[-2:])
                continue

            # Unary operations

            if self.oparg.opname == 'UNARY_POSITIVE':
                self.eval_stack[-1] += self.eval_stack[-1]
                continue

            if self.oparg.opname == 'UNARY_NEGATIVE':
                self.eval_stack[-1] -= self.eval_stack[-1]
                continue

            if self.oparg.opname == 'UNARY_NOT':
                self.eval_stack[-1] = not self.eval_stack[-1]
                continue

            if self.oparg.opname == 'UNARY_INVERT':
                self.eval_stack[-1] = ~self.eval_stack[-1]
                continue

            if self.oparg.opname == 'GET_ITER':
                self.eval_stack[-1] = iter(deepcopy(self.eval_stack[-1]))
                continue

            if self.oparg.opname == 'GET_YIELD_FROM_ITER':
                if inspect.isgenerator(self.eval_stack[-1]) or inspect.iscoroutine(self.eval_stack[-1]):
                    pass
                else:
                    self.eval_stack[-1] = iter(self.eval_stack[-1])
                continue

            # Binary operations and In-place operations

            if self.oparg.opname in ['BINARY_POWER', 'INPLACE_POWER']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 ** tos)
                continue

            if self.oparg.opname in ['BINARY_MULTIPLY', 'INPLACE_MULTIPLY']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 * tos)
                continue

            if self.oparg.opname in ['BINARY_MATRIX_MULTIPLY', 'INPLACE_MATRIX_MULTIPLY']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 @ tos)
                continue

            if self.oparg.opname in ['BINARY_FLOOR_DIVIDE', 'INPLACE_FLOOR_DIVIDE']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 // tos)
                continue

            if self.oparg.opname in ['BINARY_TRUE_DIVIDE', 'INPLACE_TRUE_DIVIDE']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 / tos)
                continue

            if self.oparg.opname in ['BINARY_MODULO', 'INPLACE_MODULO']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 % tos)
                continue

            if self.oparg.opname in ['BINARY_ADD', 'INPLACE_ADD']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 + tos)
                continue

            if self.oparg.opname in ['BINARY_SUBTRACT', 'INPLACE_SUBTRACT']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 - tos)
                continue

            if self.oparg.opname == 'STORE_SUBSCR':
                sub = self.eval_stack.pop()
                container = self.eval_stack.pop()
                v = self.eval_stack.pop()
                container[sub] = v
                continue

            if self.oparg.opname == 'BINARY_SUBSCR':
                sub = self.eval_stack.pop()
                container = self.eval_stack.pop()
                self.eval_stack.append(container[sub])
                continue

            if self.oparg.opname in ['BINARY_LSHIFT', 'INPLACE_LSHIFT']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 << tos)
                continue

            if self.oparg.opname in ['BINARY_RSHIFT', 'INPLACE_RSHIFT']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 >> tos)
                continue

            if self.oparg.opname in ['BINARY_AND', 'INPLACE_AND']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 & tos)
                continue

            if self.oparg.opname in ['BINARY_XOR', 'INPLACE_XOR']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 ^ tos)
                continue

            if self.oparg.opname in ['BINARY_OR', 'INPLACE_OR']:
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                self.eval_stack.append(tos1 | tos)
                continue

            if self.oparg.opname == 'DELETE_SUBSCR':
                sub = self.eval_stack.pop()
                container = self.eval_stack[-1]
                del container[sub]
                continue

            # Coroutine opcodes

            if self.oparg.opname == 'GET_AWAITABLE':
                self.eval_stack.append(get_awaitable(self.eval_stack[-1]))
                continue

            if self.oparg.opname == 'GET_AITER':
                self.eval_stack[-1] = self.eval_stack[-1].__aiter__()
                continue

            if self.oparg.opname == 'GET_ANEXT':
                self.eval_stack.append(get_awaitable(self.eval_stack[-1].__anext__()))
                continue

            if self.oparg.opname == 'BEFORE_ASYNC_WITH':
                aenter = self.eval_stack[-1].__aenter__()
                aexit = self.eval_stack[-1].__aexit__()
                self.eval_stack.append(aexit)
                self.eval_stack.append(aenter)
                continue

            if self.oparg.opname == 'SETUP_ASYNC_WITH':
                # Nothing to do here
                continue

            # Miscellaneous opcodes

            if self.oparg.opname == 'PRINT_EXPR':
                self.eval_stack.pop()
                continue

            if self.oparg.opname == 'BREAK_LOOP':
                # Nothing to do here
                # Has no occurrence in CPython source
                continue

            if self.oparg.opname == 'CONTINUE_LOOP':
                # Has no occurrence in CPython source
                self.bytecode_counter = self.target_index(self.oparg.argval)
                continue

            if self.oparg.opname == 'SET_ADD':
                v = self.eval_stack.pop()
                _set = self.eval_stack[-self.oparg.argval]
                set.add(_set, v)
                continue

            if self.oparg.opname == 'LIST_APPEND':
                v = self.eval_stack.pop()
                _list = self.eval_stack[-self.oparg.argval]
                list.append(_list, v)
                continue

            if self.oparg.opname == 'MAP_ADD':
                value = self.eval_stack.pop()
                key = self.eval_stack.pop()
                dict.__setitem__(self.eval_stack[-self.oparg.argval], key, value)
                continue

            if self.oparg.opname == 'RETURN_VALUE':
                # ??
                # retval = self.eval_stack.pop()
                break

            if self.oparg.opname == 'YIELD_VALUE':
                # ??
                # retval = self.eval_stack.pop()
                break

            if self.oparg.opname == 'YIELD_FROM':
                # ??
                # v = self.eval_stack.pop()
                # receiver = self.eval_stack[-1]
                break

            if self.oparg.opname == 'SETUP_ANNOTATIONS':
                # ??
                continue

            if self.oparg.opname == 'IMPORT_STAR':
                # ??
                _from = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'POP_BLOCK':
                # self.eval_stack = self.block_stack.pop()
                continue

            if self.oparg.opname == 'POP_EXCEPT':
                # self.block_stack.pop()
                continue

            if self.oparg.opname == 'END_FINALLY':
                # ??
                exc = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'LOAD_BUILD_CLASS':
                # ??
                self.eval_stack.append(self.builtins.__build_class__())
                continue

            if self.oparg.opname == 'SETUP_WITH':
                # ??
                continue

            if self.oparg.opname == 'WITH_CLEANUP_START':
                # ??
                continue

            if self.oparg.opname == 'WITH_CLEANUP_FINISH':
                # ??
                continue

            if self.oparg.opname == 'STORE_NAME':
                self.locals[self.oparg.argval] = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'STORE_FAST':
                self.locals[self.oparg.argval] = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'STORE_GLOBAL':
                self.globals[self.oparg.argval] = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'DELETE_NAME':
                del self.locals[self.oparg.argval]
                continue

            if self.oparg.opname == 'UNPACK_SEQUENCE':
                tos = self.eval_stack.pop()
                self.eval_stack.extend(tos)
                continue

            if self.oparg.opname == 'UNPACK_EX':
                tos = self.eval_stack.pop()
                for _ in self.oparg.argval & 0xFF:
                    self.eval_stack.append(tos.__next__())
                self.eval_stack.append(list(tos))
                continue

            if self.oparg.opname == 'STORE_ATTR':
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()
                tos[self.oparg.argval] = tos1
                continue

            if self.oparg.opname == 'DELETE_ATTR':
                tos = self.eval_stack.pop()
                delattr(tos, self.oparg.argval)
                continue

            if self.oparg.opname == 'DELETE_GLOBAL':
                del self.globals[self.oparg.argval]
                continue

            if self.oparg.opname == 'LOAD_CONST':
                self.eval_stack.append(self.oparg.argval)
                continue

            if self.oparg.opname == 'LOAD_NAME':
                # Search own namespace first, try to be side-effect free
                if self.oparg.argval in self.locals:
                    self.eval_stack.append(self.locals[self.oparg.argval])
                    continue
                if self.oparg.argval in self.builtins:
                    self.eval_stack.append(self.builtins[self.oparg.argval])
                    continue

            if self.oparg.opname == 'LOAD_GLOBAL':
                # Search own namespace first, try to be side-effect free

                if self.oparg.argval in self.globals:
                    self.eval_stack.append(self.globals[self.oparg.argval])
                    continue
                if self.oparg.argval in self.builtins:
                    self.eval_stack.append(self.builtins[self.oparg.argval])
                    continue

            if self.oparg.opname == 'LOAD_FAST':
                if self.oparg.argval in self.locals:
                    self.eval_stack.append(self.locals[self.oparg.argval])
                    continue

            if self.oparg.opname == 'BUILD_TUPLE':
                t = tuple(self.eval_stack[-self.oparg.argval:])
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(t)
                continue

            if self.oparg.opname == 'BUILD_LIST':
                l = list(self.eval_stack[-self.oparg.argval:])
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(l)
                continue

            if self.oparg.opname == 'BUILD_SET':
                s = set(self.eval_stack[-self.oparg.argval:])
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(s)
                continue

            if self.oparg.opname == 'BUILD_MAP':
                m = self.eval_stack[-self.oparg.argval * 2:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval * 2]
                self.eval_stack.append({k: v for k, v in zip(m[::2], m[1::2])})
                continue

            if self.oparg.opname == 'BUILD_CONST_KEY_MAP':
                keys = self.eval_stack.pop()
                values = tuple(self.eval_stack[-self.oparg.argval:])
                self.eval_stack = self.eval_stack[:-self.oparg.argval * 2]
                self.eval_stack.append({k: v for k, v in zip(keys, values)})
                continue

            if self.oparg.opname == 'BUILD_STRING':
                t = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append("".join(t))
                continue

            if self.oparg.opname == 'BUILD_TUPLE_UNPACK':
                t = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(tuple(chain(*t)))
                continue

            if self.oparg.opname == 'BUILD_TUPLE_UNPACK_WITH_CALL':
                t = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                arg = tuple(chain(*t))
                function = self.get_callable()
                self.eval_stack.append(function(arg))
                continue

            if self.oparg.opname == 'BUILD_LIST_UNPACK':
                l = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(list(chain(*l)))
                continue

            if self.oparg.opname == 'BUILD_SET_UNPACK':
                s = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(set(chain(*s)))
                continue

            if self.oparg.opname == 'BUILD_MAP_UNPACK':
                m = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                d = {}
                for _m in m:
                    d.update(_m)
                self.eval_stack.append(d)
                continue

            if self.oparg.opname == 'BUILD_MAP_UNPACK_WITH_CALL':
                m = self.eval_stack[-self.oparg.argval:]
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                d = {}
                for _m in m:
                    d.update(_m)
                function = self.get_callable()
                self.eval_stack.append(function(**d))
                continue

            if self.oparg.opname == 'LOAD_ATTR':
                tos = self.eval_stack.pop()
                self.eval_stack.append(getattr(tos, self.oparg.argval))
                continue

            if self.oparg.opname == 'COMPARE_OP':
                right = self.eval_stack.pop()
                left = self.eval_stack.pop()

                if self.oparg.argval == '<':
                    self.eval_stack.append(left < right)
                    continue

                if self.oparg.argval == '<=':
                    self.eval_stack.append(left <= right)
                    continue

                if self.oparg.argval == '==':
                    self.eval_stack.append(left == right)
                    continue

                if self.oparg.argval == '!=':
                    self.eval_stack.append(left != right)
                    continue

                if self.oparg.argval == '>':
                    self.eval_stack.append(left > right)
                    continue

                if self.oparg.argval == '>=':
                    self.eval_stack.append(left >= right)
                    continue

                if self.oparg.argval == 'in':
                    self.eval_stack.append(left in right)
                    continue

                if self.oparg.argval == 'not in':
                    self.eval_stack.append(left not in right)
                    continue

                if self.oparg.argval == 'is':
                    self.eval_stack.append(left is right)
                    continue

                if self.oparg.argval == 'is not':
                    self.eval_stack.append(left is not right)
                    continue

            if self.oparg.opname == 'IMPORT_NAME':
                tos = self.eval_stack.pop()
                tos1 = self.eval_stack.pop()

                self.eval_stack.append(__import__(self.oparg.argval, fromlist=tos, level=tos1))
                continue

            if self.oparg.opname == 'IMPORT_FROM':
                # TODO: check this
                tos = self.eval_stack[-1]

                self.eval_stack.append(getattr(tos, self.oparg.argval))
                continue

            if self.oparg.opname == 'JUMP_FORWARD':
                self.bytecode_counter = self.target_index(self.oparg.offset + self.oparg.argval)
                continue

            if self.oparg.opname == 'POP_JUMP_IF_TRUE':
                tos = self.eval_stack.pop()
                if tos:
                    self.bytecode_counter = self.target_index(self.oparg.argval)
                continue

            if self.oparg.opname == 'POP_JUMP_IF_FALSE':
                tos = self.eval_stack.pop()
                if not tos:
                    self.bytecode_counter = self.target_index(self.oparg.argval)
                continue

            if self.oparg.opname == 'JUMP_IF_TRUE_OR_POP':
                if self.eval_stack[-1]:
                    self.bytecode_counter = self.target_index(self.oparg.argval)
                else:
                    self.eval_stack.pop()
                continue

            if self.oparg.opname == 'JUMP_IF_FALSE_OR_POP':
                if not self.eval_stack[-1]:
                    self.bytecode_counter = self.target_index(self.oparg.argval)
                else:
                    self.eval_stack.pop()
                continue

            if self.oparg.opname == 'JUMP_ABSOLUTE':
                self.bytecode_counter = self.target_index(self.oparg.argval)
                continue

            if self.oparg.opname == 'FOR_ITER':
                try:
                    value = self.eval_stack[-1].__next__()
                    self.eval_stack.append(value)
                except StopIteration as e:
                    self.eval_stack.pop()
                    self.bytecode_counter = self.target_index(self.oparg.argval)
                continue

            if self.oparg.opname == 'SETUP_LOOP':
                # self.block_stack.append(self.eval_stack)
                # self.eval_stack = []
                continue

            if self.oparg.opname == 'SETUP_EXCEPT':
                # No usage in CPython source
                continue

            if self.oparg.opname == 'SETUP_FINALLY':
                # ??
                continue

            if self.oparg.opname == 'DELETE_FAST':
                # Nothing to delete if nothing is stored
                continue

            if self.oparg.opname == 'LOAD_CLOSURE':
                self.eval_stack.append(self.oparg.argval)
                continue

            if self.oparg.opname == 'LOAD_DEREF':
                self.eval_stack.append(self.locals[self.oparg.argval])
                continue

            if self.oparg.opname == 'LOAD_CLASSDEREF':
                self.eval_stack.append(self.locals[self.oparg.argval])
                continue

            if self.oparg.opname == 'STORE_DEREF':
                self.locals[self.oparg.argval] = self.eval_stack.pop()
                continue

            if self.oparg.opname == 'DELETE_DEREF':
                del self.locals[self.oparg.argval]
                continue

            if self.oparg.opname == 'RAISE_VARARGS':
                if self.oparg.argval == 2:
                    tos = self.eval_stack.pop()
                    tos1 = self.eval_stack.pop()
                    raise tos1 from tos
                if self.oparg.argval == 1:
                    raise self.eval_stack.pop()
                if self.oparg.argval == 0:
                    raise Exception("Re-raise previous exception")

                raise Exception("RAISE_VARARGS without argval")

            if self.oparg.opname == 'CALL_FUNCTION':
                args = []
                if self.oparg.argval > 0:
                    args = self.eval_stack[-self.oparg.argval:]
                    self.eval_stack = self.eval_stack[:-self.oparg.argval]

                function = self.get_callable()
                self.eval_stack.append(function(*args))
                continue

            if self.oparg.opname == 'CALL_FUNCTION_KW':
                kw = self.eval_stack.pop()
                args = []
                if self.oparg.argval > 0:
                    args = self.eval_stack[-self.oparg.argval:]
                    self.eval_stack = self.eval_stack[:-self.oparg.argval]

                kwargs = {}
                for key in kw:
                    kwargs.update({key: args.pop()})

                function = self.get_callable()
                self.eval_stack.append(function(*args, **kwargs))
                continue

            if self.oparg.opname == 'CALL_FUNCTION_EX':
                kwargs = {}
                # if self.oparg.argval & (1 << self.oparg.argval.bit_length()):
                if self.oparg.argval:
                    kwargs = self.eval_stack.pop()
                args = self.eval_stack.pop()
                function = self.get_callable()
                self.eval_stack.append(function(*args, **kwargs))
                continue

            if self.oparg.opname == 'LOAD_METHOD':
                tos = self.eval_stack.pop()
                self.eval_stack.append(getattr(tos, self.oparg.argval))
                self.eval_stack.append(tos)
                continue

            if self.oparg.opname == 'CALL_METHOD':
                args = []
                if self.oparg.argval > 0:
                    args = self.eval_stack[-self.oparg.argval:]
                    self.eval_stack = self.eval_stack[:-self.oparg.argval]

                _self = self.eval_stack.pop()
                method = self.eval_stack.pop()
                self.eval_stack.append(method(*args))
                continue

            if self.oparg.opname == 'MAKE_FUNCTION':
                qualname = self.eval_stack.pop()
                code_obj = self.eval_stack.pop()
                func_closure = None
                func_annotations = None
                func_kwdefaults = None
                func_defaults = None

                if self.oparg.argval & 0x08:
                    func_closure = self.eval_stack.pop()
                if self.oparg.argval & 0x04:
                    func_annotations = self.eval_stack.pop()
                if self.oparg.argval & 0x02:
                    func_kwdefaults = self.eval_stack.pop()
                if self.oparg.argval & 0x01:
                    func_defaults = self.eval_stack.pop()

                # Fetch reference to cell creation function
                _PyCell_New = pythonapi.PyCell_New
                # PyCell_New returns a py_object
                _PyCell_New.restype = py_object

                if func_closure:
                    func_closure = tuple((_PyCell_New(py_object(self.locals[arg])) for arg in func_closure))

                function = types.FunctionType(code_obj, self.globals, qualname, closure=func_closure)

                function.__annotations__ = func_annotations
                function.__kwdefaults__ = func_kwdefaults
                function.__defaults__ = func_defaults

                self.eval_stack.append(function)
                continue

            if self.oparg.opname == 'BUILD_SLICE':
                t = tuple(self.eval_stack[-self.oparg.argval:])
                self.eval_stack = self.eval_stack[:-self.oparg.argval]
                self.eval_stack.append(slice(*t))
                continue

            if self.oparg.opname == 'EXTENDED_ARG':
                oldoparg = self.oparg.argval
                self.next_oparg()
                self.oparg.argval |= oldoparg << 8
                continue

            if self.oparg.opname == 'FORMAT_VALUE':
                if self.oparg.argval & 0x03 == 0x00:
                    pass
                if self.oparg.argval & 0x03 == 0x01:
                    self.eval_stack[-1] = str(self.eval_stack[-1])
                if self.oparg.argval & 0x03 == 0x02:
                    self.eval_stack[-1] = repr(self.eval_stack[-1])
                if self.oparg.argval & 0x03 == 0x03:
                    self.eval_stack[-1] = ascii(self.eval_stack[-1])
                if self.oparg.argval & 0x04 == 0x04:
                    fmt_spec = self.eval_stack.pop()
                    self.eval_stack[-1] = format(fmt_spec, self.eval_stack[-1])

                continue

            if self.oparg.opname == 'HAVE_ARGUMENT':
                continue

    def get_callable(self):
        function = self.eval_stack.pop()

        if callable(function) or inspect.isclass(function) or inspect.isroutine(function):
            return function
        if function in self.builtins:
            return self.builtins[function]
        if function in self.locals:
            return self.locals[function]
        if function in self.globals:
            return self.globals[function]
