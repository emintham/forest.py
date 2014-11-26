import unittest
from forest import Forest, NotInForest


class ForestTests(unittest.TestCase):
    def setUp(self):
        self.forest = Forest()

    def assert_equal_sets(self, a, b):
        self.assertEqual(set(a), set(b))

    def assert_size(self, size):
        self.assertEqual(self.forest.size, size)

    def test_empty_forest(self):
        self.assertTrue(self.forest.empty())
        self.assert_size(0)

    def test_exceptions(self):
        with self.assertRaises(NotInForest):
            self.forest.parents(0)

        with self.assertRaises(NotInForest):
            self.forest.children(1)

    def test_is_root(self):
        for node in range(5):
            self.forest.add_node(node)
        
        for node in range(5):
            self.assertTrue(self.forest.is_root(node))

    def test_contains(self):
        for i in range(5):
            self.forest.add_node(i)

        for i in range(5):
            self.assertTrue(i in self.forest)
        
    def test_add_node(self):
        self.forest.add_node(0)
        self.assertEqual(self.forest.size, 1)

    def test_add_children(self):
        self.forest.add_node(0)
        self.forest.add_children(0, [1, 2])
        self.assert_size(3)
        self.assert_equal_sets(self.forest.children(0), [1, 2])

    def test_add_children_to_existing_parent(self):
        self.forest.add_node(0)
        self.forest.add_children(0, [1, 2, 3])
        self.forest.add_children(0, [4, 5])
        self.assert_size(6)
        self.assert_equal_sets(self.forest.children(0), [1, 2, 3, 4, 5])

    def test_add_preexisting_children(self):
        self.forest.add_children(0, [1, 2])
        self.forest.add_children(0, [1, 2, 3])
        self.assert_size(4)
        self.assert_equal_sets(self.forest.children(0), [1, 2, 3])

    def test_add_grandchildren(self):
        self.forest.add_children(0, [1, 2])
        self.forest.add_children(1, [3, 4, 5])
        self.forest.add_children(2, [6, 7, 5])
        self.assert_size(8)
        self.assert_equal_sets(self.forest.children(0), [1, 2])
        self.assert_equal_sets(self.forest.children(1), [3, 4, 5])
        self.assert_equal_sets(self.forest.children(2), [6, 7, 5])

    def test_add_parent(self):
        self.forest.add_node(0)
        self.forest.add_parent(0, 1)
        self.assert_size(2)
        self.assert_equal_sets(self.forest.parents(0), [1])

    def test_add_parent_to_existing_child(self):
        self.forest.add_child(0, 1)
        self.forest.add_parent(1, 2)
        self.assert_size(3)
        self.assert_equal_sets(self.forest.parents(1), [0, 2])

    def test_add_preexisting_parent(self):
        self.forest.add_parents(0, [1, 2, 3])
        self.forest.add_parents(0, [2, 3, 4])
        self.assert_size(5)
        self.assert_equal_sets(self.forest.parents(0), [1, 2, 3, 4])

    def test_add_grandparent(self):
        self.forest.add_parent(0, 1)
        self.forest.add_parent(1, 2)
        self.assert_size(3)
        self.assert_equal_sets(self.forest.parents(0), [1])
        self.assert_equal_sets(self.forest.parents(1), [2])
