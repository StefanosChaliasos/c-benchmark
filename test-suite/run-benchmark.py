#! /usr/bin/env python
import argparse
import sys
import os
import csv
import json
import subprocess as sp
from collections import defaultdict
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
                 '--callgrind-out-file=callgrindgraph.txt', './program'])
    run_command(['gprof2dot', '-f', 'callgrind', 
                 '-n', '0.0', '-e', '0.0', '-o', 
                 'graph.dot', 'callgrindgraph.txt'])
    run_command(['dot2fasten', '--only-current', 'program', 'graph.dot', 
                 'callgrind.json', 'test'])


def run_integrated():
    run_cscout()
    run_callgrind()
    run_command(['convert_cscout_to_stiched', 'cgraph.txt', 'stitched.json'])
    run_command(['c-integrate', 'stitched.json', 'callgrind.json', 
                 'integrate.json'])


def parse_cscout_output():
    with open('cgraph.txt') as f:
        reader = csv.reader(f, delimiter=' ')
        clear = lambda x: x.replace('program.c:', '')
        return {(clear(r[0]), clear(r[1])) for r in reader}


def parse_callgrind_output():
    with open('callgrind.json') as f:
        data = json.load(f)
        data = filter(lambda x: x[0].startswith('//test'), data)
        clear = lambda x: x.replace('()', '')[x.rfind('/')+1:]
        return {(clear(r[0]), clear(r[1])) for r in data}

def parse_integrated_output():
    with open('integrate.json') as f:
        data = json.load(f)
        clear = lambda x: x.replace('()', '')[x.rfind('/')+1:]
        return {
            (clear(data["nodes"][str(edge[0])]["URI"]), 
             clear(data["nodes"][str(edge[1])]["URI"]))
            for edge in data['edges']
        }

def clean():
    run_command(['make', 'clean'])

def read_category():
    with open('category') as f:
        category = f.readline().strip()
    return category

def print_stats(stats):
    print()
    print("Statistics")
    print("----------")
    for category, results in stats.items():
        print("{}: {} / {}".format(
            category, results['passed'], results['passed'] + results['failed']
        ))
    print()

def run_tests(tool, cwd, tests):
    commands = {
        "cscout": {
            "run": run_cscout,
            "parse": parse_cscout_output
        },
        "callgrind": {
            "run": run_callgrind,
            "parse": parse_callgrind_output
        },
        "integrated": {
            "run": run_integrated,
            "parse": parse_integrated_output
        }
    }
    stats = defaultdict(lambda: {'passed': 0, 'failed': 0, 
                                 'over-approximation': 0})
    fprint(tool + " Benchmark Starts ", fullscreen=True)
    passed = 0
    over = 0
    total = len(tests)
    for test in sorted(tests, key=lambda x: int(x.split('.')[0])):
        os.chdir(os.path.join(cwd, test))
        cg = parse_cg()
        commands[tool]['run']()
        tool_cg = commands[tool]['parse']()
        category = read_category()
        if cg == tool_cg:
            status = color("Passed", bcolors.GREEN)
            passed += 1
            stats[category]['passed'] += 1
        else:
            if cg - tool_cg:
                status = color("Failed: missing edges", bcolors.RED)
                stats[category]['failed'] += 1
            else:
                status = color("Passed: ", bcolors.GREEN)
                status += color("Over-approximation", bcolors.WARNING)
                stats[category]['passed'] += 1
                stats[category]['over-approximation'] += 1
                passed += 1
                over += 1
        clean()
        fprint("test_{}: {}".format(test, status))
        os.chdir(cwd)
    print_stats(stats)
    fprint(" {} ({}) / {} tests passed ".format(
        passed, over, total), fullscreen=True)


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
    run_tests("integrated", cwd, tests)


if __name__ == "__main__":
    main()
