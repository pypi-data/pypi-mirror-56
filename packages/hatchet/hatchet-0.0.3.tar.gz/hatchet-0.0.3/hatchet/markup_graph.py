##############################################################################
# Copyright (c) 2017-2019, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Hatchet.
# Created by Abhinav Bhatele <bhatele@llnl.gov>.
# LLNL-CODE-741008. All rights reserved.
#
# For details, see: https://github.com/LLNL/hatchet
# Please also read the LICENSE file for the MIT License notice.
##############################################################################

import sys

from .external.printtree import trees_as_text
from .util.dot import trees_to_dot
from .node import Node
from .frame import Frame


class Graph:
    """A possibly multi-rooted tree or graph from one input dataset."""

    def __init__(self, roots):
        assert roots is not None
        self.roots = roots

    def traverse(self, attrs=None):
        """Preorder traversal of all roots of this Graph.

        Arguments:
            attrs (list or str, optional): If provided, extract these
                fields from nodes while traversing and yield them. See
                node.traverse() for details.

        Only preorder traversal is currently supported.
        """
        # share visisted set so that we visit each node at most once.
        visited = set()

        # iterate over roots in order
        print(self.roots)
        for root in self.roots:
            for value in root.traverse(attrs=attrs, visited=visited):
                yield value

    def copy(self, old_to_new=None):
        """Create and return a copy of this graph.

        Arguments:
            old_to_new (dict, optional): if provided, this dictionary will
                be populated with mappings from old node -> new node.
        """
        # create a mapping dict if one wasn't passed in.
        if old_to_new is None:
            old_to_new = {}

        # first pass creates new nodes
        for node in self.traverse():
            old_to_new[node] = node.copy()

        # second pass hooks up parents and children
        for old, new in old_to_new.items():
            for old_parent in old.parents:
                new.parents.append(old_to_new[old_parent])
            for old_child in old.children:
                new.children.append(old_to_new[old_child])

        return Graph([old_to_new[r] for r in self.roots])

    def union(self, other, old_to_new=None):
        """Create the union of self and other and return it as a new Graph.

        This creates a new graph and does not modify self or other. The
        new Graph has entirely new nodes.

        Arguments:
            other (Graph): another Graph
            old_to_new (dict, optional): if provided, this dictionary will
                be populated with mappings from old node -> new node

        Return:
            (Graph): a new Graph containing all nodes and all edges from
                self and other
        """
        if old_to_new is None:
            old_to_new = {}  # mapping from old nodes to new nodes

        def frame_ordered(nodes):
            """Return list of nodes sorted by frame."""
            return sorted(nodes, key=lambda n: n.frame)

        def _merge(self_children, other_children, parent):
            """Recursively merge children of self and other.

            Arguments:
                self_children (list or tuple): List of children nodes from self
                other_children (list or tuple): List of children nodes from other
                parent (Node): Parent node for self and other child(ren)

            Modifies old_to_new (dict): Updated dict mapping old nodes from self and other to new
                    unioned nodes

            Return:
                (list): list of merged children
            """
            def make_node(*nodes):
                """Make a new node to represent the union of other nodes."""
                new_node = nodes[0].copy()
                for node in nodes:
                    old_to_new[node] = new_node
                return new_node

            new_children = []

            def connect(parent, new_node):
                if parent:
                    parent.add_child(new_node)
                    new_node.add_parent(parent)
                new_children.append(new_node)

            # step through both lists and merge nodes
            self_children, other_children = iter(self_children), iter(other_children)
            self_child = next(self_children, None)
            other_child = next(other_children, None)

            while self_child and other_child:
                print(self_child, other_child)
                if self_child.frame < other_child.frame:
                    print("<", frame_ordered(self_child.children))
                    # self_child is unique
                    new_node = old_to_new.get(self_child)
                    if not new_node:
                        print("create")
                        new_node = make_node(self_child)
                        _merge(frame_ordered(self_child.children), (), new_node)
                    connect(parent, new_node)
                    self_child = next(self_children, None)

                elif self_child.frame > other_child.frame:
                    print(">", frame_ordered(other_child.children))
                    # other_child is unique
                    new_node = old_to_new.get(other_child)
                    if not new_node:
                        new_node = make_node(other_child)
                        _merge((), frame_ordered(other_child.children), new_node)
                    connect(parent, new_node)
                    other_child = next(other_children, None)

                else:
                    # self_child and other_child are equal
                    self_mapped = old_to_new.get(self_child)
                    other_mapped = old_to_new.get(other_child)
                    if not self_mapped and not other_mapped:
                        new_node = make_node(self_child, other_child)
                    else:
                        new_node = self_mapped or other_mapped

                    # map whichever node was not mapped yet
                    if not self_mapped:
                        old_to_new[self_child] = new_node
                        self_side = frame_ordered(self_child.children)
                    else:
                        self_side = []

                    if not other_mapped:
                        old_to_new[other_child] = new_node
                        other_side = frame_ordered(other_child.children)
                    else:
                        other_side = []

                    print("=", self_side, other_side)

                    ## TODO: is this always right?
                    ## TODO: what if visited in self and not other/other and not self

                    _merge(self_side, other_side, new_node)

                    connect(parent, new_node)
                    self_child = next(self_children, None)
                    other_child = next(other_children, None)

            # finish off whichever list of children is longer
            while self_child:
                print("<<", frame_ordered(self_child.children))
                new_node = old_to_new.get(self_child)
                if not new_node:
                    new_node = make_node(self_child)
                    _merge(frame_ordered(self_child.children), (), new_node)
                connect(parent, new_node)
                self_child = next(self_children, None)

            while other_child:
                print(">>", frame_ordered(other_child.children))
                new_node = old_to_new.get(self_child)
                if not new_node:
                    new_node = make_node(other_child)
                    _merge((), frame_ordered(other_child.children), new_node)
                connect(parent, new_node)
                other_child = next(other_children, None)

            print("pop")

            return new_children

        # First establish which nodes correspond to each other
        new_roots = _merge(frame_ordered(self.roots), frame_ordered(other.roots), None)

        print(len(old_to_new))

        return Graph(new_roots)

    def to_string(
        self,
        roots=None,
        dataframe=None,
        metric="time",
        name="name",
        context="file",
        rank=0,
        threshold=0.0,
        expand_names=False,
        unicode=True,
        color=True,
    ):
        """Print the graph with or without some metric attached to each node."""
        if roots is None:
            roots = self.roots

        result = trees_as_text(
            roots,
            dataframe,
            metric,
            name,
            context,
            rank,
            threshold,
            expand_names,
            unicode=unicode,
            color=color,
        )

        if sys.version_info >= (3, 0, 0):
            return result
        else:
            return result.encode("utf-8")

    def to_dot(
        self,
        roots=None,
        dataframe=None,
        metric="time",
        name="name",
        rank=0,
        threshold=0.0,
    ):
        """Write the graph in the graphviz dot format:
        https://www.graphviz.org/doc/info/lang.html
        """
        if roots is None:
            roots = self.roots

        result = trees_to_dot(roots, dataframe, metric, name, rank, threshold)

        return result

    def __str__(self):
        """Returns a string representation of the graph."""
        return self.to_string()

    def __len__(self):
        """Size of the graph in terms of number of nodes."""
        num_nodes = 0

        for root in self.roots:
            num_nodes = sum(1 for n in root.traverse())

        return num_nodes

    def __eq__(self, other):
        """Check if two graphs have the same structure by comparing frame at each
        node.
        """
        vs = set()
        vo = set()

        # if both graphs are pointing to the same object, then graphs are equal
        if self is other:
            return True

        # if number of roots do not match, then graphs are not equal
        if len(self.roots) != len(other.roots):
            return False

        if len(self) != len(other):
            return False

        # sort roots by its frame
        ssorted = sorted(self.roots, key=lambda x: x.frame)
        osorted = sorted(other.roots, key=lambda x: x.frame)

        for self_root, other_root in zip(ssorted, osorted):
            # if frames do not match, then nodes are not equal
            if self_root.frame != other_root.frame:
                return False

            if not self_root.check_dag_equal(other_root, vs, vo):
                return False

        return True

    def __ne__(self, other):
        return not (self == other)

    @staticmethod
    def from_lists(*roots):
        """Convenience method to invoke Node.from_lists() on each root value."""
        if not all(isinstance(r, (list, tuple)) for r in roots):
            raise ValueError(
                "All arguments to Graph.from_lists() must be lists: %s" % roots
            )

        return Graph([Node.from_lists(r) for r in roots])
