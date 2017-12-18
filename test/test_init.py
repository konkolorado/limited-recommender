import sys
import unittest

import src
from src.recommender import Recommender

class TestInit(unittest.TestCase):
    def setUp(self):
        self.recommender = Recommender()

    def test_running(self):
        self.assertTrue("yes")

    def test_equals(self):
        self.assertEqual(25, 50/2)

    def test_false(self):
        self.assertFalse(0)

if __name__ == '__main__':
    unittest.main()
