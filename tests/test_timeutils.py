import datetime
import unittest

from ffxiahbot import timeutils
from tests.cookbook import randomdt


class BaseTest(unittest.TestCase):
    N = 10000

    def assertInRange(self, n, a, b):
        self.assertGreaterEqual(n, a)
        self.assertLessEqual(n, b)


class TestCase01(BaseTest):
    def test_construct(self):
        for _i in range(self.N):
            randomdt()

    def test_range(self):
        r = (1, 2)
        for name in ("month", "day", "year", "hour", "minute", "second", "microsecond"):
            for _i in range(10):
                n = getattr(randomdt(**{f"{name}_range": r}), name)
                self.assertInRange(n, *r)

    def test_explicit(self):
        v = 1
        for name in ("month", "day", "year", "hour", "minute", "second", "microsecond"):
            n = getattr(randomdt(**{f"{name}": v}), name)
            self.assertEqual(n, v)


class TestCase02(BaseTest):
    def test_str_to_datetime(self):
        dobj = timeutils.str_to_datetime("1/2/1971 04:05:06")
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
        self.assertEqual(sobj, "01/02/1971 04:05:06")


class TestCase03(BaseTest):
    def test_datetime_timestamp_conversion(self):
        for _i in range(self.N):
            dobj1 = randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            dobj2 = timeutils.timestamp_to_datetime(stmp1)
            stmp2 = timeutils.datetime_to_timestamp(dobj2)
            self.assertEqual(dobj1, dobj2)
            self.assertEqual(stmp1, stmp2)


class TestCase04(BaseTest):
    def test_str(self):
        dobj = timeutils.datetime("1/2/1903 04:05:06")
        self.assertTrue(isinstance(dobj, datetime.datetime))
        self.assertEqual(dobj.month, 1)
        self.assertEqual(dobj.day, 2)
        self.assertEqual(dobj.year, 1903)
        self.assertEqual(dobj.hour, 4)
        self.assertEqual(dobj.minute, 5)
        self.assertEqual(dobj.second, 6)
        self.assertEqual(dobj.microsecond, 0)

    def test_timestamp(self):
        for _i in range(self.N):
            dobj1 = randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            dobj2 = timeutils.datetime(stmp1)
            self.assertTrue(isinstance(dobj1, datetime.datetime))
            self.assertEqual(dobj1, dobj2)

    def test_datetime(self):
        for _i in range(self.N):
            dobj1 = randomdt()
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


class TestCase05(BaseTest):
    def test_str(self):
        stmp1 = timeutils.timestamp("1/2/1971 04:05:06")
        self.assertTrue(isinstance(stmp1, int))
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)
        self.assertEqual(dobj1.hour, 4)
        self.assertEqual(dobj1.minute, 5)
        self.assertEqual(dobj1.second, 6)
        self.assertEqual(dobj1.microsecond, 0)

    def test_timestamp(self):
        for _i in range(self.N):
            dobj1 = randomdt(year_range=(1971, 2015))
            stmp1 = timeutils.datetime_to_timestamp(dobj1)
            stmp2 = timeutils.timestamp(stmp1)
            self.assertTrue(isinstance(stmp1, int))
            self.assertEqual(stmp1, stmp2)

    def test_datetime(self):
        for _i in range(self.N):
            dobj1 = randomdt()
            stmp1 = timeutils.timestamp(dobj1)
            stmp2 = timeutils.datetime_to_timestamp(dobj1)
            self.assertTrue(isinstance(stmp1, int))
            self.assertEqual(stmp1, stmp2)

    def test_args(self):
        stmp1 = timeutils.timestamp(1971, 1, 2, tzinfo=datetime.UTC)
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertTrue(isinstance(dobj1, datetime.datetime))
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)

    def test_kwargs(self):
        stmp1 = timeutils.timestamp(1971, 1, 2, tzinfo=datetime.UTC)
        dobj1 = timeutils.timestamp_to_datetime(stmp1)
        self.assertTrue(isinstance(dobj1, datetime.datetime))
        self.assertEqual(dobj1.month, 1)
        self.assertEqual(dobj1.day, 2)
        self.assertEqual(dobj1.year, 1971)
