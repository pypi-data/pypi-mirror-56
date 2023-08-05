import logging
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from numpy.linalg import LinAlgError
from pandas import DataFrame
from pyPAL.tracer import Tracer

from pyPAL.complexity import ALL_CLASSES, UnderDeterminedEquation

logger = logging.getLogger(__name__)


class Estimator(ABC):
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    @property
    def calls(self):
        df = DataFrame(
            columns=[
                Columns.CALL_ID, Columns.FUNCTION_ID, Columns.FILE, Columns.FUNCTION_LINE, Columns.FUNCTION_NAME,
                Columns.ARGS_NAMES,
                Columns.ARGS_PROXY, Columns.KWARGS_NAMES, Columns.KWARGS_PROXY, Columns.VARARGS_NAMES,
                Columns.VARARGS_PROXY, Columns.VARKW_NAMES, Columns.VARKW_PROXY,
            ],
            data=self.tracer.get_call_stats()
        )

        # Remove columns if arguments are not present
        df.dropna(axis=1, how='all', inplace=True)
        logger.debug(len(df))
        return df

    @property
    def opcodes(self):
        df = DataFrame(
            columns=[Columns.CALL_ID, Columns.LINE, Columns.OPCODE_WEIGHT],
            data=self.tracer.get_opcode_stats(),
        )
        logger.debug(len(df))
        return df

    # Data transformation
    def aggregate_opcodes(self, line):
        # Sum opcode weights and map them to their respective calls.
        if line:
            opcode_sum = self.opcodes.groupby(
                [Columns.CALL_ID, Columns.LINE]
            )[Columns.OPCODE_WEIGHT].agg(OpcodeWeight=np.sum).reset_index()
        else:
            opcode_sum = self.opcodes.groupby(Columns.CALL_ID)[Columns.OPCODE_WEIGHT].agg(
                OpcodeWeight=np.sum).reset_index()

        df = pd.merge(self.calls, opcode_sum, on=Columns.CALL_ID)

        # Clean
        df.drop_duplicates(inplace=True)
        logger.debug("line={}: {}".format(line, len(df)))
        return df

    @staticmethod
    def infer_complexity(df, arg_column):
        """
        Derive the big O complexity class.

        :param df: Time series-like data.
                            x-axes: argument size
                            y-axes: executed opcodes
        :return: Best fitting complexity class
        """
        best_class = None
        best_residuals = np.inf
        fitted = {}

        for class_ in ALL_CLASSES:
            inst = class_()
            residuals = inst.fit(
                df[arg_column].values.astype(np.float),
                df[Columns.NORM_OPCODE_WEIGHT].values.astype(np.float)
            )
            fitted[inst] = residuals

            if residuals < best_residuals - 1e-6:
                best_residuals = residuals
                best_class = inst

        return best_class

    @abstractmethod
    def report(self):
        raise NotImplementedError()


# TODO: check if complexity estimations are independent from each other (not modifying their data frames)
# TODO: handle kwargs/varargs/varkw ? what to do about all other arguments ?
class ComplexityEstimator(Estimator):
    def analyze_args_separate_ascending(self, df):
        # View separate argument axes and sort argument proxy value ascending
        for column in df:
            if column == Columns.NORM_OPCODE_WEIGHT:
                continue

            # Keep influence of other arguments as low as possible by selecting rows with smallest proxy value
            args_columns = df.columns.to_list()[:-1]
            df = df.sort_values(args_columns)
            df.drop_duplicates([column, Columns.NORM_OPCODE_WEIGHT], keep='first', inplace=True)
            yield self.infer_complexity(df, column), column, df[[column, Columns.NORM_OPCODE_WEIGHT]]

    def analyze_all_args(self, df):
        # View all argument axes together and sort argument proxy value ascending
        args_df = pd.DataFrame(df[Columns.ARGS_PROXY].tolist(), index=df.index)
        args_df['mean'] = args_df.mean(axis=1)
        args_df[Columns.NORM_OPCODE_WEIGHT] = df[Columns.NORM_OPCODE_WEIGHT]

        # Take average of ArgProxy values and opcode weights
        if not args_df.empty:
            args_df = args_df.groupby('mean')[Columns.NORM_OPCODE_WEIGHT].mean().reset_index()
            args_df.sort_values('mean', inplace=True)

        return self.infer_complexity(args_df, 'mean'), args_df[['mean', Columns.NORM_OPCODE_WEIGHT]]

    @staticmethod
    def unpack_tuples(df):
        # Unpack tuples of arguments
        df.dropna(subset=[Columns.ARGS_PROXY], inplace=True)
        # FIXME: ArgsProxy tuples aren't unpacked correctly
        # print('--------START--------\n', df)
        args_df = pd.DataFrame(zip(*df[Columns.ARGS_PROXY])).transpose()
        # print('--------\n', args_df)
        args_df[Columns.NORM_OPCODE_WEIGHT] = df[Columns.NORM_OPCODE_WEIGHT]
        # print('--------\n', args_df)
        args_df.dropna(inplace=True, )
        # print(args_df, '\n--------STOP--------')
        return args_df

    @staticmethod
    def normalize_column(df):
        min = df.min()
        max = df.max()
        # Replacing is needed to infer complexity
        return df.apply(lambda x: (x - min) / (max - min)).fillna(1).replace(0, 1)

    def gen_data_points(self, data, group_by, return_columns):
        for _, df in data.groupby(group_by, sort=False):
            filename = df[Columns.FILE].values[0]
            line = df[Columns.FUNCTION_LINE].values[0]
            function = df[Columns.FUNCTION_NAME].values[0]
            arg_names = df[Columns.ARGS_NAMES].values[0]

            # Normalize opcode weights for least squares
            df[Columns.NORM_OPCODE_WEIGHT] = self.normalize_column(df[Columns.OPCODE_WEIGHT])
            df = df[return_columns]
            yield filename, line, function, arg_names, df

    def map_arg_names(self, pos, names):
        if not names:
            return ""
        if isinstance(pos, int):
            return names[pos]
        return list(map(lambda x: names[x], pos))

    def analyze_complexity(self, per_line, separate_args):
        logger.info(
            '{}(per_line={}, separate_args={})'.format(self.analyze_complexity.__name__, per_line, separate_args)
        )

        data = self.aggregate_opcodes(per_line)

        if per_line:
            iterator = self.gen_data_points(
                data,
                [Columns.FUNCTION_ID, Columns.LINE],
                [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT, Columns.LINE]
            )
        else:
            iterator = self.gen_data_points(
                data,
                [Columns.FUNCTION_ID],
                [Columns.ARGS_PROXY, Columns.NORM_OPCODE_WEIGHT]
            )

        for filename, per_line, function, arg_names, df in iterator:
            logger.debug("{}: {}".format(function, len(df)))
            if separate_args:
                args_df = self.unpack_tuples(df)

                arg = 0
                try:
                    for best, arg_pos, data_points in self.analyze_args_separate_ascending(args_df):
                        yield filename, per_line, function, self.map_arg_names(arg_pos, arg_names), best, len(
                            data_points), data_points
                except (LinAlgError, UnderDeterminedEquation) as e:
                    yield filename, per_line, function, self.map_arg_names(arg,
                                                                           arg_names), e.__class__.__name__, None, None
                finally:
                    arg += 1

            try:
                complexity, data_points = self.analyze_all_args(df)
                yield filename, per_line, function, arg_names, complexity, len(
                    data_points), data_points
            except (LinAlgError, UnderDeterminedEquation) as  e:
                yield filename, per_line, function, arg_names, e.__class__.__name__, None, None

    def export(self, line=False, separate=False):
        df = DataFrame(
            self.analyze_complexity(line, separate),
            columns=[Columns.FILE, Columns.LINE, Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY,
                     Columns.DATA_POINTS, Columns.TRACING_DATA, ]
        )

        # Reorder columns
        cols = [Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.LINE, Columns.FILE,
                Columns.DATA_POINTS, Columns.TRACING_DATA]
        df = df[cols]

        return df

    @staticmethod
    def _report_line(filename, function, line, arg_pos, best):
        # TODO: simplify
        args = ", ".join(map(lambda x: "arg_{}".format(x), arg_pos))
        if isinstance(best, LinAlgError):
            status = "complexity of line {} regarding {}:\n\tDid not converge".format(line, args)
        elif isinstance(best, UnderDeterminedEquation):
            status = "complexity of line {} regarding {}:\n\tNot enough data points".format(line, args)
        else:
            status = "complexity of line {} regarding {}:\n\t{}".format(line, args, best)

        return status

    @staticmethod
    def _report_routine(filename, function, line, arg_columns, best):
        # TODO: simplify
        args = ", ".join(map(lambda x: "arg_{}".format(x), arg_columns))
        if isinstance(best, LinAlgError):
            status = "complexity of {}({}):\n\tDid not converge".format(function, args)
        elif isinstance(best, UnderDeterminedEquation):
            status = "complexity of {}({}):\n\tNot enough data points".format(function, args)
        else:
            status = "complexity of {}({}):\n\t{}".format(function, args, best)

        return status

    def report(self, line=False):
        # TODO: output in ascending order of complexity
        pd.set_option('display.max_colwidth', -1)
        # TODO: more slices variants ? What about kwargs ?

        return
        if line:
            for filename, line, function, arg_pos, arg_names, best in self.analyze_line_complexity():
                print(self._report_line(filename, function, line, arg_pos, best))

        for filename, line, function, arg_columns, arg_names, best in self.analyze_call_complexity():
            print(self._report_routine(filename, function, line, arg_columns, best))


class PerformanceTestingAnalyzer(Estimator):
    def report(self):
        raise NotImplementedError()


class Columns(object):
    CALL_ID = 'CallID'
    MODULE = 'Module'
    FILE = 'File'
    FUNCTION_NAME = 'FunctionName'
    ARGS_PROXY = 'ArgsProxy'
    ARGS_NAMES = 'Args'
    KWARGS_PROXY = 'KwargsProxy'
    KWARGS_NAMES = 'Kwargs'
    VARARGS_PROXY = 'VarArgsProxy'
    VARARGS_NAMES = 'VarArgs'
    VARKW_PROXY = 'VarKwProxy'
    VARKW_NAMES = 'VarKw'
    LINE = 'Line'
    FUNCTION_LINE = 'FunctionLine'
    OPCODE_WEIGHT = 'OpcodeWeight'
    NORM_OPCODE_WEIGHT = 'NormOpcodeWeight'
    ARG_DEP = 'DependentArgs'
    COMPLEXITY = 'Complexity'
    DATA_POINTS = 'DataPoints'
    TRACING_DATA = 'TracingData'
    FUNCTION_ID = 'FunctionID'
