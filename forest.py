class NotInForest(Exception): pass


class Forest(object):
    def __init__(self):
        self.child_index = {}
        self.parent_index = {}

    def __contains__(self, node):
        return node in self.child_index and node in self.parent_index

    def parents(self, node):
        try:
            return self.parent_index[node]
        except KeyError:
            raise NotInForest

    def children(self, node):
        try:
            return self.child_index[node]
        except KeyError:
            raise NotInForest

    @property
    def size(self):
        return len(self.child_index)

    def is_root(self, node):
        return not self.parents(node)

    def empty(self):
        return not len(self.child_index) and not len(self.parent_index)

    def add_node(self, node):
        if node not in self.child_index:
            self.child_index[node] = set()

        if node not in self.parent_index:
            self.parent_index[node] = set()

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_child(self, node, child):
        self.add_nodes([node, child])

        if child not in self.child_index[node]:
            self.child_index[node] |= set([child])

        if node not in self.parent_index[child]:
            self.add_parent(child, node)

    def add_children(self, node, children):
        for child in children:
            self.add_child(node, child)

    def add_parent(self, node, parent):
        self.add_nodes([node, parent])

        if parent not in self.parent_index[node]:
            self.parent_index[node] |= set([parent])

        if node not in self.child_index[parent]:
            self.add_child(parent, node)

    def add_parents(self, node, parents):
        for parent in parents:
            self.add_parent(node, parent)

    def tree(self, node):
        pass

    def __unicode__(self):
        pass
