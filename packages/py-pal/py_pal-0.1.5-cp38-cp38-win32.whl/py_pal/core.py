from functools import wraps
from sys import gettrace

from py_pal.tracer import Tracer

opcodes_list = []
calls_list = []


def profile(function_to_trace=None, **trace_options):
    def tracing_decorator(func):
        @wraps(func)
        def tracing_wrapper(*args, **kwargs):
            if gettrace():
                return func(*args, **kwargs)

            t = Tracer(**trace_options)
            t.trace()
            try:
                return func(*args, **kwargs)
            finally:
                t.stop()
                opcodes_list.append((t.get_opcode_stats()))
                calls_list.append((t.get_call_stats()))

        return tracing_wrapper

    if function_to_trace is None:
        return tracing_decorator
    else:
        return tracing_decorator(function_to_trace)
