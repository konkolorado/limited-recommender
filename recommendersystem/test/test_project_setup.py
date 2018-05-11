import unittest

from RecommenderSystem.recommendersystem.recommender import Recommender


class TestInit(unittest.TestCase):
    def setUp(self):
        self.recommender = Recommender()

    def test_running(self):
        self.assertTrue("yes")

    def test_instance(self):
        self.assertTrue(isinstance(self.recommender, Recommender))


if __name__ == '__main__':
    unittest.main()
