"""
Revised Date : 2019-11-17

Environment Checking...

===== Guide =====
- If you want DEBUG_ON True, setup below :
    export DEBUG_ON=True
- Default Setup :
    export DEBUG_ON=False
"""
import os
PKG_PATH = os.path.dirname(os.path.abspath(__file__))


print(f"{'*'*50} {__name__} | Start.\n{__doc__}")

try:
    DBGON = os.environ['DEBUG_ON']
except Exception as e:
    print(f"Exception : {e}")
    DBGON = False
finally:
    print(f"- Current setup status:\nDEBUG_ON={DBGON}")
    print(f"\ndir() :\n{sorted(dir())}")

print(f"\n{'*'*50} {__name__} | End.")



# ============================================================
from idebug.dbg import clsattrs, clsdict, Loop, Looper, printfuncinit, fruntime, utestfunc, objsize, printdf, printiter, printexcep


# from idebug.DataStructure import *
# from idebug.html import *
# from idebug.iinspect import *
# from idebug.mongo import *
from idebug.performance import Function
