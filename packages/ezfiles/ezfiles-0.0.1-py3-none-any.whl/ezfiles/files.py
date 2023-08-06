import os
import json
from typing import List


def readlines(filename: str, strip_newline: bool = True) -> List:
    with open(os.path.abspath(filename), 'r') as f:
        lines = f.readlines()

    if not strip_newline:
        return lines

    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip())
    return new_lines


def writelines(lines: List, filename, append_newline: bool = True) -> None:
    newlines = []
    for line in lines:
        if append_newline and not line.endswith('\n'):
            newlines.append(f"{line}\n")
        else:
            newlines.append(line)

    with open(filename, 'w') as f:
        f.writelines(newlines)


def readstr(filename: str) -> str:
    with open(filename, 'r') as f:
        content = f.read()
    return content


def readjson(filename: str) -> dict:
    content = readstr(filename)
    return json.loads(content)
