#!/usr/bin/env python3
"""
Master Builder: Expands the Iranian Jeopardy Question Bank to 3,000 Verified Clues.
- 150 Single Jeopardy categories x 10 clues = 1,500 clues ($200 to $1,000)
- 135 Double Jeopardy categories x 10 clues = 1,350 clues ($400 to $2,000)
- 75 Final Jeopardy categories x 2 clues = 150 clues
Total: 360 categories, 3,000 verified clues in English AND 100% fluent Persian.
Orders clues strictly by value and difficulty (rising challenge by price).
"""
import json
import os
import re
import sys
from collections import Counter

from cats_single import SINGLE_150
from cats_double import DOUBLE_135
from cats_final import FINAL_75

def to_persian_digits(s):
    mapping = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    return ''.join(mapping.get(ch, ch) for ch in str(s))

def slugify(text):
    s = text.lower()
    s = re.sub(r'[^a-z0-9]+', '_', s)
    return s.strip('_')

print(f"Loaded 360 categories: {len(SINGLE_150)} Single, {len(DOUBLE_135)} Double, {len(FINAL_75)} Final.")
