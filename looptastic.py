#!/usr/bin/env python

# Looptastic.py - A library for handling FSM user input loops
# Zach Banks <zbanks@mit.edu>

import functools
import inspect
import sys

class Looptastic(object):
    def __init__(self):
        self.stopped = False
        self.state = None
        self.prompt = ">"
        self.states = dict(self._func_list())
        for name, fn in Looptastic._func_list():
            self.states.pop(name)

    @classmethod
    def _func_list(cls):
        return inspect.getmembers(cls, predicate=inspect.ismethod)

    def start(self, start_state):
        if start_state not in self.states:
            raise KeyError("No state `{}` in state table".format(start_state))
        self.state = start_state
        self.loop()

    def stop(self):
        self.stopped = True

    def write(self, text, raw=False):
        if not raw:
            text += "\n"
        sys.stdout.write(text)

    def read(self, raw=False):
        inp = sys.stdin.readline()
        if not raw:
            return inp.strip()
        return inp

    def loop(self):
        while not self.stopped:
            def get_input(prompt=">"):
                self.write(prompt, raw=True)
                inp = self.read()
                return inp
            newstate = self.states[self.state](self, get_input)
            if newstate is None:
                break
            if newstate not in self.states:
                raise KeyError("State `{}` does not exist (from state `{}`)".format(newstate, self.state))
            self.state = newstate

class Testloop(Looptastic):
    def begin(self, inp):
        if inp() == "stop":
            return "done"
        self.write("Continue")
        return "begin"

    def done(self, inp):
        self.write("Stopped")
        return None

if __name__ == "__main__":
    s = Testloop()
    s.start('begin')
