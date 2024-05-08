# Overview
This is simple script for removal of dead code from python source files. The software support only two situations:
1. 'if True:' or 'if False:' block of code
2. multiple return statements at main level of function
For example if you have:
```
def function():
    if False:
        print("DEV OPTIONS")
        return 0
    if True:
        print("PRODUCTION MODE")
        return 1
    print("VERY DEAD CODE")
    return -1
```
It will be converted (at ast level) into:
```
def function():
    print("PRODUCTION MODE")
    return 1
    print("VERY DEAD CODE")
    return -1
```
and then to
```
def function():
    print("PRODUCTION MODE")
    return 1
    print("VERY DEAD CODE")
    return -1
```

# Motivation
I found several programs which are able to detect dead code but unfortunately I could not find any which can *remove* dead code

# Requirement
    Python 3.9 or higher (ast.unparse was added in Python 3.9)

