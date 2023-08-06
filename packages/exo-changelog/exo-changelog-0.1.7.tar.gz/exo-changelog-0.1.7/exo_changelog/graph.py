from __future__ import unicode_literals

import sys
import warnings
from collections import deque

from six import python_2_unicode_compatible

from django.db.migrations.state import ProjectState
from django.utils import six
from django.utils.datastructures import OrderedSet
from django.db.migrations.graph import Node

from .exceptions import CircularDependencyError, NodeNotFoundError

RECURSION_DEPTH_WARNING = (
    'Maximum recursion depth exceeded while generating changes graph, '
)


class DummyNode(Node):
    def __init__(self, key, origin, error_message):
        super(DummyNode, self).__init__(key)
        self.origin = origin
        self.error_message = error_message

    def __repr__(self):
        return '<DummyNode: (%r, %r)>' % self.key

    def promote(self):
        """
        Transition dummy to a normal node and clean off excess attribs.
        Creating a Node object from scratch would be too much of a
        hassle as many dependendies would need to be remapped.
        """
        del self.origin
        del self.error_message
        self.__class__ = Node

    def raise_error(self):
        raise NodeNotFoundError(self.error_message, self.key, origin=self.origin)


@python_2_unicode_compatible
class ChangeGraph(object):
    """
    Represents the digraph of all changes in a project.

    Each change is a node, and each dependency is an edge. There are
    no implicit dependencies between numbered changes - the numbering is
    merely a convention to aid file listing. Every new numbered change
    has a declared dependency to the previous number, meaning that VCS
    branch merges can be detected and resolved.

    A node should be a tuple: (app_path, change_name). The tree special-cases
    things within an app - namely, root nodes and leaf nodes ignore dependencies
    to other apps.
    """

    def __init__(self):
        self.node_map = {}
        self.nodes = {}
        self.cached = False

    def add_node(self, key, change):
        # If the key already exists, then it must be a dummy node.
        dummy_node = self.node_map.get(key)
        if dummy_node:
            # Promote DummyNode to Node.
            dummy_node.promote()
        else:
            node = Node(key)
            self.node_map[key] = node
        self.nodes[key] = change
        self.clear_cache()

    def add_dummy_node(self, key, origin, error_message):
        node = DummyNode(key, origin, error_message)
        self.node_map[key] = node
        self.nodes[key] = None

    def add_dependency(self, change, child, parent, skip_validation=False):
        """
        This may create dummy nodes if they don't yet exist.
        If `skip_validation` is set, validate_consistency should be called afterwards.
        """
        if child not in self.nodes:
            error_message = (
                'Change %s dependencies reference nonexistent'
                ' child node %r' % (change, child)
            )
            self.add_dummy_node(child, change, error_message)
        if parent not in self.nodes:
            error_message = (
                'Change %s dependencies reference nonexistent'
                ' parent node %r' % (change, parent)
            )
            self.add_dummy_node(parent, change, error_message)
        self.node_map[child].add_parent(self.node_map[parent])
        self.node_map[parent].add_child(self.node_map[child])
        if not skip_validation:
            self.validate_consistency()
        self.clear_cache()

    def remove_replaced_nodes(self, replacement, replaced):
        """
        Removes each of the `replaced` nodes (when they exist). Any
        dependencies that were referencing them are changed to reference the
        `replacement` node instead.
        """
        # Cast list of replaced keys to set to speed up lookup later.
        replaced = set(replaced)
        try:
            replacement_node = self.node_map[replacement]
        except KeyError as exc:
            exc_value = NodeNotFoundError(
                'Unable to find replacement node %r. It was either never added'
                ' to the change graph, or has been removed.' % (replacement, ),
                replacement
            )
            exc_value.__cause__ = exc
            if not hasattr(exc, '__traceback__'):
                exc.__traceback__ = sys.exc_info()[2]
            six.reraise(NodeNotFoundError, exc_value, sys.exc_info()[2])
        for replaced_key in replaced:
            self.nodes.pop(replaced_key, None)
            replaced_node = self.node_map.pop(replaced_key, None)
            if replaced_node:
                for child in replaced_node.children:
                    child.parents.remove(replaced_node)
                    # We don't want to create dependencies between the replaced
                    # node and the replacement node as this would lead to
                    # self-referencing on the replacement node at a later iteration.
                    if child.key not in replaced:
                        replacement_node.add_child(child)
                        child.add_parent(replacement_node)
                for parent in replaced_node.parents:
                    parent.children.remove(replaced_node)
                    # Again, to avoid self-referencing.
                    if parent.key not in replaced:
                        replacement_node.add_parent(parent)
                        parent.add_child(replacement_node)
        self.clear_cache()

    def remove_replacement_node(self, replacement, replaced):
        """
        The inverse operation to `remove_replaced_nodes`. Almost. Removes the
        replacement node `replacement` and remaps its child nodes to
        `replaced` - the list of nodes it would have replaced. Its parent
        nodes are not remapped as they are expected to be correct already.
        """
        self.nodes.pop(replacement, None)
        try:
            replacement_node = self.node_map.pop(replacement)
        except KeyError as exc:
            exc_value = NodeNotFoundError(
                'Unable to remove replacement node %r. It was either never added'
                ' to the change graph, or has been removed already.' % (replacement, ),
                replacement
            )
            exc_value.__cause__ = exc
            if not hasattr(exc, '__traceback__'):
                exc.__traceback__ = sys.exc_info()[2]
            six.reraise(NodeNotFoundError, exc_value, sys.exc_info()[2])
        replaced_nodes = set()
        replaced_nodes_parents = set()
        for key in replaced:
            replaced_node = self.node_map.get(key)
            if replaced_node:
                replaced_nodes.add(replaced_node)
                replaced_nodes_parents |= replaced_node.parents
        # We're only interested in the latest replaced node, so filter out
        # replaced nodes that are parents of other replaced nodes.
        replaced_nodes -= replaced_nodes_parents
        for child in replacement_node.children:
            child.parents.remove(replacement_node)
            for replaced_node in replaced_nodes:
                replaced_node.add_child(child)
                child.add_parent(replaced_node)
        for parent in replacement_node.parents:
            parent.children.remove(replacement_node)
            # NOTE: There is no need to remap parent dependencies as we can
            # assume the replaced nodes already have the correct ancestry.
        self.clear_cache()

    def validate_consistency(self):
        """
        Ensure there are no dummy nodes remaining in the graph.
        """
        [n.raise_error() for n in self.node_map.values() if isinstance(n, DummyNode)]

    def clear_cache(self):
        if self.cached:
            for node in self.nodes:
                self.node_map[node].__dict__.pop('_ancestors', None)
                self.node_map[node].__dict__.pop('_descendants', None)
            self.cached = False

    def forwards_plan(self, target):
        """
        Given a node, returns a list of which previous nodes (dependencies)
        must be applied, ending with the node itself.
        This is the list you would follow if applying the changes to
        a database.
        """
        if target not in self.nodes:
            raise NodeNotFoundError('Node %r not a valid node' % (target, ), target)
        # Use parent.key instead of parent to speed up the frequent hashing in ensure_not_cyclic
        self.ensure_not_cyclic(target, lambda x: (parent.key for parent in self.node_map[x].parents))
        self.cached = True
        node = self.node_map[target]
        try:
            return node.ancestors()
        except (RuntimeError, AttributeError):
            # fallback to iterative dfs
            warnings.warn(RECURSION_DEPTH_WARNING, RuntimeWarning)
            return self.iterative_dfs(node)

    def backwards_plan(self, target):
        """
        Given a node, returns a list of which dependent nodes (dependencies)
        must be unapplied, ending with the node itself.
        This is the list you would follow if removing the changes from
        a database.
        """
        if target not in self.nodes:
            raise NodeNotFoundError('Node %r not a valid node' % (target, ), target)
        # Use child.key instead of child to speed up the frequent hashing in ensure_not_cyclic
        self.ensure_not_cyclic(target, lambda x: (child.key for child in self.node_map[x].children))
        self.cached = True
        node = self.node_map[target]
        try:
            return node.descendants()
        except RuntimeError:
            # fallback to iterative dfs
            warnings.warn(RECURSION_DEPTH_WARNING, RuntimeWarning)
            return self.iterative_dfs(node, forwards=False)

    def iterative_dfs(self, start, forwards=True):
        """
        Iterative depth first search, for finding dependencies.
        """
        visited = deque()
        visited.append(start)
        if forwards:
            stack = deque(sorted(start.parents))
        else:
            stack = deque(sorted(start.children))
        while stack:
            node = stack.popleft()
            visited.appendleft(node)
            if forwards:
                children = sorted(node.parents, reverse=True)
            else:
                children = sorted(node.children, reverse=True)
            # reverse sorting is needed because prepending using deque.extendleft
            # also effectively reverses values
            stack.extendleft(children)

        return list(OrderedSet(visited))

    def root_nodes(self, app=None):
        """
        Returns all root nodes - that is, nodes with no dependencies inside
        their app. These are the starting point for an app.
        """
        roots = set()
        for node in self.nodes:
            if not any(key[0] == node[0] for key in self.node_map[node].parents) and (not app or app == node[0]):
                roots.add(node)
        return sorted(roots)

    def leaf_nodes(self, app=None):
        """
        Returns all leaf nodes - that is, nodes with no dependents in their app.
        These are the "most current" version of an app's schema.
        Having more than one per app is technically an error, but one that
        gets handled further up, in the interactive command - it's usually the
        result of a VCS merge and needs some user input.
        """
        leaves = set()
        for node in self.nodes:
            if not any(key[0] == node[0] for key in self.node_map[node].children) and (not app or app == node[0]):
                leaves.add(node)
        return sorted(leaves)

    def ensure_not_cyclic(self, start, get_children):
        # Algo from GvR:
        # http://neopythonic.blogspot.co.uk/2009/01/detecting-cycles-in-directed-graph.html
        todo = set(self.nodes)
        while todo:
            node = todo.pop()
            stack = [node]
            while stack:
                top = stack[-1]
                for node in get_children(top):
                    if node in stack:
                        cycle = stack[stack.index(node):]
                        raise CircularDependencyError(', '.join('%s.%s' % n for n in cycle))
                    if node in todo:
                        stack.append(node)
                        todo.remove(node)
                        break
                else:
                    node = stack.pop()

    def __str__(self):
        return 'Graph: %s nodes, %s edges' % self._nodes_and_edges()

    def __repr__(self):
        nodes, edges = self._nodes_and_edges()
        return '<%s: nodes=%s, edges=%s>' % (self.__class__.__name__, nodes, edges)

    def _nodes_and_edges(self):
        return len(self.nodes), sum(len(node.parents) for node in self.node_map.values())

    def make_state(self, nodes=None, at_end=True, real_apps=None):
        """
        Given a change node or nodes, returns a complete ProjectState for it.
        If at_end is False, returns the state before the change has run.
        If nodes is not provided, returns the overall most current project state.
        """
        if nodes is None:
            nodes = list(self.leaf_nodes())
        if len(nodes) == 0:
            return ProjectState()
        if not isinstance(nodes[0], tuple):
            nodes = [nodes]
        plan = []
        for node in nodes:
            for change in self.forwards_plan(node):
                if change not in plan:
                    if not at_end and change in nodes:
                        continue
                    plan.append(change)
        project_state = ProjectState(real_apps=real_apps)
        for node in plan:
            project_state = self.nodes[node].mutate_state(project_state, preserve=False)
        return project_state

    def __contains__(self, node):
        return node in self.nodes
