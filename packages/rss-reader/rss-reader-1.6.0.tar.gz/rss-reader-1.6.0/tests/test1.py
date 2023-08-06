from rss_reader.news import ab
import unittest


class TestNews(unittest.TestCase):
    def test_ab(self):
        result = ab(1, 2)
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
