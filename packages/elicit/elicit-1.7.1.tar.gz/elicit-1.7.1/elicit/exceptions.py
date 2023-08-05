#!/usr/bin/env python3.5
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common exceptions.
"""


class CLIException(Exception):
    def __init__(self, value=None):
        self.value = value


class CommandQuit(CLIException):
    """An exception that is used to signal quiting from a command object.
    """


class CommandExit(CLIException):
    """An exception that is used to signal exiting from the command object. The
    command is not popped.
    """


class NewCommand(CLIException):
    """Used to signal the parser to push a new command object.
    Raise this with an instance of BaseCommands as a value.
    """


class PageQuit(Exception):
    """Quit early from paged IO.
    """
