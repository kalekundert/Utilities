#!/usr/bin/env python

import re
import sys

# Providing Verification
# ======================
# Even with its very simple interface, this module could provide some useful
# verification by checking to make sure that every argument on the command line
# was returned to the calling program at some point.  This would allow the
# calling program to notice when extraneous arguments are provided and to react
# appropriately.
#
# One concern here is that flags commonly have expanded option forms.  In order
# to do meaningful verification, this would have to be considered.  One
# possibility is to treat options without values as flags.

# Remove Parser Class
# ===================
# Having a parser class may not be necessary.  For one thing, all of its
# methods are made available as normal functions anyway.  For another, the
# class itself never gets instantiated outside of this file because the
# functions are much easier to use.
#
# However, the parser does have some state.  If I were to remove the parser
# class, all that information would have to be moved into global variables.
# Since this is a simple module, that may not be a problem.  But the
# verification problem described above is complicated, and addressing it may
# require a number of new state variables.

# Strip the Command Name
# ======================
# I often find that, when I want to use the command name, I want to remove any
# directories preceding the name of the executable.  To accommodate this, I am
# planning to add a 'strip' argument to get_command().  I can't decide if the
# default should be true or false.

class Simple(object):

    def __init__(self):

        self.arguments = sys.argv[:]
        self.command = self.arguments.pop(0)

        self.flags = []
        self.options = {}
        self.positional = []

        flag_pattern = re.compile(r"-(\w+)")
        option_pattern = re.compile(r"--(\w+)(?:=(\S+))?")

        for argument in self.arguments:

            flag_match = flag_pattern.match(argument)
            option_match = option_pattern.match(argument)

            if flag_match:
                characters = [flag for flag in flag_match.groups()]
                self.flags.extend(characters)

            elif option_match:
                name, value = option_match.groups()
                self.options[name] = value

            else:
                self.positional.append(argument)

    def get_command(self):
        return self.command

    def get_flags(self):
        return self.flags

    def get_positional(self):
        return self.positional

    def has_flag(self, name):
        return name in self.flags

    def get_flag(self, name, yes=True, no=False):
        return yes if self.has_flag(name) else no

    def has_option(self, name):
        return name in self.options

    def get_option(self, name, default=None, values=None, cast=lambda x: x):
        if values is not None:
            default = values[0]

        option = self.options.get(name, default)
        value = cast(option)

        if values is not None:
            assert value in values

        return value

    def get_options(self):
        return self.options

    def get_index(self, index):
        return self.positional[index]

    def has_any(self, *names):
        for name in names:
            if self.has_flag(name): return True
            if self.has_option(name): return True
        return False

    def has_all(self, *names):
        for name in names:
            if self.has_flag(name): continue
            if self.has_option(name): continue
            return False
        return True

parser = Simple()

# The strip argument would get rid of any directories included in the command
# name.

def command(strip=True):
    return parser.get_command()

def option(name, default=None, values=None, cast=lambda x: x):
    return parser.get_option(name, default, values, cast)

def flag(name, yes=True, no=False):
    return parser.get_flag(name, yes, no)

def any(*names):
    return parser.has_any(*names)

def first():
    return parser.index(0)

def second():
    return parser.index(1)

def third():
    return parser.index(2)

if __name__ == "__main__":

    def check_arguments(command, positional, flags, options):

        import random

        # Create a randomly ordered argument list.
        arguments = [command]
        names = options.keys()

        random.shuffle(flags)
        random.shuffle(names)

        for argument in positional:
            arguments.append(argument)

        for character in flags:
            arguments.append("-%c" % character)

        for name in names:
            option = "--%s" % name
            if options[name]: option += "=%s" % options[name]
            arguments.append(option)

        sys.argv = arguments

        # Make sure all the arguments were properly extracted.
        parser = Simple()

        assert sys.argv == arguments
        assert parser.get_command() == command

        for index, argument in enumerate(positional):
            assert parser.get_index(index) == argument

        for flag in flags:
            assert parser.has_any(flag)
            assert parser.has_flag(flag)
            assert parser.get_flag(flag, yes=None) is None

        for name in options:
            assert parser.has_option(name)
            assert parser.get_option(name) == options[name]

        assert parser.has_all(*flags)
        assert parser.has_all(*options.keys())

    # Run the tests!
    check_arguments("simple",
            [], [], {}) 

    check_arguments("positional",
            ["first", "second"], [], {})

    check_arguments("flags",
            [], ['a', 'b', 'c'], {})

    check_arguments("options",
            [], [], {"first" : '1.2', "second" : "!?", "third" : None})

    print "All tests passed!"

    

