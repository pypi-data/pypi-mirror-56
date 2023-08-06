import re


COMMAND_MAPPING = "->"
EXEC_MAPPING = "=>"
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
    COMMAND_MAPPING,
    EXEC_MAPPING,
    OPEN_P,
    CLOSE_P,
    OPEN_B,
    CLOSE_B,
    SLASH,
    COMMA,
    AT,
    UNDERSCORE,
    SPACE,
    PLUS,
    DASH,
)
SPECIAL_SET = set(SPECIAL)


_SPECIAL = "|".join(re.escape(x) for x in SPECIAL)

assert "-" in (x[0] for x in SPECIAL), "Change the regex bellow!"
_SPECIAL_FIRST = set(x[0] for x in SPECIAL if x[0] != "-")
_NON_SPECIAL = f"[^{''.join(_SPECIAL_FIRST)}-]"  # add dash at the end so you don't have to escape it
assert set(x[0] for x in SPECIAL if len(x) > 1) - set(x for x in SPECIAL if len(x) == 1) == set(
    ["="]
), "Change the regex bellow!"
# = is OK as long as it is not followed by >
_EXCEPTION = f"(=(?!>))"

TOKENIZER = re.compile(f"{_SPECIAL}|({_NON_SPECIAL}|{_EXCEPTION})+")


TILE_START = "# tile block start {{{"
TILE_END = "# tile block end }}}"
TILE_WARNING = "# WARNING: all lines in this block will be deleted if you run: tile --inplace"
