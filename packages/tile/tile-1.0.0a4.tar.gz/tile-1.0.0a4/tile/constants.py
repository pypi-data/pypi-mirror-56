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
    DASH,  # This must be last! (so we don't have to escape it in _NON_SPECIAL)
)
SPECIAL_SET = set(SPECIAL)


_SPECIAL = "|".join(map(re.escape, SPECIAL))
_NON_SPECIAL = f"[^{''.join(x for x in SPECIAL if len(x) == 1)}]"
_NEGATIVE_LOOKAHEAD = f"(?!{'|'.join(re.escape(x) for x in SPECIAL if len(x) > 1)})"

TOKENIZER = re.compile(f"{_SPECIAL}|{_NON_SPECIAL}+{_NEGATIVE_LOOKAHEAD}")


TILE_START = "# tile block start {{{"
TILE_END = "# tile block end }}}"
TILE_WARNING = "# WARNING: all lines in this block will be deleted if you run: tile --inplace"
