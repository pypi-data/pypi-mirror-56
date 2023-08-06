"""
Revised Data : 2019-11-11
"""
# ============================================================ Django.
# ============================================================ Python.
import os
import sys
# ============================================================ External-Library.
# ============================================================ My-Library.
from idebug import PKG_PATH
PJTS_PATH = os.path.dirname(os.path.dirname(PKG_PATH))

sys.path.append(f"{PJTS_PATH}/ilib")
from ilib import inumber
# ============================================================ App.
# ============================================================ Global-Variables.



print(f"{'*'*50} {__name__} | Start.\n{__doc__}\n")
print(f"{'*'*50} {__name__} | End.")
