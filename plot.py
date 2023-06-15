#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse as dateparse
from dateutil.parser import ParserError


def load_data(path):
    with open(path, 'r', newline='') as f:
        reader = csv.reader(f)
        return list(reader)


def col(c, rows):
    return [coerce(row[c]) for row in rows]


def index(c, header):
    if c not in header:
        raise KeyError('Column {} does not exist'.format(c))

    return header.index(c)


def coerce(value):
    if isinstance(value, int) \
            or isinstance(value, float) \
            or isinstance(value, datetime):
        return value

    elif isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        try:
            return dateparse(value)
        except ParserError:
            pass

        return value

    else:
        raise ValueError('What is this? {}'.format(type(value)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--header',
                        action='store_true',
                        help='Use the first row as column headers')
    parser.add_argument('-x',
                        help='Column number starting at 1 or name if -H is \
                            given to use for the x axis. If no x is provided \
                            use the row number.')
    parser.add_argument('file',
                        help='CSV file to plot')
    parser.add_argument('column',
                        nargs='+',
                        help='Column number starting at 1 or name if -h is \
                            given to plot')

    args = parser.parse_args()

    data = load_data(args.file)

    if args.header:
        headers = data[0]
        data = data[1:]
    else:
        headers = [str(i+1) for i in range(len(data[0]))]

    if args.x:
        c = index(args.x, headers)
        x = col(c, data)
    else:
        x = range(len(data))

    columns = [
        col(index(c, headers), data) for c in args.column
    ]

    for c in args.column:
        y = col(index(c, headers), data)
        plt.plot(x, y, '.-', label=c)

    plt.title(args.file)
    if args.x:
        plt.xlabel(args.x)
    else:
        plt.xlabel('Index')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
