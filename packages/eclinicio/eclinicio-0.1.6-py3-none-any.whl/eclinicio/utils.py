import os
from configparser import (ConfigParser,
                          ExtendedInterpolation, BasicInterpolation)


class PickleableFile(object):
    'Creates a pickle-compatible file-like object'

    def __init__(self, filename, mode='rb'):
        self.filename = filename
        self.mode = mode
        self.file = open(filename, mode)

    def __getstate__(self):
        state = dict(filename=self.filename, mode=self.mode, closed=self.file.closed)
        if not self.file.closed:
            state['filepos'] = self.file.tell()
        return state

    def __setstate__(self, state):
        self.filename = state['filename']
        self.mode = state['mode']
        self.file = open(self.filename, self.mode)
        if state['closed']:
            self.file.close()
        else:
            self.file.seek(state['filepos'])

    def __getattr__(self, attr):
        return getattr(self.file, attr)


class IniParser(ConfigParser):
    'Reads a .ini configuration'

    def has_option(self, option):
        for section in self.sections():
            if option in self.options(section):
                return section, True

        return None, False


def read_ini(filename, interp='basic'):
    """Read.ini config file(s) with `simple` or `extended` interpolation
    Returns: a ConfigParser object with filename read.
    """

    interpo = BasicInterpolation() if interp == 'basic' else ExtendedInterpolation()
    config = IniParser(interpolation=interpo)
    config.optionxform = str
    config.read(filename)
    return config


def get_module_path():
    'Return the dirname of the current file. If frozen returns the dir of executable'
    import os
    import sys
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def make_signature(fields):
    from inspect import Signature, Parameter

    return Signature(
        Parameter(field, Parameter.POSITIONAL_OR_KEYWORD)
        for field in fields)


def truncate_file(filename):
    'Delete file contents'
    if os.path.exists(filename):
        with open(filename, 'w'):
            return True
    return False


def CSVDictWriter(filename, headers, rows):
    "Write list of dicts to csv file"
    import csv
    with open(filename, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)
        return True
