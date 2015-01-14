import unittest
import logging
logging.getLogger().setLevel(logging.DEBUG)

from .. import timeutils
import datetime

class BaseTest(unittest.TestCase):
    N = 10000

    def assertInRange(self, n, a, b):
        self.assertGreaterEqual(n, a)
        self.assertLessEqual(n, b)

class TestRandomdt(BaseTest):

    def test_construct(self):
        for i in range(self.N):
            timeutils.randomdt()

    def test_range(self):
        r = (1, 2)
        for name in ('month', 'day', 'year', 'hour', 'minute', 'second', 'microsecond'):
            for i in range(10):
                n = getattr(timeutils.randomdt(**{'{}_range'.format(name) : r}), name)
                self.assertInRange(n, *r)

    def test_explicit(self):
        v = 1
        for name in ('month', 'day', 'year', 'hour', 'minute', 'second', 'microsecond'):
            n = getattr(timeutils.randomdt(**{'{}'.format(name) : v}), name)
            self.assertEqual(n, v)

class TestConvert_str(BaseTest):

    def test_str_to_datetime(self):
        dobj = timeutils.str_to_datetime('1/2/1971 04:05:06')
        self.assertTrue(isinstance(dobj, datetime.datetime))
        self.assertEqual(dobj.month, 1)
        self.assertEqual(dobj.day, 2)
        self.assertEqual(dobj.year, 1971)
        self.assertEqual(dobj.hour, 4)
        self.assertEqual(dobj.minute, 5)
        self.assertEqual(dobj.second, 6)
        self.assertEqual(dobj.microsecond, 0)

    def test_datetime_to_str(self):
        dobj = datetime.datetime(1971, 1, 2, 4, 5, 6, 0)
        sobj = timeutils.datetime_to_str(dobj)
        self.assertTrue(isinstance(sobj, str))
        self.assertEqual(sobj, '01/02/1971 04:05:06')

class TestConvert_timestamp(BaseTest):

    def test_datetime_timestamp_conversion(self):
        for i in range(self.N):
            dobj1 = timeutils.randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            dobj2 = timeutils.timestamp_to_datetime(stmp1)
            stmp2 = timeutils.datetime_to_timestamp(dobj2)
            self.assertEqual(dobj1, dobj2)
            self.assertEqual(stmp1, stmp2)

class TestFunc_datetime(BaseTest):

    def test_str(self):
        dobj = timeutils.datetime('1/2/1903 04:05:06')
        self.assertTrue(isinstance(dobj, datetime.datetime))
        self.assertEqual(dobj.month, 1)
        self.assertEqual(dobj.day, 2)
        self.assertEqual(dobj.year, 1903)
        self.assertEqual(dobj.hour, 4)
        self.assertEqual(dobj.minute, 5)
        self.assertEqual(dobj.second, 6)
        self.assertEqual(dobj.microsecond, 0)

    def test_timestamp(self):
        for i in range(self.N):
            dobj1 = timeutils.randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            dobj2 = timeutils.datetime(stmp1)
            self.assertTrue(isinstance(dobj1, datetime.datetime))
            self.assertEqual(dobj1, dobj2)

    def test_datetime(self):
        for i in range(self.N):
            dobj1 = timeutils.randomdt()
            dobj2 = timeutils.datetime(dobj1)
            self.assertTrue(isinstance(dobj2, datetime.datetime))
            self.assertEqual(dobj1, dobj2)

    def test_args(self):
        dobj = timeutils.datetime(1900, 1, 2)
        self.assertTrue(isinstance(dobj, datetime.datetime))
        self.assertEqual(dobj.month, 1)
        self.assertEqual(dobj.day, 2)
        self.assertEqual(dobj.year, 1900)

    def test_kwargs(self):
        dobj = timeutils.datetime(1900, 1, 2, microsecond=1)
        self.assertTrue(isinstance(dobj, datetime.datetime))
        self.assertEqual(dobj.month, 1)
        self.assertEqual(dobj.day, 2)
        self.assertEqual(dobj.year, 1900)
        self.assertEqual(dobj.microsecond, 1)

class TestFunc_timestamp(BaseTest):

    def test_str(self):
        stmp1 = timeutils.timestamp('1/2/1971 04:05:06')
        self.assertTrue(isinstance(stmp1, float))
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)
        self.assertEqual(dobj1.hour, 4)
        self.assertEqual(dobj1.minute, 5)
        self.assertEqual(dobj1.second, 6)
        self.assertEqual(dobj1.microsecond, 0)

    def test_timestamp(self):
        for i in range(self.N):
            dobj1 = timeutils.randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            stmp2 = timeutils.timestamp(stmp1)
            self.assertTrue(isinstance(stmp1, float))
            self.assertEqual(stmp1, stmp2)

    def test_datetime(self):
        for i in range(self.N):
            dobj1 = timeutils.randomdt()
            stmp1 = timeutils.timestamp(dobj1)
            stmp2 = timeutils.datetime_to_timestamp(dobj1)
            self.assertTrue(isinstance(stmp1, float))
            self.assertEqual(stmp1, stmp2)

    def test_args(self):
        stmp1 = timeutils.timestamp(1971, 1, 2)
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertTrue(isinstance(dobj1, datetime.datetime))
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)

    def test_kwargs(self):
        stmp1 = timeutils.timestamp(1971, 1, 2, microsecond=1)
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertTrue(isinstance(dobj1, datetime.datetime))
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)
        self.assertEqual(dobj1.microsecond, 1)

if __name__ == '__main__':
    unittest.main()