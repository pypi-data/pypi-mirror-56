#!/usr/bin/python
"""
Packs/Unpacks `All-in-One WP Migration` packages. For more information:
https://wordpress.org/plugins/all-in-one-wp-migration/
"""

import collections
import errno
import json
import os
import six
import struct


def s__(obj):
    """
    Converts an object to str format.
    :rtype: str
    """

    if isinstance(obj, str):
        return obj
    if six.PY2:
        if isinstance(obj, unicode):
            return obj.encode('utf-8')
    elif six.PY3:
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
    return str(obj)


def b__(obj):
    """
    Converts an object to bytes format.
    :rtype: bytes
    """

    if six.PY2:
        return s__(obj)

    if isinstance(obj, bytes):
        return obj
    if not isinstance(obj, str):
        obj = str(obj)
    return obj.encode('utf-8')


class Ai1wmError(Exception):
    """ Exceptions raised from this package. """
    pass


class Ai1wmHeader(tuple):
    """ Parses an `All-in-One WP Migration` header. """

    SIZE = 4377
    EOF = b'\x00' * SIZE

    _Location = collections.namedtuple('_Location', ['offset', 'size'])
    _LOC_NAME = _Location(0, 255)       # File name
    _LOC_SIZE = _Location(255, 14)      # File size
    _LOC_TIME = _Location(269, 12)      # Last modified time
    _LOC_PATH = _Location(281, 4096)    # File path

    def __new__(cls, path=None, name=None, size=None, time=None):
        """ Returns a new instance of the object. """

        if path or name or size or time:
            if not isinstance(path, str) or path == '':
                raise ValueError('<path> must be a nonempty string')
            if not isinstance(name, str) or name == '':
                raise ValueError('<name> must be a nonempty string')
            if not isinstance(size, int) or size < 0:
                raise ValueError('<size> must be a non-negative integer')
            if not isinstance(time, int) or time < 0:
                raise ValueError('<time> must be a non-negative integer')

        return super(Ai1wmHeader, cls).__new__(cls, [path, name, size, time])

    @classmethod
    def unpack(cls, header):
        """ Unpacks a binary header. """

        if len(header) != cls.SIZE:
            raise Ai1wmError('invalid header size')

        if header == cls.EOF:
            return cls()

        return cls(
            path=s__(cls.__extract_field(header, cls._LOC_PATH)),
            name=s__(cls.__extract_field(header, cls._LOC_NAME)),
            size=cls.__extract_int(header, cls._LOC_SIZE),
            time=cls.__extract_int(header, cls._LOC_TIME),
        )

    def pack(self):
        """ Packs to a binary header. """

        attributes, formats, locations = [], '', [
            ('name', self._LOC_NAME),
            ('size', self._LOC_SIZE),
            ('time', self._LOC_TIME),
            ('path', self._LOC_PATH),
        ]

        for name, location in locations:
            attribute = b__(getattr(self, name))
            if len(attribute) > location.size:
                raise Ai1wmError('{} is too long to pack: {}'.format(name, getattr(self, name)))
            attributes.append(attribute)
            formats += '{}s'.format(location.size)

        return struct.pack(formats, *attributes)

    @property
    def path(self):
        """ Path of the file. """

        return self[0]

    @property
    def name(self):
        """ Name of the file. """

        return self[1]

    @property
    def size(self):
        """ Size of the file. """

        return self[2]

    @property
    def time(self):
        """ Time of the file. """

        return self[3]

    @property
    def eof(self):
        """ Indicates if this is an EOF header. """

        return not any(self)

    @classmethod
    def __extract_field(cls, header, location):
        """ Extracts a header field. """

        try:
            field = struct.unpack_from('{}s'.format(location.size), header, offset=location.offset)[0]
        except struct.error as e:
            raise Ai1wmError('error extracting a header field, error: {}'.format(e))

        return field.rstrip(b'\x00')

    @classmethod
    def __extract_int(cls, header, location):
        """ Extracts an integral header field. """

        try:
            return int(cls.__extract_field(header, location))
        except ValueError:
            raise Ai1wmError('invalid header field')


class Ai1wmUnpacker(object):
    """ Unpacks an `All-in-One WP Migration` package. """

    @staticmethod
    def __make_dirs(path, mode=0o777):
        """ A simple wrapper of os.makedirs(), which does not raise exception if the leaf directory already exists. """

        try:
            os.makedirs(path, mode=mode)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise Ai1wmError('error creating a directory: {}, error: {}'.format(path, e))
        return path

    @classmethod
    def __extract_file(cls, stream, path, size):
        """ Extracts a file from the input stream. """

        block_size = 0x4000

        with open(path, 'wb') as f:
            while size > 0:
                if block_size > size:
                    block_size = size
                block = stream.read(block_size)
                if len(block) != block_size:
                    raise Ai1wmError('error extracting a file: {}, error: bad file size'.format(path))
                f.write(block)
                size -= len(block)

    @classmethod
    def __unpack(cls, stream, target):
        """ Unpacks a package. """

        while True:
            header = Ai1wmHeader.unpack(stream.read(Ai1wmHeader.SIZE))
            if header.eof:
                break

            path = os.path.join(target, header.path)
            cls.__make_dirs(path)

            path = os.path.join(path, header.name)
            cls.__extract_file(stream, path, header.size)

    @classmethod
    def unpack(cls, source, target):
        """ Unpacks a package. """

        source, target = s__(os.path.realpath(source)), s__(os.path.realpath(target))
        try:
            with open(source, 'rb') as f:
                cls.__unpack(f, target)
        except Exception as ex:
            raise Ai1wmError('error unpacking a file: {}, error: {}'.format(source, ex))
        return target


class Ai1wmPacker(object):
    """ Packs an `All-in-One WP Migration` package. """

    @classmethod
    def __archive_file(cls, stream, root_dir, path, name):
        """ Archives a file to the output stream. """

        full_path = os.path.join(path, name)
        header = Ai1wmHeader(
            path=path[len(root_dir) + 1:] or '.',
            name=name,
            size=os.path.getsize(full_path),
            time=int(os.path.getmtime(full_path)),
        )
        stream.write(header.pack())

        with open(full_path, 'rb') as f:
            while True:
                block = f.read(0x4000)
                if len(block) <= 0:
                    break
                stream.write(block)

    @classmethod
    def __pack(cls, stream, source):
        """ Packs a package. """

        for path, _, files in os.walk(source):
            for name in files:
                cls.__archive_file(stream, source, path, name)
        stream.write(Ai1wmHeader.EOF)

    @classmethod
    def pack(cls, source, target):
        """ Packs a package. """

        source, target = s__(os.path.realpath(source)), s__(os.path.realpath(target))
        try:
            with open(target, 'wb') as f:
                cls.__pack(f, source)
        except Exception as ex:
            raise Ai1wmError('error packing a directory: {}, error: {}'.format(source, ex))
        return target


class Ai1wmPackage(object):
    """ An unpacked All-in-One WP Migration package. """

    DATABASE_FILE = 'database.sql'
    INFO_FILE = 'package.json'
    LOG_FILE = 'migration.log'

    def __init__(self, base_dir):
        """ Constructor. """

        self.base_dir = base_dir
        self._details = None
        self._plugins = None

    @property
    def info_file(self):
        """ Path to the migration information file. """

        return os.path.join(self.base_dir, self.INFO_FILE)

    @property
    def database_file(self):
        """ Path to the database dump file. """

        return os.path.join(self.base_dir, self.DATABASE_FILE)

    @property
    def log_file(self):
        """ Path to the migration log file. """

        return os.path.join(self.base_dir, self.LOG_FILE)

    @property
    def details(self):
        """ Details of the package. """

        if self._details is None:
            try:
                with open(self.info_file, 'r') as fp:
                    self._details = json.load(fp)
            except IOError:
                raise Ai1wmError('error reading package information file: {}'.format(self.info_file))
        return self._details

    @property
    def plugins(self):
        """ A list of active plugins. """

        if self._plugins is None:
            try:
                self._plugins = [i.split('/', 1)[0] for i in self.details['Plugins']]
            except (KeyError, TypeError, ValueError):
                raise Ai1wmError('error retrieving plugin list from package information: {}'.format(self.details))
        return self._plugins

    @property
    def stylesheet(self):
        """ The active style sheet. """

        return self.details.get('Stylesheet', None)

    @property
    def template(self):
        """ The active template. """

        return self.details.get('Template', None)

    def validate(self):
        """ Validates the package. """

        if not os.path.isfile(self.info_file):
            raise Ai1wmError('package information file is missing: {}'.format(self.info_file))
        if not os.path.isfile(self.database_file):
            raise Ai1wmError('database dump file is missing: {}'.format(self.database_file))
        return self

    def unpack_from(self, source_file):
        """ Unpacks a package. """

        if not os.path.isfile(source_file):
            raise Ai1wmError('not a file: {}'.format(source_file))
        Ai1wmUnpacker.unpack(source_file, self.base_dir)

        return self.validate()

    def pack_to(self, target_file):
        """ Packs a package. """

        return Ai1wmPacker.pack(self.validate().base_dir, target_file)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Pack/Unpack All-in-One WP Migration Packages')
    parser.add_argument('source', help='source path')
    parser.add_argument('target', help='target path')
    args = parser.parse_args()

    try:
        if os.path.isfile(args.source):
            Ai1wmPackage(args.target).unpack_from(args.source)
        elif os.path.isdir(args.source):
            Ai1wmPackage(args.source).pack_to(args.target)
    except Ai1wmError as e:
        print(e)
