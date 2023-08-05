# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command parser module. Default is a simple, POSIX-like command parsing.
"""

__all__ = ['CommandParser']

import sys
import os
import readline

from . import exceptions
from . import controller
from .fsm import FSM, ANY


class CommandParser:
    """Reads an IO stream and parses input similar to POSIX shell syntax.
    Calls command methods for each line. Handles readline completer.
    """

    VARCHARS = r'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_?'
    _SPECIAL = {"r": "\r", "n": "\n", "t": "\t", "b": "\b"}

    def __init__(self, controller=None, historyfile=None):
        if historyfile:
            self._historyfile = os.path.expanduser(os.path.expandvars(str(historyfile)))
        else:
            self._historyfile = None
        if self._historyfile:
            try:
                readline.read_history_file(self._historyfile)
            except FileNotFoundError:
                pass
        self.initialize()
        self.reset(controller)

    def _rl_completer(self, text, state):
        if state == 0:
            curr = readline.get_line_buffer()
            b = readline.get_begidx()
            if b == 0:
                complist = self._controller.get_completion_scope("commands")
            else:  # complete based on scope keyed on previous word
                word = curr[:b].split()[-1]
                complist = self._controller.get_completion_scope(word)
            self._complist = [s for s in complist if s.startswith(text)]
        try:
            return self._complist[state]
        except IndexError:
            return None

    def close(self):
        self.reset()

    def __del__(self):
        if self._historyfile:
            readline.write_history_file(self._historyfile)

    def reset(self, newcontroller=None):
        self._controllers = []
        self._controller = None
        self.arg_list = []
        self._buf = ""
        if newcontroller:
            self.push_controller(newcontroller)

    def push_controller(self, newcontroller):
        lvl = int(newcontroller.environ.setdefault("SHLVL", 0))
        newcontroller.environ["SHLVL"] = lvl + 1
        self._controllers.append(newcontroller)
        self._controller = newcontroller  # current command holder
        cmdlist = newcontroller.get_command_names()
        newcontroller.add_completion_scope("commands", cmdlist)
        newcontroller.add_completion_scope("help", cmdlist)

    def pop_controller(self, returnval=None):
        cont = self._controllers.pop()
        cont.finalize()
        if self._controllers:
            self._controller = self._controllers[-1]
            if returnval is not None:
                self._controller.handle_subcommand_exit(returnval)
        else:
            raise exceptions.CommandQuit("last command object quit.")

    def parse(self, url):
        import urllib
        fo = urllib.urlopen(url)
        try:
            self.parse_file(fo)
        finally:
            fo.close()

    def parse_file(self, fo):
        data = fo.read(4096)
        while data:
            self.feed(data)
            data = fo.read(4096)

    def interact(self):
        _reset_readline()
        oc = readline.get_completer()
        readline.set_completer(self._rl_completer)
        try:
            try:
                while 1:
                    ui = self._controller._ui
                    try:
                        line = ui.user_input()
                        if not line:
                            continue
                        while self.feed(line + "\n"):
                            line = ui.more_user_input()
                    except EOFError:
                        self._controller._ui.write("\n")
                        self.pop_controller()
            except (exceptions.CommandQuit, exceptions.CommandExit):
                pass
        finally:
            readline.set_completer(oc)
            if self._historyfile:
                readline.write_history_file(self._historyfile)

    def feed(self, text):
        text = self._buf + text
        i = 0
        for c in text:
            i += 1
            try:
                self._fsm.process(c)
                while self._fsm.stack:
                    self._fsm.process(self._fsm.pop())
            except EOFError:
                self.pop_controller()
            except exceptions.CommandQuit:
                val = sys.exc_info()[1]
                self.pop_controller(val.value)
            except exceptions.NewCommand as cmdex:
                self.push_controller(controller.CommandController(cmdex.value))
        if self._fsm.current_state:  # non-zero, stuff left
            self._buf = text[i:]
        return self._fsm.current_state

    def initialize(self):
        f = FSM(0)
        f.arg = ""
        f.add_default_transition(self._error, 0)
        # normally add text to args
        f.add_transition(ANY, 0, self._addtext, 0)
        f.add_transitions(" \t", 0, self._wordbreak, 0)
        f.add_transitions(";\n", 0, self._doit, 0)
        # slashes
        f.add_transition("\\", 0, None, 1)
        f.add_transition("\\", 3, None, 6)
        f.add_transition(ANY, 1, self._slashescape, 0)
        f.add_transition(ANY, 6, self._slashescape, 3)
        # vars
        f.add_transition("$", 0, self._startvar, 7)
        f.add_transition("{", 7, self._vartext, 9)
        f.add_transitions(self.VARCHARS, 7, self._vartext, 7)
        f.add_transition(ANY, 7, self._endvar, 0)
        f.add_transition("}", 9, self._endvar, 0)
        f.add_transition(ANY, 9, self._vartext, 9)
        # vars in singlequote
        f.add_transition("$", 3, self._startvar, 8)
        f.add_transition("{", 8, self._vartext, 10)
        f.add_transitions(self.VARCHARS, 8, self._vartext, 8)
        f.add_transition(ANY, 8, self._endvar, 3)
        f.add_transition("}", 10, self._endvar, 3)
        f.add_transition(ANY, 10, self._vartext, 10)

        # single quotes quote all
        f.add_transition("'", 0, None, 2)
        f.add_transition("'", 2, self._singlequote, 0)
        f.add_transition(ANY, 2, self._addtext, 2)
        # double quotes allow embedding word breaks and such
        f.add_transition('"', 0, None, 3)
        f.add_transition('"', 3, self._doublequote, 0)
        f.add_transition(ANY, 3, self._addtext, 3)
        # single-quotes withing double quotes
        f.add_transition("'", 3, None, 5)
        f.add_transition("'", 5, self._singlequote, 3)
        f.add_transition(ANY, 5, self._addtext, 5)
        self._fsm = f

    def _startvar(self, c, fsm):
        fsm.varname = c

    def _vartext(self, c, fsm):
        fsm.varname += c

    def _endvar(self, c, fsm):
        if c == "}":
            fsm.varname += c
        else:
            fsm.push(c)
        try:
            val = self._controller.environ.expand(fsm.varname) or ""
        except:  # noqa
            ex, val, tb = sys.exc_info()
            self._controller._ui.error("Could not expand variable "
                                       "{!r}: {} ({})".format(fsm.varname, ex, val))
        else:
            if val is not None:
                fsm.arg += str(val)

    def _error(self, input_symbol, fsm):
        self._controller._ui.error('Syntax error: {}\n{!r}'.format(input_symbol, fsm.stack))
        fsm.reset()

    def _addtext(self, c, fsm):
        fsm.arg += c

    def _wordbreak(self, c, fsm):
        if fsm.arg:
            self.arg_list.append(fsm.arg)
            fsm.arg = ''

    def _slashescape(self, c, fsm):
        fsm.arg += CommandParser._SPECIAL.get(c, c)

    def _singlequote(self, c, fsm):
        self.arg_list.append(fsm.arg)
        fsm.arg = ''

    def _doublequote(self, c, fsm):
        self.arg_list.append(fsm.arg)
        fsm.arg = ''

    def _doit(self, c, fsm):
        if fsm.arg:
            self.arg_list.append(fsm.arg)
            fsm.arg = ''
        args = self.arg_list
        self.arg_list = []
        self._controller.call(args)


def _reset_readline():
    if sys.platform == "darwin":
        readline.parse_and_bind("^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set horizontal-scroll-mode on")
    readline.parse_and_bind("set page-completions on")
    readline.set_completer_delims(" ")
    readline.set_history_length(500)

# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
