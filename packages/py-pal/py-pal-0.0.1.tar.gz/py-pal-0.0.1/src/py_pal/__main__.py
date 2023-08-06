import argparse
import inspect
import logging
import os
import sys

import matplotlib.pyplot as plt

from py_pal.complexity import Complexity
from py_pal.estimator import ComplexityEstimator, Columns
from py_pal.tracer import Tracer


def check_positive(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return int_value


def main():
    assert sys.version_info >= (3, 7)

    parser = argparse.ArgumentParser(description='Profile')
    parser.add_argument('-f', '--function', type=str, help='specify a function')
    parser.add_argument('-l', '--line', help='Calculate complexity for each line', action='store_true')
    parser.add_argument('-v', '--visualize', help='Plot runtime graphs', action='store_true')
    parser.add_argument('-s', '--separate', help='Estimate function complexity for each argument', action='store_true')
    parser.add_argument('-o', '--out', type=str, help='Output directory', default='stats')
    parser.add_argument('--save', help='Save statistics', action='store_true')
    parser.add_argument('--debug', help='Log debug output', action='store_true')
    parser.add_argument('--format', type=str, help='Output format, possible types are: csv, html, excel, json',
                        default='csv')
    parser.add_argument('target', type=str, help='a Python file or import path')

    args, unknown = parser.parse_known_args()
    print(args, unknown, sys.argv)

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='[%(levelname)s, %(module)s, %(funcName)s]: %(message)s'
    )
    logger = logging.getLogger(__name__)

    function = None
    if args.function:
        function = getattr(__import__(args.target, fromlist=[args.function]), args.function)
        sys.argv = [inspect.getfile(function), *unknown]

    file = None
    try:
        file = open(args.target).read()
    except FileNotFoundError:
        pass

    if not function and not file:
        raise ValueError("File or function could not be loaded")

    # TODO: Test cases: simple examples, sorting algorithms, games(pygame, term2048, mario, ...)
    # TODO: Output: function, parameter_name+nummer, complexity, line, module(filename), amount_data_points

    tracer = Tracer()

    if file:
        code = compile(file, filename=args.target, mode='exec')
        g = globals()

        # Execute as direct call e.g. 'python example.py'
        g['__name__'] = '__main__'

        # Append path to enable module import resolution in client code
        sys.path.append(os.path.dirname(args.target))

        # Pass arguments
        sys.argv = [args.target, *unknown]

        tracer.trace()
        exec(code, g, g)
        tracer.stop()

    if function:
        tracer.trace()
        function()
        tracer.stop()

    estimator = ComplexityEstimator(tracer)
    res = estimator.export(line=args.line, separate=args.separate)

    logger.debug(res[
                     [
                         Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.LINE, Columns.FILE,
                         Columns.DATA_POINTS
                     ]
                 ].dropna().sort_values(by=[Columns.COMPLEXITY]).to_string())
    logger.info(
        res[
            [
                Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.LINE, Columns.FILE,
                Columns.DATA_POINTS
            ]
        ].to_string())

    # pd.options.display.max_colwidth = 100

    if not args.save and args.visualize:
        res = res[[isinstance(x, Complexity) for x in res[Columns.COMPLEXITY]]]

        for index, df in res.iterrows():
            plt = plot_data_points(df)
            plt.show()

    if args.save:
        if not os.path.isdir(args.out):
            os.mkdir(args.out)

        filename = os.path.basename(args.target)

        if args.format == 'csv':
            res.to_csv("{}\\{}.csv".format(args.out, filename))
        if args.format == 'html':
            res.to_html("{}\\{}.html".format(args.out, filename))
        if args.format == 'excel':
            res.to_excel("{}\\{}.excel".format(args.out, filename))
        if args.format == 'json':
            res.to_json("{}\\{}.json".format(args.out, filename))
        if args.visualize:
            res = res[[isinstance(x, Complexity) for x in res[Columns.COMPLEXITY]]]

            for index, df in res.iterrows():
                plt = plot_data_points(df)
                plt.savefig('{}\\{}_{}.png'.format(args.out, df[Columns.FUNCTION_NAME], df[Columns.ARG_DEP]))


def plot_data_points(df):
    tracing_data = df[Columns.TRACING_DATA]
    ax = plt.gca()
    x = tracing_data.columns[0]
    tracing_data.plot(
        x=x,
        y=Columns.NORM_OPCODE_WEIGHT,
        kind='scatter',
        title="Function: {}, Args: {}".format(df[Columns.FUNCTION_NAME], df[Columns.ARG_DEP]),
        ax=ax
    )
    x_values = tracing_data[x].to_numpy()
    ax.plot(
        x_values,
        df[Columns.COMPLEXITY].compute(x_values),
        color='red'
    )
    return plt


if __name__ == "__main__":
    main()
