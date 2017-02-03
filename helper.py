#!/usr/bin/env python
"""This module contains helper functions."""

def is_integer(string):
    """Return integer number if |string| is a number. Otherwise, return None."""
    try:
        return int(string)
    except ValueError:
        return None

def is_number(string):
    """Return float number if |string| is a number. Otherwise, return None."""
    try:
        return float(string)
    except ValueError:
        return None
