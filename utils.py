"""
Utils library
"""

from hashlib import sha256

def get_hash(*args):
    """
    Get a standard hash.
    """
    return sha256((''.join(args)).encode()).hexdigest()
