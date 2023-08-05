import csv
import types
import os
import sys
import abc
from collections import namedtuple
from configparser import ConfigParser


class ImportMeta(type):
    def __new__(meta, clsname, bases, clsdict):
        clsobj = super().__new__(meta, clsname, bases, clsdict)

        if hasattr(clsobj, 'ext') and hasattr(clsobj, 'Loader'):
            sys.meta_path.append(clsobj(sys.path))
        return clsobj


class CustomImporter(metaclass=ImportMeta):
    def __init__(self, path):
        self._path = path

    def find_module(self, fullname, path=None):
        name = fullname.rpartition('.')[-1]
        if path is None:
            path = self._path

        for dn in path:
            filename = os.path.join(dn, name + self.ext)
            if os.path.exists(filename):
                if hasattr(self, 'doc'):
                    return self.Loader(filename, self.doc)
                else:
                    return self.Loader(filename)
        return None


class StructLoader(abc.ABC):
    def __init__(self, filename, doc=None):
        self._filename = filename
        self.doc = doc

    @abc.abstractmethod
    def load_module(self, fullname):
        pass


class StructCSVLoader(StructLoader):
    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        mod.__file__ = self._filename
        mod.__loader__ = self
        mod.__doc__ = self.doc
        headers, data = self.read_csv()
        mod.headers = headers

        rows = []
        Row = namedtuple('Row', headers)
        for row in data:
            rows.append(Row(*tuple(row)))
        mod.rows = rows
        return mod

    def read_csv(self):
        with open(self._filename, newline='') as f:
            headers = [h.strip() for h in next(f).split(',')]
            rows = csv.reader(f)
            return headers, list(rows)


class StructTextLoader(StructLoader):
    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        mod.__file__ = self._filename
        mod.__loader__ = self

        with open(self._filename, 'rt') as f:
            mod.text = f.read()
        return mod


class StructBytesLoader(StructLoader):
    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        mod.__file__ = self._filename
        mod.__loader__ = self

        with open(self._filename, 'rb') as f:
            mod.data = f.read()
        return mod


config = ConfigParser()
config.optionxform = str


class StructIniLoader(StructLoader):
    def load_module(self, fullname):

        mod = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        mod.__file__ = self._filename
        mod.__loader__ = self
        config.read(self._filename)
        mod.config = config
        return mod


class CSVImporter(CustomImporter):
    ext = '.csv'
    Loader = StructCSVLoader

    doc = """A custom csv file imported as a module
    Attributes:
    headers: returns a list of csv headers
    rows: Returns a list of rows for the csv
    __file__: Returns the path to the csv file
    """


class TextImporter(CustomImporter):
    ext = '.txt'
    Loader = StructTextLoader


class MarkDownImporter(CustomImporter):
    ext = '.md'
    Loader = StructTextLoader


class IniImporter(CustomImporter):
    ext = '.ini'
    Loader = StructIniLoader


class PNGImporter(CustomImporter):
    ext = '.png'
    Loader = StructBytesLoader


class JPGImporter(CustomImporter):
    ext = '.jpg'
    Loader = StructBytesLoader


class IconImporter(CustomImporter):
    ext = '.ico'
    Loader = StructBytesLoader


class GifImporter(CustomImporter):
    ext = '.gif'
    Loader = StructBytesLoader
