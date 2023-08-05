import dis
from abc import ABC, abstractmethod
from copy import deepcopy
from itertools import chain

from pyPAL.call_metric import avg_builtin_method_complexity, avg_builtin_function_complexity


def get_bc_and_instr(frame):
    code = frame.f_code
    bytecode = deepcopy(list(dis.get_instructions(code)))
    if frame.f_lasti > 0:
        instr = filter(lambda x: x.offset == frame.f_lasti, bytecode).__next__()
        return bytecode, instr
    else:
        return bytecode, None


class OpcodeMetricBase(ABC):
    @abstractmethod
    def get_value(self, frame, value_stack_callback):
        raise NotImplementedError()


class SimpleOpcodeMetric(OpcodeMetricBase):
    def get_value(self, frame, value_stack_callback):
        opcode = frame.f_code.co_code[frame.f_lasti]
        opname = dis.opname[opcode]
        return opname, 1


class OpcodeMetric(OpcodeMetricBase):
    def __init__(self, mcm=avg_builtin_method_complexity, fcm=avg_builtin_function_complexity):
        self.method_complexity_map = mcm
        self.function_complexity_map = fcm

    def get_value(self, frame, value_stack_callback):
        opcode = frame.f_code.co_code[frame.f_lasti]
        opname = dis.opname[opcode]

        if opname == "BINARY_POWER":
            # TODO: implement complexity calculation
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

        if opname == "BINARY_POWER":
            # TODO: implement O(log n)
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

        if opname == "BINARY_MATRIX_MULTIPLY":
            # m-by-n matrix by an n-by-p matrix has complexity O(mnp)
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)
            # m_x_n = value_stack[0]
            # n_x_p = value_stack[1]
            # TODO: implement O(m*n*p)

        if opname == "GET_ITER":
            # Iteration, O(len(...))
            # TODO: fix this
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)
            return opname, 1 #len(list(value_stack[-1]))

        if opname == 'DELETE_SUBSCR':
            # O(len(...)), del list[i]
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if isinstance(value_stack[-2], list):
                return opname, len(value_stack[-2])

        if opname == 'BUILD_SLICE':
            # O(len(...))
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)
            if instr.argval == 2:
                return opname, len(value_stack[-3][value_stack[-2]:value_stack[-1]])
            else:
                return opname, len(value_stack[-4][value_stack[-3]:value_stack[-2]:value_stack[-1]])

        if opname in [
            'BUILD_TUPLE', 'BUILD_LIST', 'BUILD_SET', 'BUILD_MAP', 'BUILD_CONST_KEY_MAP', 'BUILD_STRING',
            'BUILD_TUPLE_UNPACK', 'BUILD_LIST_UNPACK', 'BUILD_SET_UNPACK', 'BUILD_MAP_UNPACK'
        ]:
            # O(len(...))
            _, instr = get_bc_and_instr(frame)
            if instr:
                return opname, instr.argval

        # Function and method calls

        if opname == 'CALL_FUNCTION':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            function = value_stack[-(instr.argval + 1)]

            if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                return opname, 1

            arguments = value_stack[-instr.argval:]
            complexity = self.function_complexity_map[function.__qualname__]
            return opname, complexity(*arguments).value

        if opname == 'CALL_FUNCTION_KW':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            function = value_stack[-(instr.argval + 2)]

            if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                return opname, 1

            kw = value_stack[-1]
            args = value_stack[-(instr.argval + 1):-1]
            kwargs = {k: v for k, v in zip(kw, args[::-1])}
            args = args[:-len(kw)]

            complexity = self.function_complexity_map[function.__qualname__]

            return opname, complexity(*args, **kwargs).value

        if opname == 'CALL_FUNCTION_EX':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            if instr.argval:
                kwargs = value_stack[-1]
                args = value_stack[-2]
                function = value_stack[-3]
            else:
                kwargs = {}
                args = value_stack[-1]
                function = value_stack[-2]

            if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                return opname, 1

            complexity = self.function_complexity_map[function.__qualname__]
            return opname, complexity(*args, **kwargs).value

        if opname == 'BUILD_TUPLE_UNPACK_WITH_CALL':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            function = value_stack[-(instr.argval + 1)]

            if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                return opname, 1

            t = value_stack[-instr.argval:]
            args = tuple(chain(*t))
            complexity = self.function_complexity_map[function.__qualname__]

            return opname, complexity(*args).value

        if opname == 'BUILD_MAP_UNPACK_WITH_CALL':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            function = value_stack[-(instr.argval + 2)]

            if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                return opname, 1

            m = value_stack[-instr.argval:]
            args = {}
            for _m in m:
                args.update(_m)
            complexity = self.function_complexity_map[function.__qualname__]

            return opname, complexity(**args).value

        if opname == 'CALL_METHOD':
            _, instr = get_bc_and_instr(frame)
            value_stack = value_stack_callback(frame)

            if not value_stack:
                return opname, 1

            instance = value_stack[-(instr.argval + 1)]
            method = value_stack[-(instr.argval + 2)]

            if method:
                if not hasattr(method, '__qualname__') or method.__qualname__ not in self.method_complexity_map:
                    return opname, 1

                arguments = value_stack[-instr.argval:]
                complexity = self.method_complexity_map[method.__qualname__]
                return opname, complexity(*arguments, instance=instance).value
            else:
                # 'LOAD_METHOD' can push NULL/None as instance
                function = instance

                if not hasattr(function, '__qualname__') or function.__qualname__ not in self.function_complexity_map:
                    return opname, 1

                arguments = value_stack[-instr.argval:]
                complexity = self.function_complexity_map[function.__qualname__]
                return opname, complexity(*arguments).value

        #  'BUILD_MAP_UNPACK_WITH_CALL'

        return opname, 1
