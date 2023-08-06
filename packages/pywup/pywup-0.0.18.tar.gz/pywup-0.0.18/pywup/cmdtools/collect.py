#!/usr/bin/env python3

from subprocess import Popen, PIPE
from .shared import *

import numpy as np
import shlex
import math
import csv
import sys
import pdb
import re


class NewLine:
    
    def __init__(self, args):
        self.p = re.compile(args.pop_parameter())
    
    def check(self, row):
        return self.p.search(row)


class Pattern:
    
    def __init__(self, args):
        self.name = args.pop_parameter()
        self.p = re.compile(args.pop_parameter())
        self.data = None
    
    def clear(self):
        self.data = None
    
    def get_name(self):
        return self.name
    
    def get_value(self):
        if self.data is None:
            sys.stdout.write("!(" + self.name + ")")
        return self.data
    
    def value(self):
        return -1 if self.data is None else float(self.data)
    
    def check(self, row):
        m = self.p.search(row)
        if m:
            self.data = m.groups()[0]


class ListVariable:
    
    def __init__(self, args):
        self.name = args.pop_parameter()
        self.values = []
        
        while args.has_cmd():
            self.values.append(args.pop_parameter())
    
    def get_name(self):
        return self.name
    
    def get_values(self):
        return self.values


class RunVariable:
    
    def __init__(self, num):
        self.name = "RUN"
        self.values = [i for i in range(num)]
    
    def get_name(self):
        return self.name
    
    def get_values(self):
        return self.values


class ArithmeticVariable:
    
    def __init__(self, args):
        self.name = args.pop_parameter()
        
        first = float(args.pop_parameter())
        last  = float(args.pop_parameter())
        step  = float(args.pop_parameter()) if not args.has_cmd() else 1
        self.values = np.arange(first, last, step)
    
    def get_name(self):
        return self.name
    
    def get_values(self):
        return self.values


class GeometricVariable:
    
    def __init__(self, args):
        self.name = args.pop_parameter()
        
        first = float(args.pop_parameter())
        last  = float(args.pop_parameter())
        step  = float(args.pop_parameter()) if args.has_cmd() else 2.0
        
        if step == 1:
            raise RuntimeError("step cannot be equal to 1")
        
        self.values = list()
        current = first
        
        while current < last:
            self.values.append(current)
            current = current * step
    
    def get_name(self):
        return self.name
    
    def get_values(self):
        return self.values


def invoke(cmdline):
    args = shlex.split(cmdline)
    p = Popen(args, stdout=PIPE)
    
    if p.wait() != 0:
        raise RuntimeError("Command is not working")
    
    stdout, _ = p.communicate()
    return stdout.decode("utf-8").split("\n")


def perm_variables(variables, output=[], named_output=[]):
    if len(variables) == len(output):
        yield output, named_output
    
    else:
        name = variables[len(output)].get_name()
        
        for v in variables[len(output)].get_values():
            output.append(v)
            named_output.append((name, v))
            for tmp in perm_variables(variables, output):
                yield tmp
            output.pop()
            named_output.pop()


def do_collect(line_breaks, variables, cmdline, patterns, runs, filepath):
    
    if not cmdline:
        return print("Missing parameter --c")

    if len(patterns) == 0:
        return print("No pattern (--p) was given, nothing would be collected")

    if runs <= 0:
        return print("--runs must be >= 1")

    variables.append(RunVariable(runs))

    print()

    print("FilepathOut:", filepath)
    print("Runs:", runs)
    print("Variables:")
    
    for v in variables:
        vs = v.get_values()
        print("    {} ({}) : {}".format(v.get_name(), len(vs), vs))

    print()

    with open(filepath, "w") as fout:
        writer = csv.writer(fout, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow([v.get_name() for v in variables] + [p.get_name() for p in patterns])
        
        needs_dump = False
        
        for sequence, named in perm_variables(variables):
            sys.stdout.write("Running for " + ", ".join(str(i[0]) + "=\"" + str(i[1]) + "\"" for i in named) + " ...")
            sys.stdout.flush()
            
            prepared_cmd = cmdline.format(*sequence)
            
            rows = invoke(prepared_cmd)
        
            for row in rows:
                    
                doBreak = False
                
                for n in line_breaks:
                    if n.check(row):
                        doBreak = True
                
                if doBreak:
                    if needs_dump:
                        writer.writerow(sequence + [p.get_value() for p in patterns])
                        fout.flush()
                    
                    needs_dump = True
                    for p in patterns:
                        p.clear()
                
                for p in patterns:
                    p.check(row)
            
            if needs_dump or not line_breaks:
                writer.writerow(sequence + [p.get_value() for p in patterns])
                fout.flush()
                needs_dump = False
    
            print()


def main(argv):

    args = Args(argv)
    filepath = "./collect_output.csv"
    line_breaks = []
    variables = []
    patterns = []
    cmdline = None
    runs = 1

    while args.has_next():
        cmd = args.pop_cmd()
        #print("parsing ", cmd)

        if cmd == "--n":
            line_breaks.append(NewLine(args))
        
        elif cmd == "--p":
            patterns.append(Pattern(args))

        elif cmd == "--runs":
            runs = int(args.pop_parameter())

        elif cmd == "--va":
            variables.append(ArithmeticVariable(args))

        elif cmd == "--vg":
            variables.append(GeometricVariable(args))

        elif cmd == "--v":
            variables.append(ListVariable(args))

        elif cmd == "--c":
            cmdline = args.pop_parameter()

        elif cmd == "--o":
            filepath = args.pop_parameter()

    do_collect(line_breaks, variables, cmdline, patterns, runs, filepath)
