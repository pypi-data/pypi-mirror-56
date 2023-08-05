# Copyright 2017-2019 Lawrence Livermore National Security, LLC and other
# Hatchet Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: MIT

import sys
from collections import defaultdict

import pandas as pd
import numpy as np

from .node import Node
from .graph import Graph
from .frame import Frame
from .external.printtree import trees_as_text
from .util.dot import trees_to_dot

lit_idx = 0
squ_idx = 0


class GraphFrame:
    """An input dataset is read into an object of this type, which includes a graph
    and a dataframe.
    """

    def __init__(self, graph, dataframe, exc_metrics=None, inc_metrics=None):
        """Create a new GraphFrame from a graph and a dataframe.

        Likely, you do not want to use this function.

        See ``from_hpctoolkit``, ``from_caliper``, ``from_caliper_json``,
        ``from_gprof_dot``, and other reader methods for easier ways to
        create a ``GraphFrame``.

        Arguments:
             graph (Graph): Graph of nodes in this GraphFrame.
             dataframe (DataFrame): Pandas DataFrame indexed by Nodes
                 from the graph, and potentially other indexes.
             exc_metrics: list of names of exclusive metrics in the dataframe.
             inc_metrics: list of names of inclusive metrics in the dataframe.
        """
        if graph is None:
            raise ValueError("GraphFrame() requires a Graph")
        if dataframe is None:
            raise ValueError("GraphFrame() requires a DataFrame")

        if "node" not in list(dataframe.index.names):
            raise ValueError(
                "DataFrames passed to GraphFrame() must have an index called 'node'."
            )

        self.graph = graph
        self.dataframe = dataframe
        self.exc_metrics = [] if exc_metrics is None else exc_metrics
        self.inc_metrics = [] if inc_metrics is None else inc_metrics

    @staticmethod
    def from_hpctoolkit(dirname):
        """Read an HPCToolkit database directory into a new GraphFrame.

        Arguments:
            dirname (str): parent directory of an HPCToolkit
                experiment.xml file

        Returns:
            (GraphFrame): new GraphFrame containing HPCToolkit profile data
        """
        # import this lazily to avoid circular dependencies
        from .readers.hpctoolkit_reader import HPCToolkitReader

        return HPCToolkitReader(dirname).read()

    @staticmethod
    def from_caliper(filename, query):
        """Read in a Caliper `cali` file.

        Args:
            filename (str): name of a Caliper output file in `.cali` format
            query (str): cali-query in CalQL format
        """
        # import this lazily to avoid circular dependencies
        from .readers.caliper_reader import CaliperReader

        return CaliperReader(filename, query).read()

    @staticmethod
    def from_caliper_json(filename_or_stream):
        """Read in a Caliper `cali-query` JSON-split file or an open file object.

        Args:
            filename_or_stream (str or file-like): name of a Caliper JSON-split
                output file, or an open file object to read one
        """
        # import this lazily to avoid circular dependencies
        from .readers.caliper_reader import CaliperReader

        return CaliperReader(filename_or_stream).read()

    @staticmethod
    def from_gprof_dot(filename):
        """Read in a DOT file generated by gprof2dot."""
        # import this lazily to avoid circular dependencies
        from .readers.gprof_dot_reader import GprofDotReader

        return GprofDotReader(filename).read()

    @staticmethod
    def from_literal(graph_dict):
        """Create a GraphFrame from a list of dictionaries.

        TODO: calculate inclusive metrics automatically.

        Example:

        .. code-block:: console

            dag_ldict = [
                {
                    "name": "A",
                    "metrics": {"time (inc)": 130.0, "time": 0.0},
                    "children": [
                        {
                            "name": "B",
                            "metrics": {"time (inc)": 20.0, "time": 5.0},
                            "children": [
                                {
                                    "name": "C",
                                    "metrics": {"time (inc)": 5.0, "time": 5.0},
                                    "children": [
                                        {
                                            "name": "D",
                                            "metrics": {"time (inc)": 8.0, "time": 1.0},
                                        }
                                    ],
                                }
                            ],
                        },
                        {
                            "name": "E",
                            "metrics": {"time (inc)": 55.0, "time": 10.0},
                            "children": [
                                {"name": "H", "metrics": {"time (inc)": 1.0, "time": 9.0}}
                            ],
                        },
                    ],
                }
            ]

        Return:
            (GraphFrame): graphframe containing data from dictionaries
        """

        def parse_node_literal(child_dict, hparent):
            """Create node_dict for one node and then call the function
            recursively on all children.
            """

            hnode = Node(Frame({"name": child_dict["name"]}), hparent)

            node_dicts.append(
                dict(
                    {"node": hnode, "name": child_dict["name"]}, **child_dict["metrics"]
                )
            )
            hparent.add_child(hnode)

            if "children" in child_dict:
                for child in child_dict["children"]:
                    parse_node_literal(child, hnode)

        list_roots = []
        node_dicts = []

        # start with creating a node_dict for each root
        for i in range(len(graph_dict)):
            graph_root = Node(Frame({"name": graph_dict[i]["name"]}), None)

            node_dict = {"node": graph_root, "name": graph_dict[i]["name"]}
            node_dict.update(**graph_dict[i]["metrics"])
            node_dicts.append(node_dict)

            list_roots.append(graph_root)

            # call recursively on all children of root
            if "children" in graph_dict[i]:
                for child in graph_dict[i]["children"]:
                    parse_node_literal(child, graph_root)

        graph = Graph(list_roots)
        graph.enumerate_traverse()

        exc_metrics = []
        inc_metrics = []
        for key in graph_dict[i]["metrics"].keys():
            if "(inc)" in key:
                inc_metrics.append(key)
            else:
                exc_metrics.append(key)

        dataframe = pd.DataFrame(data=node_dicts)
        dataframe.set_index(["node"], inplace=True)
        for i, node in enumerate(graph.traverse()):
            dataframe.loc[node]._hatchet_nid = i
        dataframe.sort_index(inplace=True)

        return GraphFrame(graph, dataframe, exc_metrics, inc_metrics)

    @staticmethod
    def from_lists(*lists):
        """Make a simple GraphFrame from lists.

        This creates a Graph from lists (see ``Graph.from_lists()``) and uses
        it as the index for a new GraphFrame. Every node in the new graph has
        exclusive time of 1 and inclusive time is computed automatically.

        """
        graph = Graph.from_lists(*lists)
        graph.enumerate_traverse()

        df = pd.DataFrame({"node": list(graph.traverse())})
        df["time"] = [1.0] * len(graph)
        df.set_index(["node"], inplace=True)

        for i, node in enumerate(graph.traverse()):
            df.loc[node]._hatchet_nid = i
        df.sort_index(inplace=True)

        gf = GraphFrame(graph, df, ["time"], [])
        gf.update_inclusive_columns()
        return gf

    def copy(self):
        """Return a shallow copy of the graphframe.

        This copies the DataFrame, but the Graph is shared between self and
        the new GraphFrame.
        """
        return GraphFrame(
            self.graph,
            self.dataframe.copy(),
            list(self.exc_metrics),
            list(self.inc_metrics),
        )

    def deepcopy(self):
        """Return a copy of the graphframe."""
        node_clone = {}
        graph_copy = self.graph.copy(node_clone)
        dataframe_copy = self.dataframe.copy()

        index_names = dataframe_copy.index.names
        dataframe_copy.reset_index(inplace=True)

        dataframe_copy["node"] = dataframe_copy["node"].apply(lambda x: node_clone[x])

        dataframe_copy.set_index(index_names, inplace=True)

        return GraphFrame(
            graph_copy, dataframe_copy, list(self.exc_metrics), list(self.inc_metrics)
        )

    def drop_index_levels(self, function=np.mean):
        """Drop all index levels but `node`."""
        index_names = list(self.dataframe.index.names)
        index_names.remove("node")

        # create dict that stores aggregation function for each column
        agg_dict = {}
        for col in self.dataframe.columns.tolist():
            if col in self.exc_metrics + self.inc_metrics:
                agg_dict[col] = function
            else:
                agg_dict[col] = lambda x: x.iloc[0]

        # perform a groupby to merge nodes that just differ in index columns
        self.dataframe.reset_index(level="node", inplace=True)
        agg_df = self.dataframe.groupby("node").agg(agg_dict)

        self.dataframe = agg_df

    def filter(self, filter_function):
        """Filter the dataframe using a user-supplied function."""
        dataframe_copy = self.dataframe.copy()

        index_names = self.dataframe.index.names
        dataframe_copy.reset_index(inplace=True)

        filtered_rows = dataframe_copy.apply(filter_function, axis=1)
        filtered_df = dataframe_copy[filtered_rows]
        filtered_df.set_index(index_names, inplace=True)

        filtered_gf = GraphFrame(self.graph, filtered_df)
        filtered_gf.exc_metrics = self.exc_metrics
        filtered_gf.inc_metrics = self.inc_metrics

        return filtered_gf

    def squash(self):
        """Rewrite the Graph to include only nodes present in the DataFrame's rows.

        This can be used to simplify the Graph, or to normalize Graph
        indexes between two GraphFrames.
        """
        index_names = self.dataframe.index.names
        self.dataframe.reset_index(inplace=True)

        # create new nodes for each unique node in the old dataframe
        old_to_new = {n: n.copy() for n in set(self.dataframe["node"])}
        for i in old_to_new:
            old_to_new[i]._hatchet_nid = i._hatchet_nid

        # Maintain sets of connections to make for each old node.
        # Start with old -> new mapping and update as we traverse subgraphs.
        connections = defaultdict(lambda: set())
        connections.update({k: {v} for k, v in old_to_new.items()})

        new_roots = []  # list of new roots

        # connect new nodes to children according to transitive
        # relationships in the old graph.
        def rewire(node, new_parent, visited):
            # make all transitive connections for the node we're visiting
            for n in connections[node]:
                if new_parent:
                    # there is a parent in the new graph; connect it
                    if n not in new_parent.children:
                        new_parent.add_child(n)
                        n.add_parent(new_parent)

                elif n not in new_roots:
                    # this is a new root
                    new_roots.append(n)

            new_node = old_to_new.get(node)
            transitive = set()
            if node not in visited:
                visited.add(node)
                for child in node.children:
                    transitive |= rewire(child, new_node or new_parent, visited)

            if new_node:
                # since new_node exists in the squashed graph, we only
                # need to connect new_node
                return {new_node}
            else:
                # connect parents to the first transitively reachable
                # new_nodes of nodes we're removing with this squash
                connections[node] |= transitive
                return connections[node]

        # run rewire for each root and make a new graph
        visited = set()
        for root in self.graph.roots:
            rewire(root, None, visited)
        graph = Graph(new_roots)
        graph.enumerate_traverse()

        # reindex new dataframe with new nodes
        df = self.dataframe.copy()
        df["node"] = df["node"].apply(lambda x: old_to_new[x])

        # at this point, the graph is potentially invalid, as some nodes
        # may have children with identical frames.
        merges = graph.normalize()
        df["node"] = df["node"].apply(lambda n: merges.get(n, n))

        df.set_index(index_names, inplace=True)
        # create dict that stores aggregation function for each column
        agg_dict = {}
        for col in df.columns.tolist():
            if col in self.exc_metrics + self.inc_metrics:
                agg_dict[col] = np.sum
            else:
                agg_dict[col] = lambda x: x.iloc[0]

        # perform a groupby to merge nodes with the same callpath
        agg_df = df.groupby(index_names).agg(agg_dict)

        for i, node in enumerate(graph.traverse()):
            df.loc[node]._hatchet_nid = i
        df.sort_index(inplace=True)

        # put it all together
        new_gf = GraphFrame(graph, agg_df, self.exc_metrics, self.inc_metrics)
        new_gf.update_inclusive_columns()
        return new_gf

    def _init_sum_columns(self, columns, out_columns):
        """Helper function for subtree_sum and subgraph_sum."""
        if out_columns is None:
            out_columns = columns
        else:
            # init out columns with input columns in case they are not there.
            for col, out in zip(columns, out_columns):
                self.dataframe[out] = self.dataframe[col]

        if len(columns) != len(out_columns):
            raise ValueError("columns out_columns must be the same length!")

        return out_columns

    def subtree_sum(self, columns, out_columns=None, function=np.sum):
        """Compute sum of elements in subtrees.  Valid only for trees.

        For each row in the graph, ``out_columns`` will contain the
        element-wise sum of all values in ``columns`` for that row's node
        and all of its descendants.

        This algorithm will multiply count nodes with in-degree higher
        than one -- i.e., it is only correct for trees.  Prefer using
        ``subgraph_sum`` (which calls ``subtree_sum`` if it can), unless
        you have a good reason not to.

        Arguments:
            columns (list of str): names of columns to sum (default: all columns)
            out_columns (list of str): names of columns to store results
                (default: in place)
            function (callable): associative operator used to sum
                elements (default: sum)

        """
        out_columns = self._init_sum_columns(columns, out_columns)

        # sum over the output columns
        for node in self.graph.traverse(order="post"):
            if node.children:
                self.dataframe.loc[node, out_columns] = function(
                    self.dataframe.loc[[node] + node.children, out_columns]
                )

    def subgraph_sum(self, columns, out_columns=None, function=np.sum):
        """Compute sum of elements in subgraphs.

        For each row in the graph, ``out_columns`` will contain the
        element-wise sum of all values in ``columns`` for that row's node
        and all of its descendants.

        This algorithm is worst-case quadratic in the size of the graph,
        so we try to call ``subtree_sum`` if we can.  In general, there
        is not a particularly efficient algorithm known for subgraph
        sums, so this does about as well as we know how.

        Arguments:
            columns (list of str):  names of columns to sum (default: all columns)
            out_columns (list of str): names of columns to store results
                (default: in place)
            function (callable): associative operator used to sum
                elements (default: sum)
        """
        if self.graph.is_tree():
            self.subtree_sum(columns, out_columns, function)
            return

        out_columns = self._init_sum_columns(columns, out_columns)
        for node in self.graph.traverse():
            subgraph_nodes = list(node.traverse())
            # TODO: need a better way of aggregating inclusive metrics when
            # TODO: there is a multi-index
            if isinstance(self.dataframe.index, pd.core.index.MultiIndex):
                for i in self.dataframe.loc[(node), out_columns].index.unique():
                    # TODO: if you take the list constructor away from the
                    # TODO: assignment below, this assignment gives NaNs. Why?
                    self.dataframe.loc[(node, i), out_columns] = list(
                        function(self.dataframe.loc[(subgraph_nodes, i), columns])
                    )
            else:
                # TODO: if you take the list constructor away from the
                # TODO: assignment below, this assignment gives NaNs. Why?
                self.dataframe.loc[(node), out_columns] = list(
                    function(self.dataframe.loc[(subgraph_nodes), columns])
                )

    def update_inclusive_columns(self):
        """Update inclusive columns (typically after operations that rewire the
        graph.
        """
        self.inc_metrics = ["%s (inc)" % s for s in self.exc_metrics]
        self.subgraph_sum(self.exc_metrics, self.inc_metrics)

    def unify(self, other):
        """Returns a unified graphframe.

        Ensure self and other have the same graph and same node IDs. This may
        change the node IDs in the dataframe.

        Update the graphs in the graphframe if they differ.
        """
        if self.graph is other.graph:
            return

        node_map = {}
        union_graph = self.graph.union(other.graph, node_map)
        union_graph.enumerate_traverse()

        self_index_names = self.dataframe.index.names
        other_index_names = other.dataframe.index.names

        self.dataframe.reset_index(inplace=True)
        other.dataframe.reset_index(inplace=True)

        self.dataframe["node"] = self.dataframe["node"].apply(lambda x: node_map[x])
        other.dataframe["node"] = other.dataframe["node"].apply(lambda x: node_map[x])

        self.dataframe.set_index(self_index_names, inplace=True, drop=True)
        other.dataframe.set_index(other_index_names, inplace=True, drop=True)

        for i, node in enumerate(union_graph.traverse()):
            self.dataframe.loc[node]._hatchet_nid = i
            other.dataframe.loc[node]._hatchet_nid = i

        self.graph = union_graph
        other.graph = union_graph

        self.dataframe.sort_index(inplace=True)
        other.dataframe.sort_index(inplace=True)

    def tree(
        self,
        metric="time",
        name="name",
        context="file",
        rank=0,
        thread=0,
        threshold=0.0,
        expand_names=False,
        unicode=True,
        color=None,
    ):
        """Format this graphframe as a tree and return the resulting string."""
        # automatic color by default; use True or False to force override
        if color is None:
            color = sys.stdout.isatty()

        result = trees_as_text(
            self.graph.roots,
            self.dataframe,
            metric,
            name,
            context,
            rank,
            thread,
            threshold,
            expand_names,
            unicode=unicode,
            color=color,
        )

        return result

    def to_dot(self, metric="time", name="name", rank=0, threshold=0.0):
        """Write the graph in the graphviz dot format:
        https://www.graphviz.org/doc/info/lang.html
        """
        return trees_to_dot(
            self.graph.roots, self.dataframe, metric, name, rank, threshold
        )

    def _operator(self, other, op, *args, **kwargs):
        """Generic function to apply operator to two dataframes and store
        result in self.

        Arguments:
            self (graphframe): self's graphframe
            other (graphframe): other's graphframe
            op (operator): pandas arithmetic operator

        Return:
            (GraphFrame): self's graphframe modified
        """
        # unioned set of self and other exclusive and inclusive metrics
        all_metrics = list(
            set().union(
                self.exc_metrics, self.inc_metrics, other.exc_metrics, other.inc_metrics
            )
        )

        self.dataframe.update(op(other.dataframe[all_metrics], *args, **kwargs))

        return self

    def add(self, other, *args, **kwargs):
        """Returns the column-wise sum of two graphframes as a new graphframe.

        This graphframe is the union of self's and other's graphs, and does not
        modify self or other.

        Return:
            (GraphFrame): new graphframe
        """
        # create a copy of both graphframes
        self_copy = self.copy()
        other_copy = other.copy()

        # unify copies of graphframes
        self_copy.unify(other_copy)

        return self_copy._operator(other_copy, self_copy.dataframe.add, *args, **kwargs)

    def sub(self, other, *args, **kwargs):
        """Returns the column-wise difference of two graphframes as a new
        graphframe.

        This graphframe is the union of self's and other's graphs, and does not
        modify self or other.

        Return:
            (GraphFrame): new graphframe
        """
        # create a copy of both graphframes
        self_copy = self.copy()
        other_copy = other.copy()

        # unify copies of graphframes
        self_copy.unify(other_copy)

        return self_copy._operator(other_copy, self_copy.dataframe.sub, *args, **kwargs)

    def __iadd__(self, other):
        """Computes column-wise sum of two graphframes and stores the result in
        self.

        Self's graphframe is the union of self's and other's graphs, and the
        node handles from self will be rewritten with this operation. This
        operation does not modify other.

        Return:
            (GraphFrame): self's graphframe modified
        """
        # create a copy of other's graphframe
        other_copy = other.copy()

        # unify self graphframe and copy of other graphframe
        self.unify(other_copy)

        return self._operator(other_copy, self.dataframe.add)

    def __add__(self, other):
        """Returns the column-wise sum of two graphframes as a new graphframe.

        This graphframe is the union of self's and other's graphs, and does not
        modify self or other.

        Return:
            (GraphFrame): new graphframe
        """
        return self.add(other)

    def __isub__(self, other):
        """Computes column-wise difference of two graphframes and stores the
        result in self.

        Self's graphframe is the union of self's and other's graphs, and the
        node handles from self will be rewritten with this operation. This
        operation does not modify other.

        Return:
            (GraphFrame): self's graphframe modified
        """
        # create a copy of other's graphframe
        other_copy = other.copy()

        # unify self graphframe and other graphframe
        self.unify(other_copy)

        return self._operator(other_copy, self.dataframe.sub)

    def __sub__(self, other):
        """Returns the column-wise difference of two graphframes as a new
        graphframe.

        This graphframe is the union of self's and other's graphs, and does not
        modify self or other.

        Return:
            (GraphFrame): new graphframe
        """
        return self.sub(other)
