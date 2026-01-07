"""
Helper utilities for ID generation and common operations.
"""
import uuid
import random


def gen_id():
    """Generate a short unique ID (12 characters)."""
    return str(uuid.uuid4())[:12]


def pick_weighted(options, weights):
    """Pick from options with weighted probability."""
    return random.choices(options, weights=weights, k=1)[0]
