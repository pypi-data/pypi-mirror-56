import json
import os
from typing import Dict, Iterable, List, Type, BinaryIO

from sight_machine import BinaryLoggable


class BinaryLogger:
    COLUMN = b':'
    PIPE = b'|'

    def __init__(self, file_path: str):
        """
        Logs serialized instances of BinaryLoggable into a file and reads them back.
        The structure of the file is divided in two parts:
        - the log entries that are added sequentially, one after the other
        - the index, that is always at the end of the file

        A log entry has three parts:
        - the size of the next two parts, followed by a column (:)
        - the address of the previous entry of the same class, followed by a  pipe (|)
        - the serialized object

        The index is a JSON-serialized dictionary, with the class names as keys, and
        the address of the last entry of the class as value, followed by a column (:)
        and the size of the index.
        """
        # ensure that the log file always exists
        if not os.path.exists(file_path):
            with open(file_path, 'wb+') as f:
                f.write(b'')
        self.handle = open(file_path, 'rb+')

    def __del__(self):
        if self.handle:
            self.handle.close()
            self.handle = None

    def write(self, binary_log: BinaryLoggable) -> None:
        """
        Writes the serialized instance.
        """
        if isinstance(binary_log, BinaryLoggable) is False:
            return
        # retrieve the index and the address of the previous entry of the same class
        seek, size, index = self.get_index()
        klass = binary_log.__class__.__name__
        previous = -1
        if klass in index:
            previous = index[klass]
        # the address of the current entry is where the index currently begins
        index[klass] = size + seek
        # move before the index
        self.handle.seek(seek, os.SEEK_END)
        # write the new entry
        entry = self.COLUMN + str(previous).encode() + self.PIPE + binary_log.to_bytes()
        self.handle.write(str(len(entry)).encode() + entry)
        # write the index
        j_index = json.dumps(index)
        self.handle.write(j_index.encode() + self.COLUMN + str(len(j_index)).encode())

    def read(self, binary_loggable_clazz: Type[BinaryLoggable]) -> Iterable[BinaryLoggable]:
        """
        Read and iterate through instances persisted in the given file.
        """
        seek, size, index = self.get_index()
        klass = binary_loggable_clazz.__name__
        if klass not in index:
            return
        seek = index[klass]
        while seek > -1:
            self.handle.seek(seek, os.SEEK_SET)
            # get the size of the log entry
            size = self.get_size(self.handle, self.COLUMN)
            if size == 0:
                break
            log_entry = self.handle.read(size)
            sep = log_entry.find(self.PIPE)
            seek = int(log_entry[1:sep].decode())
            instance = binary_loggable_clazz()
            instance.from_bytes(bytearray(log_entry[sep + 1:]))
            yield instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_size(f: BinaryIO, separator: bytes) -> int:
        value: List = []
        char = f.read(1)
        while char and char != separator:
            value.append(char)
            char = f.read(1)
        if char:
            f.seek(-1, os.SEEK_CUR)  # go back to the last read character
            return int(b''.join(value).decode())
        return 0

    def get_index(self) -> (int, int, Dict):
        """
        The index is always at the end of the file, with all last characters after
        the column (:) being the actual size of the index
        :return:
        - the address of the beginning of the index,
        - the size of the file,
        - the index
        """
        cursor = 0
        size = 0
        self.handle.seek(cursor, os.SEEK_END)  # from the end of the file
        total = self.handle.tell()
        # retrieve the size of the index
        while not size and self.handle.tell() > 0 and -1 * cursor < total:
            self.handle.seek(cursor, os.SEEK_END)
            if self.handle.read(1) == self.COLUMN:
                cursor += 1
                size = int(self.handle.read(-1 * cursor).decode())
            cursor -= 1
        # retrieve the index
        if size > 0:
            seek = -1 * size + cursor
            self.handle.seek(seek, os.SEEK_END)
            return seek, total, json.loads(self.handle.read(size))
        return 0, total, {}
