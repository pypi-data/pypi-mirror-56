#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import re
from typing import Deque, List, Optional

from .constants import (
    AT,
    BIND_MAPPING,
    CLOSE_B,
    CLOSE_P,
    COMMA,
    DASH,
    EXEC_MAPPING,
    OPEN_B,
    OPEN_P,
    PLUS,
    RE,
    SLASH,
    SPACE,
    SPECIAL_SET,
    UNDERSCORE,
)
from .node import N, Node


class ParsingError(Exception):
    pass


class Side:
    LEFT = 0
    RIGHT = 1


class Parser:
    def __init__(self):
        self.parse_special = {
            EXEC_MAPPING: self._parse_exec,
            BIND_MAPPING: self._parse_exec,
            OPEN_P: self._parse_open_p,
            CLOSE_P: self._parse_close_p,
            OPEN_B: self._parse_open_b,
            CLOSE_B: self._parse_close_b,
            SPACE: self._parse_separator,
            SLASH: self._parse_slash,
            COMMA: self._parse_comma,
            DASH: self._parse_dash,
            AT: self._parse_at,
            UNDERSCORE: self._parse_underscore,
            PLUS: self._parse_separator,
        }

    def parse(self, sentance: str) -> Node:
        self.open_stack: Deque[str] = collections.deque()
        self.root = Node(N.ROOT)
        self.parent: Node = Node(N.ROOT_CHILD, self.root)
        self.current: Optional[Node] = None
        self.side = Side.LEFT
        self.last_var = 0
        for match in RE.finditer(sentance):
            # print(match)
            self._parse_match(match.group(0))
        if self.open_stack or len(self.root.children) != 2:
            raise ParsingError("Parsed line cannot be validated.")
        return self.root

    def _parse_match(self, match: str) -> None:
        if match in SPECIAL_SET:
            parse_as_regular = self.parse_special[match](match)
            if not parse_as_regular:
                return
        if self.current is not None:
            self.current.data += match
        else:
            self.current = Node(N.TEXT, self.parent, match)

    def _go_up(self) -> None:
        if self.parent.parent is not None:
            self.parent = self.parent.parent

    def _parse_exec(self, match) -> bool:
        if self.side is Side.LEFT:
            if self.open_stack:
                raise ParsingError("Open parenthesis are not closed.")
            self.current = None
            self.parent = Node(N.ROOT_CHILD, self.root)
            self.side = Side.RIGHT
            self.root.data = match
            return False
        return True

    def _parse_open_p(self, _) -> None:
        self.open_stack.append(OPEN_P)
        self.current = None

    def _parse_close_p(self, _) -> None:
        if not self.open_stack or self.open_stack.pop() != OPEN_P:
            raise ParsingError("Wrong use of parenthesis.")
        self.current = None

    def _parse_open_b(self, _) -> None:
        self.open_stack.append(OPEN_B)
        self.parent = Node(N.VARIABLE, self.parent, str(self.last_var))
        self.last_var += 1
        self.current = None

    def _parse_close_b(self, _) -> None:
        if not self.open_stack or self.open_stack.pop() != OPEN_B:
            raise ParsingError("Wrong use of brackets.")
        # TODO: this might not be needed anymore
        while self.parent.type is not N.VARIABLE:
            self._go_up()
        self._go_up()
        self.current = None

    def _parse_slash(self, _) -> bool:
        if self.side is Side.LEFT:
            if self.current is None or self.current.type not in [N.ALTERNATIVE, N.TEXT]:
                raise ParsingError('Wrong use of "/"')
            self.current.type = N.ALTERNATIVE
        return True

    def _parse_comma(self, _) -> bool:
        if self.parent.type is N.VARIABLE:
            self.current = None
            return False
        return True

    def _parse_dash(self, _) -> bool:
        if self.parent.type is N.VARIABLE:
            if self.current is None or self.current.type is not N.TEXT:
                raise ParsingError('Wrong use of "-"')
            self.current.type = N.VARIABLE_EXPANSION
        return True

    def _parse_at(self, _) -> None:
        self.current = Node(N.VARIABLE_REF, self.parent)

    def _parse_underscore(self, _) -> bool:
        if self.parent.type is N.VARIABLE:
            Node(N.EMPTY, self.parent)
            self.current = None
            return False
        return True

    def _parse_separator(self, match) -> bool:
        if self.open_stack and self.open_stack[-1] is OPEN_P:
            return True
        if self.parent.type is not N.VARIABLE:
            Node(N.TEXT, self.parent, match)
            self.current = None
            return False
        return True
