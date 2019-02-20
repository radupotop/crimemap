"""
Utils library
"""

from hashlib import sha256


def get_hash(*args):
    """
    Get a standard hash.
    """
    arglist = [str(a) for a in args]
    return sha256((''.join(arglist)).encode()).hexdigest()
