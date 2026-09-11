#!/usr/bin/env python3
"""
Master Builder: 3,000 Verified Clues for Jeopardy Iranian Edition.
- 150 Single Jeopardy categories x 10 clues = 1,500 clues
- 135 Double Jeopardy categories x 10 clues = 1,350 clues
- 75 Final Jeopardy categories x 2 clues = 150 clues
Total: 360 categories, 3,000 verified clues.
Rising difficulty:
  Single: 200=CASUAL, 400=STANDARD, 600=STANDARD, 800=SCHOLAR, 1000=INSUFFERABLE
  Double: 400=STANDARD, 800=STANDARD, 1200=SCHOLAR, 1600=SCHOLAR, 2000=INSUFFERABLE
  Final: 0=INSUFFERABLE
Generates both English and 100% fluent Persian banks.
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

def get_difficulty(value, round_str):
    if round_str == 'final':
        return 'INSUFFERABLE'
    if round_str == 'single':
        if value <= 200: return 'CASUAL'
        if value <= 600: return 'STANDARD'
        if value <= 800: return 'SCHOLAR'
        return 'INSUFFERABLE'
    if round_str == 'double':
        if value <= 400: return 'STANDARD'
        if value <= 800: return 'STANDARD'
        if value <= 1600: return 'SCHOLAR'
        return 'INSUFFERABLE'
    return 'STANDARD'

print("Base configuration loaded.")
