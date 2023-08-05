import os
import sys

try:

    # Save sys.path
    _path = sys.path[:]

    sys.path = [p for p in sys.path if p not in ("", os.getcwd())]

    # Import 
    from .pyzt import inputs, inputi, inputf, inputc
    try:
        from .pyzt import get_long
    except ImportError:
        pass

finally:

    # Restore student's sys.path (just in case library raised an exception that caller caught)
    sys.path = _path