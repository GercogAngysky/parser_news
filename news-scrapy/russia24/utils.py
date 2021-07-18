from string import whitespace
from w3lib.html import remove_tags


def clear_string(string):
    return remove_tags(
        string.translate(
            {ord(c): ' ' for c in whitespace}
            )
        )
