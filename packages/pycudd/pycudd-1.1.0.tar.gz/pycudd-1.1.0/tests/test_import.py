from __future__ import print_function

import os
import sys

old_path = list(sys.path)

#sys.path.append(PYCUDD_PATH)
cwd = os.getcwd()
if cwd in sys.path:
    sys.path.remove(cwd)

try:
    import pycudd
    print('Successfully imported package')
    print(pycudd.__file__)
except ImportError:
    raise Exception('Compilation error: could not import pycudd')
finally:
    sys.path = old_path
