from PyWarframe.debug import debugLog
from PyWarframe.helpers import createId

import threading 


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def threadedDaemon(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

def finder(func):
    def wrapper(*args, **kwargs):
        try:
            searchId = createId()
            self = args[0]
            #this will load the following data needed for the items.
            if args != None: 
                for arg in args:
                    if arg in self.jsonRefer.keys():
                        key = arg
                
            if kwargs != None:
                for arg in kwargs:
                    if arg in self.jsonRefer.keys():
                        key = arg
                
            if func.__defaults__ != None:
                for arg in func.__defaults__:
                    if arg in self.jsonRefer.keys():
                        key=arg

            self.jsonRefer[key]['used'].append(searchId)

            if self.jsonRefer[key]['data'] == None:
                self.loadExport(arg).join()

            
            returnVal = func(*args, **kwargs)
            #this deloads it. after the cleaner thread gets it anyway 
            self.jsonRefer[key]['used'].remove(searchId)
            return returnVal
        except Exception as e:
            debugLog(f'Failed Search {func.__name__}; {e}', source='Finder Wrapper', logtype='error')
            self.jsonRefer[key]['used'].remove(searchId)
            #this will (hopefully) deload on an error
            return False
    return wrapper




    

    


