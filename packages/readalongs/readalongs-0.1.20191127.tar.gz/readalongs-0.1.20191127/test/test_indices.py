from unittest import main, TestCase

from lxml import etree

from readalongs.log import LOGGER
from readalongs.text.util import compose_indices

class TestIndices(TestCase):
    def setUp(self):
        pass

    def test_i1_lower(self):
        i1 = [(1, 1), (2, 2), (3, 3), (4, 4)]
        i2 = [(1, 1), (2, 4), (3, 6), (4, 8)]
        self.assertEqual(compose_indices(i1, i2), i2)
    
    def test_i2_lower(self):
        i2 = [(1, 1), (2, 2), (3, 3), (4, 4)]
        i1 = [(1, 1), (2, 4), (3, 6), (4, 8)]
        self.assertEqual(compose_indices(i1, i2), i1)
    
    def test_equal_length(self):
        i1 = [(1, 0), (2, 1), (3, 2), (4, 4)]    # 'test'
        i2 = [(1, 1), (2, 4), (3, 6), (4, 8)]    # 'D IY S T'
        self.assertEqual(compose_indices(i1, i2), [(1, 1), (2, 4), (3, 6), (4, 8)])
    
    def test_l1_longer(self):
        i1 = [(1, 0), (2, 1), (3, 2), (4, 3), (6, 5)]
        i2 = [(1, 1), (2, 4), (4, 8), (5, 10)]
        self.assertEqual(compose_indices(i1, i2), [(1, 1), (2, 4), (4, 8), (6, 10)])

    def test_l2_longer(self):
        pass


if __name__ == '__main__':
    LOGGER.setLevel('DEBUG')
    unittest.main()
