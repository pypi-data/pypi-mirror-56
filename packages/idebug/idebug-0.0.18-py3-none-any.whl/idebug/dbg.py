"""
Revised : 2019-11-17
"""
# ============================================================ Python.
import inspect
import pprint
pp = pprint.PrettyPrinter(indent=2)
import os
import sys
from datetime import datetime
import re
# ============================================================ External-Library.
# ============================================================ My-Library.
from idebug.lib import inumber
# ============================================================ Project.
from idebug import DBGON


#============================================================
"""Base Code."""
#============================================================




def printfuncinit(f):
    def _printfuncinit(*args, **kwargs):
        print(f"\n{'+'*50} {f.__module__}.{f.__qualname__}")
        return f(*args, **kwargs)
    return _printfuncinit


def fruntime(f):
    def _fruntime(*args, **kwargs):
        start_dt = datetime.now()
        print(f"\n{'+'*50} {f.__module__}.{f.__qualname__}")

        rv = f(*args, **kwargs)

        runt = (datetime.now() - start_dt).total_seconds()
        timeexp, unit = inumber.convert_timeunit(runt)
        print(f"\n{'+ '*25} {f.__module__}.{f.__qualname__} | Function Runtime : {timeexp} ({unit})")
        return rv
    return _fruntime


def utestfunc(f):
    def _utestfunc(*args, **kwargs):
        start_dt = datetime.now()
        print(f"\n\n\n\n\n\n{'='*50} {f.__module__}.{f.__qualname__}")

        rv = f(*args, **kwargs)

        runt = (datetime.now() - start_dt).total_seconds()
        timeexp, unit = inumber.convert_timeunit(runt)
        print(f"\n{'+ '*25} {f.__module__}.{f.__qualname__} | Test Runtime : {timeexp} ({unit})")
        return rv
    return _utestfunc


def printreport(f):
    def func(*args, **kwargs):
        print(f"\n{'*'*50} {f.__module__}.{f.__qualname__}")
        return f(*args, **kwargs)
    return func


def printexcep(f, e, v=None):
    print(f"\n{'#'*50} {f.__module__}.{f.__qualname__}\nException : {e}")
    if v is not None:
        print("\nlocals():")
        pp.pprint(v)


@printfuncinit
def clsattrs(cls, loose=True):
    if DBGON:
        try:
            whour = f"cls : {cls.__class__.__name__}"
            p_hidden = re.compile('^_.*')
            p_df = re.compile('_*df_*')
            attrs = dir(cls)
            if loose:
                attrs = [e for e in attrs if p_hidden.match(e) is None]
            for attr in attrs:
                try:
                    v = getattr(cls, attr)
                    if p_df.search(string=attr) is None:
                        print(f"{'-'*50} {whour}\na : {attr}\nv : {v}\nt : {type(v)}")
                        if isinstance(v, dict):
                            print("When isinstance(v, dict) :")
                            pp.pprint(v)
                    else:
                        print(f"{'-'*50} {whour}\na : {attr}\nv : 생략.\nt : {type(v)}")
                except Exception as e:
                    pass
        except Exception as e:
            printexcep(f=clsattrs, e=e, v=locals())


@printfuncinit
def clsdict(cls, loose=False):
    if DBGON:
        try:
            whour = f"cls : {cls.__class__.__name__}"
            p_hidden = re.compile('^_.*')
            p_df = re.compile('_*df_*')
            dkeys = list(cls.__dict__)
            if loose:
                dkeys = [e for e in dkeys if p_hidden.match(e) is None]
            for k,v in cls.__dict__.items():
                if k in dkeys:
                    if p_df.search(string=k) is None:
                        print(f"{'-'*50} {whour}\n{k} : {v}")
                        if isinstance(v, dict):
                            print("When isinstance(v, dict) :")
                            pp.pprint(v)
                    else:
                        print(f"{'-'*50} {whour}\n{k} : 생략.")
        except Exception as e:
            printexcep(f=clsdict, e=e, v=locals())


class Loop:
    start_dt = datetime.now()
    count = 0

    def __init__(self, iterable, func):
        self.it = iter(iterable)
        self.len = len(iterable)
        # sefl.itname = iterable.__name__
        self.f = func

    def next(self):
        if hasattr(self.f, '__qualname__'):
            whoiam = f"{self.f.__module__}.{self.f.__qualname__}"
        else:
            whoiam = f"{self.f.__module__}.{self.f.__name__}"
        self.count += 1
        print(f"{'-'*50} {whoiam} ({self.count}/{self.len})")
        # self.it.next()
        next(self.it)
        pass


class Looper:

    def __init__(self, cframe, len, exp_runtime=60):
        self.start_dt = datetime.now()
        self.count = 1
        self.len = len
        self.exp_runtime = exp_runtime
        frameinfo = inspect.getframeinfo(frame=cframe)
        self.caller = f"{frameinfo.filename} | {frameinfo.function}"

    def report(self, addi_info):
        whoiam = f"{'*'*50} {__name__}.{__class__.__qualname__}"
        cum_runtime = (datetime.now() - self.start_dt).total_seconds()
        avg_runtime = cum_runtime / self.count
        leftover_runtime = avg_runtime * (self.len - self.count)
        print(f"{whoiam} | ({self.count}/{self.len})")
        print(f" caller : {self.caller}\n addi_info : {addi_info}")
        tpls = [
            ('누적실행시간', cum_runtime),
            ('잔여실행시간', leftover_runtime),
            ('평균실행시간', avg_runtime),
        ]
        for tpl in tpls:
            timeexp, unit = inumber.convert_timeunit(tpl[1])
            print(f" {tpl[0]} : {timeexp} ({unit})")
        if self.count == self.len:
            if avg_runtime > self.exp_runtime:
                print(f"{whoiam}\n Save the final report into DB.")
        self.count += 1
        return self





def objsize(obj, seen=None):
    """Recursively finds size of objects
    https://goshippo.com/blog/measure-real-size-any-python-object/
    """
    whoiam = f"{__name__}.{inspect.stack()[0][3]}"
    print(f"{'*'*50} {whoiam}")
    print(f"type : {type(obj)}")
    print(f"size : {sys.getsizeof(obj)} (bytes)")
    try:
        if hasattr(obj, '__name__'):
            print(f"objname : {obj.__name__}")
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")
    try:
        print(f"len : {len(obj)}")
    except Exception as e:
        print(f"{'#'*50} {whoiam}\nException : {e}")

    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])

@printfuncinit
def printdf(df, slen=10):
    slen = abs(slen)
    _slen = slen * -1
    print(f"\n{'* '*25} df.info()")
    print(df.info())

    # print(f"\n{'* '*25} df[:{slen}].T")
    # print(f"{df[:slen].T}")
    print(f"\n{'* '*25} df.head({slen}).T")
    print(f"{df.head(slen).T}")

    if len(df) > 50:
        print(f"\n{'* '*25} df.head({slen}) | df.tail({slen})")
        print(f"{df.head(slen)}")
        print(f"{df.tail(slen)}")
    else:
        print(f"\n{'* '*25} df")
        print(f"{df}")

    print(f"\n{'* '*25} df.tail({slen}).T")
    print(f"{df.tail(slen).T}")


def printiter(iterable, slen=10):
    print(f"{'*'*50} {__name__}.{inspect.stack()[0][3]}")
    print(f"len(iterable) : {len(iterable)}")
    if len(iterable) > 50:
        print(f"\niterable[:{slen}] :")
        pp.pprint(iterable[:slen])
        print(f"\niterable[{-1*slen}:] :")
        pp.pprint(iterable[-1*slen:])
    else:
        pp.pprint(iterable)
