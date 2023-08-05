import inspect
import pickle
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from pickle import PicklingError

from pyPAL import refactoring, call_metric, estimator
from pyPAL.refactoring import interpreter, data_handler, opcode_metric
from pyPAL.refactoring.interpreter import BytecodeInterpreter
from pyPAL.refactoring.opcode_metric import get_bc_and_instr, OpcodeMetric


class Tracer(ABC):
    def __init__(self, dh, om=OpcodeMetric(), inc=(), exc=()):
        self.opcode_metric = om
        self.data_handler = dh
        self.namespace = [
            __name__,
            refactoring.__name__,
            estimator.__name__,
            data_handler.__name__,
            interpreter.__name__,
            opcode_metric.__name__,
            call_metric.__name__,
        ]
        self.previous = None
        self.inc = inc
        self.exc = exc

    def in_scope(self, frame):
        f = frame
        while f:
            if any(map(lambda x: x.__code__ == frame.f_code, self.inc)):
                return True

            if frame.f_back == f:
                break
            f = frame.f_back

        return False

    def __call__(self, frame, event, arg):
        frame.f_trace_opcodes = True
        frame.f_trace_lines = True

        if frame.f_globals.get('__name__', '') in self.namespace:
            # Do not measure inside of tracing machinery
            return self

        if self.inc and not self.in_scope(frame):
            return self

        # call = (module, frame.f_code.co_name, args, kwargs)
        # if call in self.traced:
        #    # Stop tracing of function calls with the same argument signature
        #    return self

        # TODO: return with calculated complexity if function is already in complexity map

        if event == 'opcode':
            opname, weight = self.opcode_metric.get_value(frame, self.get_value_stack)
            self.data_handler.log_opcode(frame.f_lineno, weight)

        if event == 'call':
            args, kwargs = self.data_handler.get_proxy_args(inspect.getargvalues(frame))
            module = frame.f_globals.get('__name__', '')
            self.data_handler.log_call(module, frame.f_code.co_name, frame.f_code.co_filename, args, kwargs)

        if event == 'return':
            # call_id = self.data_handler._call_stack[-1]
            # row_filter = filter(lambda x: x[0] == call_id, self.data_handler._calls)
            # Module, function, args, kwargs
            # try:
            #    row = row_filter.__next__()
            #    self.traced.add((row[1], row[3], row[4], row[5]))
            # except StopIteration:
            #    pass
            self.data_handler.log_return()

        return self

    @abstractmethod
    def get_value_stack(self, frame):
        raise NotImplementedError()

    def trace(self):
        # Prevent multiple tracers
        self.previous = sys.gettrace()
        if not self.previous:
            sys.settrace(self)
            return self
        return self.previous

    def stop(self):
        sys.settrace(self.previous)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class CustomCPythonTracer(Tracer):
    def get_value_stack(self, frame):
        return frame.f_valuestack


class PythonTracer(Tracer):
    frame_locals = {}
    frame_globals = {}

    def _pickeable(self, value):
        try:
            pickle.dumps(value)
        except (TypeError, PicklingError):
            return False
        return True

    def __call__(self, frame, event, arg):
        # Save references to objects at beginning of each frame.
        # The bytecode interpreter needs these (E.g. iterators) in their initial state. Otherwise the result of the
        # interpreter will differ from the original evaluation stack.
        if id(frame) not in self.frame_locals:
            self.frame_locals[id(frame)] = {
                k: v if not self._pickeable(v) else deepcopy(v) for k, v in frame.f_locals.items()
            }
        if id(frame) not in self.frame_globals:
            self.frame_globals[id(frame)] = {
                k: v if not self._pickeable(v) else deepcopy(v) for k, v in frame.f_globals.items()
            }
        return super(PythonTracer, self).__call__(frame, event, arg)

    def get_value_stack(self, frame):
        # Standard CPython, no direct access
        bytecode, instr = get_bc_and_instr(frame)

        # FIXME: Performance: the interpreter only needs to be declared once every frame,
        #  every other opcode within the frame can be 'stepped through'
        bi = BytecodeInterpreter(
            bytecode,
            instr,
            self.frame_locals[id(frame)],
            self.frame_globals[id(frame)],
            frame.f_builtins
        )
        return bi.evaluation_stack()
