#! /usr/bin/env python
import argparse
import sys
import os
import csv
import subprocess as sp
from sys import platform


class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def lprint(string, fullscreen=False):
    if fullscreen:
        _, terminal_width = os.popen('stty size', 'r').read().split()
        print(string.center(int(terminal_width), "="))
    else:
        print(string)


def fprint(string, fullscreen=False):
    if platform in ("linux", "linux2", "darwin"):
        lprint(string, fullscreen)
    else:
        print(string)


def color(string, color):
    return color + string + bcolors.ENDC


def run_command(arguments):
    try:
        cmd = sp.Popen(arguments, stdout=sp.PIPE, stderr=sp.STDOUT)
        cmd.communicate()
        if cmd.returncode != 0:
            raise Exception
    except Exception as e:
        sys.exit("Command {}: failed".format(" ".join(arguments)))


def parse_cg():
    """Parses the call graph from cg.txt

    Returns:
        set of tuples (e.g. {("foo", "bar")}
    """
    with open('cg.txt',) as f:
        reader = csv.reader(f)
        return {(r[0], r[1]) for r in reader}


def run_cscout():
    run_command(['csmake'])
    run_command(['cscout', '-R', 'cgraph.txt', 'make.cs'])


def parse_cscout_output():
    with open('cgraph.txt') as f:
        reader = csv.reader(f, delimiter=' ')
        clear = lambda x: x.replace('program.c:', '')
        return {(clear(r[0]), clear(r[1])) for r in reader}


def clean():
    run_command(['make', 'clean'])


def main():
    # Parse arguments
    parser = argparse.ArgumentParser('Run C Call Graphs Benchmark')
    parser.add_argument('-t', '--test-number', help='Specify specific test')
    args = parser.parse_args()
    cwd = os.getcwd()

    tests = [d for d in os.listdir('.') if os.path.isdir(d)]
    if args.test_number:
        if args.test_number not in tests:
            sys.exit("Test number {} does not exist".format(args.test_number))
        tests = [args.test_number]


    fprint(" C Benchmark Starts ", fullscreen=True)
    passed = 0
    total = len(tests)
    for test in sorted(tests, key=lambda x: int(x)):
        os.chdir(os.path.join(cwd, test))
        cg = parse_cg()
        run_cscout()
        cscout_cg = parse_cscout_output()
        clean()
        status = color("Failed", bcolors.RED)
        if cg == cscout_cg:
            status = color("Passed", bcolors.GREEN)
            passed += 1
        fprint("test_{}: {}".format(test, status))
        os.chdir(cwd)
    fprint(" {}/{} tests passed ".format(passed, total), fullscreen=True)

if __name__ == "__main__":
    main()
