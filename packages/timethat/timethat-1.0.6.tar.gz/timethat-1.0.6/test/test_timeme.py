# -*- coding: utf-8 -*-
# noinspection PyUnresolvedReferences
from .context import timethat
from timethat import TimeThat

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_a_empty(self):
        self.assertEqual(TimeThat.timedict, {})

    def test_b_talkone(self):
        TimeThat.talkone("ttt", 123.567)
        self.assertEqual(TimeThat.timedict, {})

    def test_c_start(self):
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, TimeThat.start, 13)
        self.assertRaises(ValueError, TimeThat.start, "")
        TimeThat.start("TestMe")
        self.assertGreater(TimeThat.timedict.get("TestMe", {}).get("stime"), 0)

    def test_d_stop(self):
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, TimeThat.stop, 13)
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, TimeThat.stop, "13", 13)
        self.assertRaises(ValueError, TimeThat.stop, "")
        self.assertRaises(ValueError, TimeThat.stop, "xyz")
        TimeThat.stop("TestMe")
        self.assertEqual(TimeThat.timedict.get("TestMe", {}).get("stime"), 0)
        self.assertGreater(TimeThat.timedict.get("TestMe", {}).get("cost"), 0)
        self.assertEqual(TimeThat.timedict.get("TestMe", {}).get("cnt"), 1)

    def test_e_summary(self):
        # noinspection PyTypeChecker
        self.assertRaises(TypeError, TimeThat.summary, 13)
        # noinspection PyArgumentList,PyTypeChecker
        self.assertRaises(TypeError, TimeThat.summary, [], 13)
        TimeThat.summary(reset=True)
        self.assertEqual(TimeThat.timedict, {})

    def test_f_trials(self):
        for x in range(3):
            TimeThat.start("Trial")
            TimeThat.stop("Trial")

        self.assertGreater(TimeThat.timedict.get("Trial", {}).get("cost"), 0)
        self.assertEqual(TimeThat.timedict.get("Trial", {}).get("cnt"), 3)


if __name__ == '__main__':
    unittest.main()
