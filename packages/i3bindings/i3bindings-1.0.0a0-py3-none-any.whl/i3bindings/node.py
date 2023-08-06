#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import pprint
from typing import List, Optional


class N:
    ROOT = 0
    ROOT_CHILD = 1
    TEXT = 2
    EMPTY = 3
    ALTERNATIVE = 4
    VARIABLE = 5
    VARIABLE_EXPANSION = 6
    VARIABLE_REF = 7

    @classmethod
    def translate(cls, search_value):
        for key, value in cls.__dict__.items():
            if value == search_value:
                return key


class Node:
    __slots__ = ("type", "data", "children", "parent")

    def __init__(self, node_type: int, parent: Node = None, node_data: str = ""):
        self.type = node_type
        self.parent: Optional[Node] = parent
        self.data = node_data
        self.children: List[Node] = []
        if parent is not None:
            parent.children.append(self)

    def serialize(self):
        d = [N.translate(self.type)]
        if self.data:
            d.append(self.data)
        if self.children:
            d.append(list(c.serialize() for c in self.children))
        return tuple(d)

    def pprint(self):
        pprint.pprint(self.serialize(), indent=2)

    def __str__(self):
        return f"({N.translate(self.type)}, {self.data}, {len(self.children)})"

    def __repr__(self):
        return pprint.pformat(self.serialize(), indent=1)

    def __eq__(self, other):
        return self.serialize() == other.serialize()
