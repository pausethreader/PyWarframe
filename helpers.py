from random import choice


def createId():
    return ''.join(choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(30))

def stripFileName(dir):
    splitIndex = dir.rfind('/')
    fileName = dir[splitIndex+1:]
    dir = dir[:splitIndex+1]

    return dir, fileName