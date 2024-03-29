import sys

# For more information, search for "VT100 terminal codes".

colors = {
    'normal'        : 0,
    'black'         : 30,
    'red'           : 31,
    'green'         : 32,
    'yellow'        : 33,
    'blue'          : 34,
    'magenta'       : 35,
    'cyan'          : 36,
    'white'         : 37 }

styles = {
    'normal'        : 0,
    'bold'          : 1,
    'reverse'       : 2 }

def write(string):
    """ Write string to standard out. """
    sys.stdout.write(string)
    sys.stdout.flush()

def write_color(string, name, style="normal"):
    """ Write a colored string to standard out. """
    write(color(string, name, style))

def color(string, name, style="normal"):
    """ Change the color of the given string. """
    prefix = '\033[%d;%dm' % (styles[style], colors[name])
    suffix = '\033[%d;%dm' % (styles["normal"], colors["normal"])
    return prefix + string + suffix

def move(x, y):
    """ Move cursor to the given coordinates. """
    write('\033[' + str(x) + ';' + str(y) + 'H')

def move_up(lines):
    """ Move cursor up the given number of lines. """
    write('\033[' + str(lines) + 'A')

def move_down(lines):
    """ Move cursor down the given number of lines. """
    write('\033[' + str(lines) + 'B')

def move_forward(chars):
    """ Move cursor forward the given number of characters. """
    write('\033[' + str(chars) + 'C')

def move_back(chars):
    """ Move cursor backward the given number of characters. """
    write('\033[' + str(chars) + 'D')

def clear():
    """ Clear the screen and home the cursor. """
    write('\033[2K' + '\r')

def clear_eol():
    """ Clear the screen to end of line. """
    write('\033[0K')

def save():
    """ Save the cursor position. """
    write('\033[s')

def restore():
    """ Restore the cursor position. """
    write('\033[u')

def conceal():
    """ Conceal the cursor. """
    write('\033[?25l')

def reveal():
    """ Reveal the cursor. """
    write('\033[?25h')
