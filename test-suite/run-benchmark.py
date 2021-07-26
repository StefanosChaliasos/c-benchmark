#! /usr/bin/env python
import argparse
import sys
import os
import csv
import json
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


def run_callgrind():
    run_command(['make'])
    run_command(['valgrind', '--tool=callgrind', 
                 '--callgrind-out-file=cgraph.txt', './program'])
    run_command(['gprof2dot', '-f', 'callgrind', 
                 '-n', '0.0', '-e', '0.0', '-o', 
                 'graph.dot', 'cgraph.txt'])
    run_command(['dot2fasten', 'program', 'graph.dot', 'callgrind.json'])


def parse_cscout_output():
    with open('cgraph.txt') as f:
        reader = csv.reader(f, delimiter=' ')
        clear = lambda x: x.replace('program.c:', '')
        return {(clear(r[0]), clear(r[1])) for r in reader}


def parse_callgrind_output():
    with open('callgrind.json') as f:
        data = json.load(f)
        data = filter(lambda x: not x[0].startswith('//'), data)
        clear = lambda x: x.replace('()', '')[x.rfind('/')+1:]
        return {(clear(r[0]), clear(r[1])) for r in data}

def clean():
    run_command(['make', 'clean'])


def run_tests(tool, cwd, tests):
    commands = {
        "cscout": {
            "run": run_cscout,
            "parse": parse_cscout_output
        },
        "callgrind": {
            "run": run_callgrind,
            "parse": parse_callgrind_output
        }
    }
    fprint(tool + " Benchmark Starts ", fullscreen=True)
    passed = 0
    total = len(tests)
    for test in sorted(tests):
        os.chdir(os.path.join(cwd, test))
        cg = parse_cg()
        commands[tool]['run']()
        tool_cg = commands[tool]['parse']()
        clean()
        status = color("Failed", bcolors.RED)
        if cg == tool_cg:
            status = color("Passed", bcolors.GREEN)
            passed += 1
        fprint("test_{}: {}".format(test, status))
        os.chdir(cwd)
    fprint(" {}/{} tests passed ".format(passed, total), fullscreen=True)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser('Run C Call Graphs Benchmark')
    parser.add_argument('-t', '--test', help='Specify specific test')
    args = parser.parse_args()
    cwd = os.getcwd()

    tests = [d for d in os.listdir('.') if os.path.isdir(d)]
    if args.test:
        if args.test not in tests:
            sys.exit("Test {} does not exist".format(args.test))
        tests = [args.test]
    run_tests("cscout", cwd, tests)
    run_tests("callgrind", cwd, tests)


if __name__ == "__main__":
    main()
