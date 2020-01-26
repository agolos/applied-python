import argparse
import re
import sys


def output(line):
    print(line)


def grep(lines, params):
    counter = 0
    processed_lines_list = []
    res_list = []
    # line_number block
    if params.line_number:
        lines = [str(i + 1) + ':' + lines[i] for i in range(len(lines))]
    # context block
    if params.context:
        params.after_context = params.before_context = params.context
    # regular block
    params.pattern = params.pattern.replace('?', '\w')
    params.pattern = params.pattern.replace('*', '\w*')
    # ignore case block
    params.pattern = params.pattern.upper() if params.ignore_case else params.pattern
    for i in range(len(lines)):
        line_tmp = lines[i].rstrip().upper() if params.ignore_case else lines[i].rstrip()
        # invert value block
        if params.invert:
            if re.search(params.pattern, line_tmp) is None and i not in processed_lines_list:
                processed_lines_list.append(i)
                res_list.append(lines[i])
        elif re.search(params.pattern, line_tmp) is not None:
            if params.count:
                counter += 1
            elif params.before_context or params.after_context:
                start_ind, stop_ind = i - params.before_context, i + 1 + params.after_context
                for j in range(start_ind, stop_ind):
                    if (j % len(lines)) not in processed_lines_list:
                        processed_lines_list.append(j)
                        if params.line_number:
                            res_list.append(
                                lines[j % len(lines)] if i == j else lines[j % len(lines)].replace(':', '-'))
                        else:
                            res_list.append(lines[j % len(lines)])
                    elif (j % len(lines)) == i and params.line_number:
                        ''' code for strings that were defined in after or before blocks with line number param, 
                        but match with pattern'''
                        res_list[res_list.index(lines[i].replace(':', '-'))] = lines[i].replace('-', ':')
            elif i not in processed_lines_list:
                processed_lines_list.append(i)
                res_list.append(lines[i])
    for line in res_list:
        output(line)
    if counter:
        output(str(counter))


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
