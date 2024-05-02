#!/usr/bin/python
# -*- coding: utf-8 -*-
## SEEC - Secure Encrypted Email Client
## Programming project for Secure Programming course at TUNI
##
## General utilities
## 2. May. 2024

def text_editor(prompt, max_empty=2, strip_lines=False) -> str:
    """
    A basic input for writing multiline text
    """
    print(prompt)
    print("="*43)
    lines = []
    line = "<None>"
    empty_lines = 0
    while empty_lines < max_empty:
        line = input("")
        if strip_lines:
            lines.append(line.strip())
        else:
            lines.append(line)
        if line == "":
            empty_lines += 1
        else:
            empty_lines = 0
    print("="*43)
    return "\n".join(lines)

