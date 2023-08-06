import logging
import re
from collections import deque
from typing import Deque, Iterable, Iterator, List, Optional, Tuple, Union

from .constants import BIND_MAPPING, COMMENT, DASH, SLASH
from .node import N, Node
from .tree_parser import Parser, ParsingError


class ProcessingError(Exception):
    pass


def remove_node(node):
    if node.type in [N.ROOT, N.ROOT_CHILD]:
        return
    parent = node.parent
    index = parent.children.index(node)
    parent.children.remove(node)
    for c in reversed(node.children):
        parent.children.insert(index, c)
        c.parent = parent


def simplify_variable_expansion(root: Node, var_exp: Node) -> Iterable[Node]:
    start, end = var_exp.data.split(DASH, 1)
    if start == "" and end == "":
        var_exp.type = N.TEXT
        yield root
    else:
        try:
            for i in range(int(start), int(end) + 1):
                Node(N.TEXT, var_exp, str(i))
            var_exp.data = ""
            remove_node(var_exp)
            yield root
        except ValueError:
            raise ProcessingError(f'Unable to expand "{var_exp.data}"')


def simplify_alternative(root: Node, alt: Node) -> Iterable[Node]:
    alt.type = N.TEXT
    alt_data = alt.data
    for alternative in alt.data.split(SLASH):
        alt.data = alternative
        yield root
    alt.type = N.ALTERNATIVE
    alt.data = alt_data


def simplify_variable(root: Node, var: Node) -> Iterable[Node]:
    var_children = var.children
    var_data = var.data
    var.children = []
    root_child = var
    while root_child.parent and root_child.parent is not root:
        root_child = root_child.parent
    root_child_index = root.children.index(root_child)
    updated_reference = update_reference(root, var)
    corresponding = None
    if root_child_index == 0:
        corresponding = find_first(root.children[1], (N.VARIABLE,), len_children=len(var_children))
    if corresponding:
        corresponding_children = corresponding.children
        corresponding_data = corresponding.data
        corresponding.children = []
        update_reference(root, corresponding)
    if not corresponding and not update_reference:
        raise ProcessingError("Variable without counterpart and without reference.")
    for i, child in enumerate(var_children):
        var.data = child.data
        var.type = child.type
        var.children = child.children
        if corresponding:
            try:
                corresponding_child = corresponding_children[i]
            except IndexError:
                raise ProcessingError("Corresponding variable has wrong number of children")
            else:
                corresponding.data = corresponding_child.data
                corresponding.type = corresponding_child.type
                corresponding.children = corresponding_child.children
        yield root
    var.data = var_data
    var.type = N.VARIABLE
    var.children = var_children
    if corresponding:
        corresponding.data = corresponding_data
        corresponding.type = N.VARIABLE
        corresponding.children = corresponding_children


def simplify(node: Node) -> Iterable[Node]:
    simplify_func = {
        N.VARIABLE_EXPANSION: simplify_variable_expansion,
        N.VARIABLE: simplify_variable,
        N.ALTERNATIVE: simplify_alternative,
    }
    # node.pprint()
    to_change = find_first(node, (N.VARIABLE_EXPANSION,))
    if to_change is None:
        to_change = find_first(node, (N.VARIABLE, N.ALTERNATIVE))
    if to_change is None:
        # if find_first(node, (N.VARIABLE_REF,)) is not None:
        #     raise ProcessingError("Variable reference to non-existing variable")
        yield node
    else:
        for simpler in simplify_func[to_change.type](node, to_change):
            yield from simplify(simpler)


def find_first(node: Node, node_type: Tuple[int, ...], len_children: Optional[int] = None) -> Optional[Node]:
    if node.type in node_type:
        if len_children is not None:
            if len_children == len(node.children):
                return node
        else:
            return node
    for c in node.children:
        found = find_first(c, node_type)
        if found:
            return found
    return None


def update_reference(node: Node, var: Node) -> bool:
    if node.type is N.VARIABLE_REF and node.data == var.data:
        node.children = [var]
        return True
    return min(update_reference(c, var) for c in node.children) if node.children else False


def print_simple(node: Node):
    if node.type is N.ROOT:
        left = node.children[0]
        right = node.children[1]
        cmd_type = "" if node.data == BIND_MAPPING else " exec --no-startup-id"
        line = f"bindsym {print_simple(left)}{cmd_type} {print_simple(right)}"
        no_doublespace = re.sub(r"[ ]{2,}", " ", line)
        return no_doublespace
    if not node.children:
        return node.data
    else:
        return "".join(print_simple(c) for c in node.children)


def parse(lines: Iterator[str], strict=False) -> Iterator[str]:
    parser = Parser()
    parse = parser.parse
    for line in lines:
        if line != "\n" and not line.startswith(COMMENT):
            try:
                for s in simplify(parse(line.strip())):
                    yield print_simple(s)
            except (ParsingError, ProcessingError) as e:
                logging.debug(e)
                if strict:
                    raise
