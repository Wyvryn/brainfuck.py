# -*- coding: utf-8 -*-

import sys
import re
import getch


class Interpreter(object):

    """brainfuck.py Interpreter class

    After initializing an Interpreter object, call Interpreter.execute(x)
    to run
    """

    def __init__(self):
        self.tape = [0] * 30000
        self.head = 0
        self.loop = [[]]
        self.loopLevel = 0
        self.bracket = 0
        self.tokens = {
            '.': self.dot,
            ',': self.comma,
            '+': self.plus,
            '-': self.minus,
            '<': self.lt,
            '>': self.gt,
            '[': self.lb,
            ']': self.rb
        }

    def runLine(self, line):
        """Runs one line of brainfuck code.

        Args:
          line (iterable): An iterable containing brainfuck code to
            be executed.
        """
        for char in line:
            if self.bracket != 0 and char != '[' and char != ']':
                self.loop[self.loopLevel - 1].append(char)
            else:
                self.tokens[char]()

    def executeLoop(self):
        """Executes code in the highest level loop buffer"""
        while self.tape[self.head] != 0:
            self.runLine(self.loop[self.loopLevel - 1][1:-1])

        del self.loop[self.loopLevel - 1]
        self.runLoop = True
        self.loopLevel -= 1

    def execute(self, f):
        """Takes in a file as a string, tokenizes it, and then executes it

        Args:
          f (string): input program as a string
        """
        for line in f:
            clean = self.lex(line)
            if clean:
                self.runLine(clean)

        if self.bracket != 0:
            print "\nExpected ']' before EOF"

    def lex(self, line):
        """Tokenizs a string - removes all non valid symbols

        Args:
          line (string): string to be tokenized
        """
        return ''.join(re.findall(r'\++|\-+|\.+|\,+|\<+|\>+|\[+|\]+', line))

    def dot(self):
        """Prints the value of the current register"""
        sys.stdout.write(chr(self.tape[self.head]))

    def comma(self):
        """Sets the value of the current register to input character"""
        self.tape[self.head] = ord(getch.getch())

    def plus(self):
        """Adds 1 to the current register"""
        self.tape[self.head] += 1

    def minus(self):
        """Subtracts 1 from the current register"""
        self.tape[self.head] -= 1

    def gt(self):
        """Moves the head forward one space"""
        if self.head < len(self.tape) - 1:
            self.head += 1
        else:
            raise IndexError("\nIndex out of bounds: '>' at register %d" %
                   len(self.tape) - 1)

    def lt(self):
        """Moves the head backwards one space"""
        if self.head > 0:
            self.head -= 1
        else:
            raise IndexError("\nIndex out of bounds: '<' at register 0")

    def lb(self):
        """Signals the beginning of a loop, records all commands until
        matching ] is found.
        """
        if self.bracket == 0:
            self.loopLevel += 1
        self.bracket += 1
        self.loop.append([])
        self.loop[self.loopLevel - 1].append('[')

    def rb(self):
        """Signals the end of a loop. Executes all commands recorded
        since matching [
        """
        try:
            self.loop[self.loopLevel - 1].append(']')
            self.bracket -= 1
            if self.bracket == 0:
                self.executeLoop()

        except:
            print "\nUnexpected ']'"


if __name__ == "__main__":

    i = Interpreter()
    with open(sys.argv[1]) as f:
        i.execute(f)
