import unittest
from forest import Forest, NotInForest


class ForestTests(unittest.TestCase):
    def setUp(self):
        self.forest = Forest()

    def assert_equal_sets(self, a, b):
        self.assertEqual(set(a), set(b))

    def assert_size(self, size):
        self.assertEqual(self.forest.size, size)

    def make_x_tree(self):
        f = Forest()
        f.add_children(0, [1, 2])
        f.add_parents(0, [3, 4])
        return f

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

    def test_roots(self):
        self.forest.add_children(0, [1, 2])
        self.forest.add_children(3, [4, 5])
        self.forest.add_children(6, [5, 1])
        self.assert_equal_sets(self.forest.roots, [0, 3, 6])

    def test_roots_with_intersected_tree(self):
        pass

    def test_eq(self):
        self.forest.add_children(3, [4, 5])
        self.forest.add_children(4, [6, 7])
        self.forest.add_children(5, [8 ,9])
        self.assert_size(7)
        other_forest = Forest()
        other_forest.add_children(3, [4, 5])
        other_forest.add_children(4, [6, 7])
        other_forest.add_children(5, [8 ,9])
        self.assertEqual(other_forest.size, self.forest.size)
        self.assertEqual(other_forest, self.forest)

    def test_neq(self):
        self.forest.add_children(3, [4, 5])
        self.forest.add_children(4, [6, 7])
        self.forest.add_children(5, [8 ,9])
        self.assert_size(7)
        other_forest = Forest()
        self.assertEqual(other_forest.size, 0)
        self.assertNotEqual(other_forest, self.forest)

    def test_replace(self):
        self.forest = self.make_x_tree()
        self.assert_size(5)
        self.forest.replace(0, 5)
        self.assert_size(5)
        self.assertTrue(5 in self.forest)
        self.assert_equal_sets(self.forest.children(5), [1, 2])
        self.assert_equal_sets(self.forest.parents(5), [3, 4])
        self.assertFalse(0 in self.forest)

    def test_replace_nonexistent_raises_error(self):
        with self.assertRaises(NotInForest):
            self.forest.replace(0, 1)

    def test_subtree_leaf(self):
        self.forest.add_children(0, [1, 2, 3])
        expected = Forest().add_node(1)

        leaf = self.forest.subtree(1)

        self.assert_size(4)
        self.assertEqual(leaf.size, 1)
        self.assertEqual(leaf, expected)

    def test_subtree_tree(self):
        self.forest = self.make_x_tree()
        expected = Forest().add_children(0, [1, 2])

        tree = self.forest.subtree(0)

        self.assert_size(5)
        self.assertEqual(tree.size, 3)
        self.assertEqual(tree, expected)

    def test_subtree_with_loop(self):
        self.forest = self.make_x_tree()
        self.forest.add_parents(5, [1, 2])
        self.forest.add_child(5, 6)
        expected = self.make_x_tree()
        expected.add_child(5, 6)

        tree = self.forest.subtree(0)

        self.assert_size(7)
        self.assertEqual(tree.size, 5)
        self.assertEqual(tree, expected)

    def test_bfs(self):
        pass
