from .debug import debugLog

from json import load as loadJson
from json import loads as loadJsonString
from json import dump as dumpJson
from json import dumps as dumpJsonString

from os import listdir, makedirs
from os.path import isfile, exists, isdir
from datetime import datetime

from PyWarframe.helpers import stripFileName
from PyWarframe.decorators import threaded

class load():
    #Full functions

    #loads json file from directory
    def loadFromDir(dir, fileName=None):
        
        if fileName == None:
            dir, fileName = stripFileName(dir)
        
        debugLog(f'Loading {fileName}', source='loadFromDir')

        if exists(dir) and isdir(dir) and isfile(dir+fileName):
            return loadJson(open(dir+fileName, 'r'))['Data']
        else:
            debugLog(f'Failed Load {dir+fileName}', source='fileManage.loadFromDir', logtype='error')
            return None
    
    #loads multiple json from a directory 
    def loadMulitpleFromDir(dir, fileNames=None):
        returnList = []
        for path in listdir():
            if isfile(path):
                if '.json' in path:
                    if fileNames != None:   
                        debugLog(f'Loading {path}', source='fileManage.loadFromDir')
                        returnList.append(loadJson(open(path, 'r'))['Data'])
                        continue
                    
                    if dir in fileNames:
                        returnList.append(loadJson(open(dir, 'r'))['Data'])
    


        return returnList
 
class save():

    @threaded
    def saveJsonToPath(dir, data, fileName=None):
        if fileName == None:
            dir, fileName = stripFileName(dir)
        
        curTime = datetime.now().timestamp()
        debugLog(f'Saving {dir+fileName} at {str(curTime)}', source='fileManage.saveToPath')
        if not isdir(dir):
            makedirs(dir)
        dumpJson({'Saved':curTime,'Data':data}, open(dir+fileName, 'x'), indent=5)

    @threaded
    def saveBytesToPath(dir, data, fileName):
        if fileName == None:
            dir, fileName = stripFileName(dir)

        with open(dir+fileName, 'wb') as f:
            f.write(data)





class check():
    #check if data is fresh according to a time difference int
    def freshData(dir, timeDiff, fileName=None):
        

        if fileName == None:
            dir, fileName = stripFileName(dir)
        

        if not isfile(dir+fileName):
            return False


        if loadJson(open(dir+fileName))['Saved']-datetime.now().timestamp() > timeDiff:
            return False
        else:
            return True