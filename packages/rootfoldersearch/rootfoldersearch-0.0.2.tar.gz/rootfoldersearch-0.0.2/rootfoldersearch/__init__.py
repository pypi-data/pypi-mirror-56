import os

def findpath(refpath, cwd = os.getcwd(), depth=10):
    currpath = os.path.abspath(cwd)
    while depth > 0:
        if os.path.exists(os.path.join(currpath, refpath)):
            return currpath
        depth -= 1
        currpath = os.path.abspath(os.path.join(currpath, os.pardir))
    return None
