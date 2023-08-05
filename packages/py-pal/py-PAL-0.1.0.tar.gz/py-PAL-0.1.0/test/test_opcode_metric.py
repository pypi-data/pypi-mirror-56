import dis
import unittest
from sys import settrace

from pyPAL.refactoring.opcode_metric import get_opcode_weight


def trace_function(frame, event, arg):
    frame.f_trace_opcodes = True

    code = frame.f_code
    if code.co_filename == '<string>':
        current_opcode = code.co_code[frame.f_lasti]
        if TestOpcodeMetric.opcode == current_opcode:
            TestOpcodeMetric.weights.append(get_opcode_weight(
                dis.opname[current_opcode], frame
            ))

    return trace_function


class TestOpcodeMetric(unittest.TestCase):
    opcode = None
    weights = []

    def setUp(self) -> None:
        settrace(trace_function)

    def tearDown(self) -> None:
        settrace(None)
        TestOpcodeMetric.opcode = None
        TestOpcodeMetric.weights = []

    def test_BUILD_TUPLE(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_TUPLE']
        exec('a=1;(a,a,a)')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_LIST(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_LIST']
        exec('[1,2,3]')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_SET(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_SET']
        exec('{1,2,3}')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_MAP(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_MAP']
        exec('a=1;{a:1,2:2,3:3}')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_CONST_KEY_MAP(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_CONST_KEY_MAP']
        exec('{1:1,2:2,3:3}')
        self.assertEqual(3, self.weights[0])

    # FIXME: how to test BUILD_STRING

    def test_BUILD_TUPLE_UNPACK(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_TUPLE_UNPACK']
        exec('(*[1,2],*[1,2,3],*[1])')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_LIST_UNPACK(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_LIST_UNPACK']
        exec('[*[1,2],*[1,2,3],*[1]]')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_SET_UNPACK(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_SET_UNPACK']
        exec('{*[1,2],*[1,2,3],*[1]}')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_MAP_UNPACK(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_MAP_UNPACK']
        exec('{**{1:1},**{2:2},**{3:3}}')
        self.assertEqual(3, self.weights[0])

    def test_BUILD_SLICE(self):
        TestOpcodeMetric.opcode = dis.opmap['BUILD_SLICE']
        exec('l=[1,2,3];l[1:2]')
        self.assertEqual(1, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3];l[1:]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3];l[:2]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3];l[:-1]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3];l[-2:]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[3:8]')
        self.assertEqual(5, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[2:6:2]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[2:6:-1]')
        self.assertEqual(0, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[4:-6:-1]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[-1:0:-1]')
        self.assertEqual(7, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[-1:1:-1]')
        self.assertEqual(6, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[-1:-1:-1]')
        self.assertEqual(0, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[::-1]')
        self.assertEqual(8, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[::2]')
        self.assertEqual(4, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[::1]')
        self.assertEqual(8, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('l=[1,2,3,4,5,6,7,8];l[:5:-1]')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        with self.assertRaises(ValueError):
            exec('l=[1,2,3,4,5,6,7,8];l[-1:0:0]')
        TestOpcodeMetric.weights = []

    def test_eval_bytecode(self):
        bc = list(dis.get_instructions('[]'))[:-1]
        _, arg = eval_bytecode(bc, bc[-1].argval, [])
        self.assertEqual(arg, [])

        bc = list(dis.get_instructions('[1]'))[:-1]
        _, arg = eval_bytecode(bc, bc[-1].argval, [])
        self.assertEqual(arg, [[1]])

        bc = list(dis.get_instructions('(1,)'))[:-1]
        _, arg = eval_bytecode(bc, bc[-1].argval, [])
        self.assertEqual(arg, [[1]])

        """
        exec('[].append(2)')
        metric_function.assert_called_once_with([2], list.append.__qualname__)
        metric_function.reset_mock()

        exec('l=[];l.append([1,2])')
        metric_function.assert_called_once_with([[1, 2]], list.append.__qualname__)
        metric_function.reset_mock()

        exec('l=[];l.extend([1,2])')
        metric_function.assert_called_once_with([[1, 2]], list.extend.__qualname__)
        metric_function.reset_mock()

        exec('l=[];l.extend({1,2})')
        metric_function.assert_called_once_with([{1, 2}], list.extend.__qualname__)
        metric_function.reset_mock()

        exec('l=[];l.extend({1:1,2:2})')
        metric_function.assert_called_once_with([{1: 1, 2: 2}], list.extend.__qualname__)
        metric_function.reset_mock()

        exec('l=[1,2];l.extend((*l,*l))')
        metric_function.assert_called_once_with([(1, 2, 1, 2)], list.extend.__qualname__)
        metric_function.reset_mock()
        """

        # TODO: more testing, especially builtin complexities

    def test_CALL_FUNCTION(self):
        TestOpcodeMetric.opcode = dis.opmap['CALL_FUNCTION']
        exec('sum([1,2,3])')
        self.assertEqual(3, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('print("test", 1,2)')
        self.assertEqual(2, self.weights[0])
        TestOpcodeMetric.weights = []

        exec('sum(range(5))')
        self.assertEqual(5, self.weights[0])
        self.assertEqual(self.weights[1], 1)
        TestOpcodeMetric.weights = []

        # TODO: more testing, especially builtin complexities


if __name__ == '__main__':
    unittest.main()
