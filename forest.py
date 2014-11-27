class NotInForest(Exception): pass


class Forest(object):
    def __init__(self):
        self.child_index = {}
        self.parent_index = {}
        self._size = 0
        self._roots = set()

    def __eq__(self, obj):
        if not isinstance(obj, self.__class__):
            return False

        # check number of nodes
        if obj.size != self.size:
            return False
        
        return (self.child_index == obj.child_index and
                self.parent_index == obj.parent_index)

    def __neq__(self, obj):
        return not self == obj

    def __contains__(self, node):
        return node in self.child_index and node in self.parent_index

    def parents(self, node):
        """
        Returns a set of all parents of a node. NotInForest raised if node not
        in forest.
        """
        try:
            return self.parent_index[node]
        except KeyError:
            raise NotInForest

    def children(self, node):
        """
        Returns a set of all children of a node. NotInForest raised if node not
        in forest.
        """
        try:
            return self.child_index[node]
        except KeyError:
            raise NotInForest

    @property
    def size(self):
        """
        Returns number of nodes.
        """
        return self._size

    def is_root(self, node):
        """
        True iff node is a root.
        """
        return node in self._roots

    @property
    def roots(self):
        """
        Returns a list of roots in the forest.
        """
        return list(self._roots)

    def empty(self):
        """
        True iff there are no nodes in the forest.
        """
        return self.size == 0

    def add_node(self, node):
        """
        Adds an orphan node to the forest. All orphan nodes are, by definition,
        roots.
        """
        if node not in self:
            self.child_index[node] = set()
            self.parent_index[node] = set()
            self._roots.add(node)
            self._size += 1

    def add_nodes(self, nodes):
        """
        Adds a list of orphan nodes to the forest. All orphan nodes are, by
        definition, roots.
        """
        for node in nodes:
            self.add_node(node)

    def add_child(self, node, child):
        """
        Adds a child to a node. If node is not already in the forest, it is
        added to the forest.
        """
        self.add_nodes([node, child])

        if self.is_root(child):
            self._roots.remove(child)

        if child not in self.child_index[node]:
            self.child_index[node] |= set([child])

        if node not in self.parent_index[child]:
            self.add_parent(child, node)

    def add_children(self, node, children):
        """
        Adds a list of children to a node. If node is not already in the
        forest, it is added to the forest.
        """
        for child in children:
            self.add_child(node, child)

    def add_parent(self, node, parent):
        """
        Adds a parent to a node. If node is not already in the forest, it is
        added to the forest.
        """
        self.add_nodes([node, parent])

        if self.is_root(node):
            self._roots.remove(node)

        if parent not in self.parent_index[node]:
            self.parent_index[node] |= set([parent])

        if node not in self.child_index[parent]:
            self.add_child(parent, node)

    def add_parents(self, node, parents):
        """
        Adds a list of parents to a node. If node is not already in the forest,
        it is added to the forest.
        """
        for parent in parents:
            self.add_parent(node, parent)

    def subtree(self, node):
        """
        Returns a subtree of the forest starting at node. If node is not in the
        tree, NotInForest is raised.
        """
        pass

    def cut(self, node):
        """
        Removes the subtree starting at node from the forest.
        """
        pass

    def __unicode__(self):
        pass

    def replace(self, old_node, new_node):
        """
        Replaces a node in the forest. All edges of the old node is inherited
        by the new one. NotInForest is raised if node is not in the tree.
        """
        if old_node not in self:
            raise NotInForest
        else:
            # copy, del, paste
            children = self.child_index[old_node]
            parents = self.parent_index[old_node]
            del self.child_index[old_node]
            del self.parent_index[old_node]
            self.child_index[new_node] = children
            self.parent_index[new_node] = parents

            if self.is_root(old_node):
                self._roots.remove(old_node)
                self._roots.add(new_node)
