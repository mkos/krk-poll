import unittest
import wios


class TestFlatten(unittest.TestCase):

    def test_flatten_not_dict(self):
        self.assertEqual({}, wios.flatten('some string'))

    def test_flatten_single_level(self):
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, wios.flatten({'a': 1, 'b': 2, 'c': 3}))

    def test_flatten_two_levels(self):
        self.assertEqual({'a': 1, 'b': 2, 'c.a': 4, 'c.b': 5}, wios.flatten({'a': 1, 'b': 2, 'c': {'a': 4, 'b': 5}}))

    def test_flatten_three_levels(self):
        self.assertEqual({'a': 1, 'b': 2, 'c.a': 4, 'c.b': 5, 'c.c.d': 6, 'c.c.e': 7},
                         wios.flatten({'a': 1, 'b': 2, 'c': {'a': 4, 'b': 5, 'c': {'d': 6, 'e': 7}}}))

    def test_flatten_one_list(self):
        self.assertEqual({'a': 1, 'b': 2, 'c': [3, 4, 5]}, wios.flatten({'a': 1, 'b': 2, 'c': [3, 4, 5]}))

    def test_flatten_one_tuple(self):
        self.assertEqual({'a': 1, 'b': 2, 'c': (3, 4, 5)}, wios.flatten({'a': 1, 'b': 2, 'c': (3, 4, 5)}))

    def test_remove_empty_sub_dict(self):
        self.assertEqual({'a': 1, 'b': 2}, wios.flatten({'a': 1, 'b': 2, 'c': {}}))

if __name__ == '__main__':
    unittest.main()
