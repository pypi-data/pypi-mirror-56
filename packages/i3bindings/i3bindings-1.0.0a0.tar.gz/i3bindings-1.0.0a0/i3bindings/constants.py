import re

BIND_MAPPING = "->"
EXEC_MAPPING = "#>"
OPEN_P = "("
CLOSE_P = ")"
OPEN_B = "{"
CLOSE_B = "}"
SLASH = "/"
COMMA = ","
DASH = "-"
AT = "@"
UNDERSCORE = "_"
SPACE = " "
PLUS = "+"
COMMENT = "#"
SPECIAL = (
    BIND_MAPPING,
    EXEC_MAPPING,
    OPEN_P,
    CLOSE_P,
    OPEN_B,
    CLOSE_B,
    SLASH,
    COMMA,
    DASH,
    AT,
    UNDERSCORE,
    SPACE,
    PLUS,
)
SPECIAL_SET = set(SPECIAL)


def _escape(s: str) -> str:
    if s in (".", "^", "$", "*", "+", "?", "{", "}", "[", "]", "\\", "|", "(", ")"):
        return f"\{s}"
    return s


def _escape_in_set(s: str) -> str:
    if s == "-":
        return f"\{s}"
    return s


_SPECIAL = r"|".join(_escape(x) for x in SPECIAL)
_NON_SPECIAL = rf"[^{''.join(_escape_in_set(x) for x in set(''.join(SPECIAL)))}]"
_RE = rf"{_SPECIAL}|{_NON_SPECIAL}+"
RE = re.compile(_RE)


I3BINDING_START = "# i3bindings block start {{{"
I3BINDING_END = "# i3bindings block end }}}"
I3BINDING_WARNING = "# WARNING: all lines in this block will be deleted if you run: i3bindings --inplace"
