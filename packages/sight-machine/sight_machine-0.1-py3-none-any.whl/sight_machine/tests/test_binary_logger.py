import os
import unittest
from datetime import datetime, timezone
from time import monotonic
from unittest.mock import MagicMock, call

from sight_machine import BinaryLogger, BinaryLoggable


class TestBinaryLogger(unittest.TestCase):
    log_file = '/tmp/test_binary_logger.log'

    def setUp(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test___init__(self):
        # the log file does NOT exist --> it is created
        self.assertFalse(os.path.exists(self.log_file))
        tested = BinaryLogger(self.log_file)
        del tested
        self.assertTrue(os.path.exists(self.log_file))
        expected = 0
        result = os.path.getsize(self.log_file)
        self.assertEqual(expected, result)

        # the log file does exist --> it is unchanged
        with open(self.log_file, 'w') as f:
            for i in range(5):
                f.write(f'line #{i}')
        tested = BinaryLogger(self.log_file)
        del tested
        self.assertTrue(os.path.exists(self.log_file))
        expected = 35
        result = os.path.getsize(self.log_file)
        self.assertEqual(expected, result)

    def test___del__(self):
        mock = MagicMock()
        tested = BinaryLogger(self.log_file)
        tested.handle.close()
        # the file handle is correctly closed on instance destruction
        tested.handle = mock
        del tested
        expected = [
            call.__bool__(),
            call.close(),
        ]
        self.assertEqual(expected, mock.mock_calls)

    def test_write(self):
        # adding an entry that is NOT BinaryLoggable has no impact
        tested = BinaryLogger(self.log_file)
        instance = datetime(2019, 11, 28, 12, 34, 55)
        tested.write(instance)
        self.assertTrue(os.path.exists(self.log_file))
        self.assertEqual(0, os.path.getsize(self.log_file))
        del tested

        #  adding the first entry create the index too
        tested = BinaryLogger(self.log_file)
        instance = HelperBinaryLoggable1()
        instance.now = datetime(2019, 11, 28, 12, 34, 56)
        tested.write(instance)
        del tested
        with open(self.log_file, 'r') as f:
            result = f.readlines()
            expected = [
                ('32:-1|Test1+-1+2019-11-28T12:34:56'
                 '{"HelperBinaryLoggable1": 0}:28'),
            ]
            self.assertEqual(expected, result)

        #  adding an entry from a new class creates a new key in the index
        tested = BinaryLogger(self.log_file)
        instance = HelperBinaryLoggable2()
        instance.now = datetime(2019, 11, 28, 12, 34, 55)
        tested.write(instance)
        del tested
        with open(self.log_file, 'r') as f:
            result = f.readlines()
            expected = [
                ('32:-1|Test1+-1+2019-11-28T12:34:56'
                 '32:-1|Test2+-1+2019-11-28T12:34:55'
                 '{"HelperBinaryLoggable1": 0, "HelperBinaryLoggable2": 34}:57')
            ]
            self.assertEqual(expected, result)

        #  adding an entry from a known class updates the key in the index
        tested = BinaryLogger(self.log_file)
        instance = HelperBinaryLoggable2()
        instance.now = datetime(2019, 11, 28, 12, 34, 54)
        tested.write(instance)
        del tested
        with open(self.log_file, 'r') as f:
            result = f.readlines()
            expected = [
                ('32:-1|Test1+-1+2019-11-28T12:34:56'
                 '32:-1|Test2+-1+2019-11-28T12:34:55'
                 '32:34|Test2+-1+2019-11-28T12:34:54'
                 '{"HelperBinaryLoggable1": 0, "HelperBinaryLoggable2": 68}:57')
            ]
            self.assertEqual(expected, result)

    def test_read(self):
        tested = BinaryLogger(self.log_file)

        # there is NO entry of the class
        result = len([e for e in tested.read(HelperBinaryLoggable1)])
        expected = 0
        self.assertEqual(expected, result)

        # there are some entries of the class
        with open(self.log_file, 'w') as f:
            f.write('32:-1|Test1+-1+2019-11-28T12:34:56'
                    '32:-1|Test2+-1+2019-11-28T12:34:55'
                    '32:34|Test2+-1+2019-11-28T12:34:54'
                    '{"HelperBinaryLoggable1": 0, "HelperBinaryLoggable2": 68}:57')
        count = 0
        for idx, entry in enumerate(tested.read(HelperBinaryLoggable1)):
            count += 1
            self.assertIsInstance(entry, HelperBinaryLoggable1)
            self.assertEqual(datetime(2019, 11, 28, 12, 34, 56), entry.now)
        self.assertEqual(1, count)
        count = 0
        for idx, entry in enumerate(tested.read(HelperBinaryLoggable2)):
            count += 1
            self.assertIsInstance(entry, HelperBinaryLoggable2)
            self.assertEqual(datetime(2019, 11, 28, 12, 34, 54 + idx), entry.now)
        self.assertEqual(2, count)

    def test_get_size(self):
        with open(self.log_file, 'wb') as f:
            f.write(b'XYZ1234+56')
        tested = BinaryLogger(self.log_file)
        # the separator is found
        with open(self.log_file, 'rb') as f:
            f.seek(3)
            result = tested.get_size(f, b'+')
            self.assertEqual(1234, result)
            self.assertEqual(7, f.tell())
        # the separator is NOT found
        with open(self.log_file, 'rb') as f:
            f.seek(3)
            result = tested.get_size(f, b'-')
            self.assertEqual(0, result)
            self.assertEqual(10, f.tell())

    def test_get_index(self):
        tested = BinaryLogger(self.log_file)

        # empty file
        seek, size, index = tested.get_index()
        self.assertEqual(0, seek)
        self.assertEqual(0, size)
        self.assertEqual({}, index)

        # there is NO entry
        with open(self.log_file, 'w') as f:
            f.write('{}:2')

        seek, size, index = tested.get_index()
        self.assertEqual(-4, seek)
        self.assertEqual(4, size)
        self.assertEqual({}, index)

        # there are some entries
        with open(self.log_file, 'w') as f:
            f.write('This is some text'
                    'That is just to give some size'
                    '{"HelperBinaryLoggable1": 0, "HelperBinaryLoggable2": 68}:57')

        seek, size, index = tested.get_index()
        self.assertEqual(-60, seek)
        self.assertEqual(107, size)
        expected = {
            'HelperBinaryLoggable1': 0,
            'HelperBinaryLoggable2': 68,
        }
        self.assertEqual(expected, index)

    def test_performance(self):
        # check that the logger is less than 15 times slower than just keeping writing
        items = 10000
        start_time = monotonic()
        with open(self.log_file, 'wb') as f:
            for i in range(items):
                f.write(HelperBinaryLoggable1().to_bytes())
                if i % 2 == 0:
                    f.write(HelperBinaryLoggable2().to_bytes())
        base_time = monotonic() - start_time
        self.setUp()
        with BinaryLogger(self.log_file) as tested:

            start_time = monotonic()
            for i in range(items):
                instance = HelperBinaryLoggable1()
                instance.idx = i
                tested.write(instance)
                if i % 2 == 0:
                    instance = HelperBinaryLoggable2()
                    instance.idx = i
                    tested.write(instance)
            end_time = monotonic()
            self.assertGreater(base_time * 15, end_time - start_time)

            count = 0
            for entry in tested.read(HelperBinaryLoggable1):
                count += 1
                self.assertIsInstance(entry, HelperBinaryLoggable1)
                self.assertEqual(items - count, entry.idx)
            self.assertEqual(items, count)
            count = 0
            for entry in tested.read(HelperBinaryLoggable2):
                count += 1
                self.assertIsInstance(entry, HelperBinaryLoggable2)
                self.assertEqual(items - 2 * count, entry.idx)
            self.assertEqual(items, 2 * count)


class HelperBinaryLoggable(BinaryLoggable):
    def __init__(self):
        self.me = 'Test'
        self.idx = -1
        self.now = datetime.now(timezone.utc)

    def to_bytes(self) -> bytearray:
        return bytearray(self.me + '+' + str(self.idx) + '+' + self.now.isoformat(), 'utf-8')

    def from_bytes(self, byte_array: bytearray) -> None:
        splits = byte_array.decode().split('+')
        self.me = splits[0]
        self.idx = int(splits[1])
        self.now = datetime.fromisoformat(splits[2])


class HelperBinaryLoggable1(HelperBinaryLoggable):
    def __init__(self):
        super().__init__()
        self.me = 'Test1'


class HelperBinaryLoggable2(HelperBinaryLoggable):
    def __init__(self):
        super().__init__()
        self.me = 'Test2'


if __name__ == '__main__':
    unittest.main()
