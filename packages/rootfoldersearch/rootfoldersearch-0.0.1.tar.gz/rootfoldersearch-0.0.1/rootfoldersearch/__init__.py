import os

def findpath(refpath, depth=10):
    currpath = os.getcwd()
    while depth > 0:
        if os.path.exists(os.path.join(currpath, refpath)):
            return currpath
        depth -= 1
        currpath = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    return None
