"""
[A] Edward Rollins, Jr.
[C] enderprime.com
[D] predicate functions
[E] ender.prime@gmail.com
[F] bool.py
[V] 01.22.17
"""

def isBool(v):   return type(v) is bool
def isDict(v):   return type(v) is dict
def isEven(i):   return (i % 2) == 0
def isFloat(v):  return type(v) is float
def isInt(v):    return type(v) is int
def isList(v):   return type(v) is list
def isNeg(n):    return n < 0
def isNull(v):   return v is None
def isNum(v):    return (type(v) is float) or (type(v) is int)
def isOdd(i):    return not ((i % 2) == 0)
def isOne(n):    return n == 1
def isPos(n):    return n >= 0
def isStr(v):    return type(v) is str
def isTuple(v):  return type(v) is tuple
def isZero(n):   return n == 0

def notBool(v):  return not (type (v) is bool)
def notDict(v):  return not (type(v) is dict)
def notFloat(v): return not (type(v) is float)
def notInt(v):   return not (type(v) is int)
def notList(v):  return not (type(v) is list)
def notNull(v):  return not (v is None)
def notNum(v):   return not ((type(v) is float) or (type(v) is int))
def notOne(n):   return not (n == 1)
def notStr(v):   return not (type(v) is str)
def notTuple(v): return not (type(v) is tuple)
def notZero(n):  return not (n == 0)
