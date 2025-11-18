from PyWarframe.debug import debugLog
from PyWarframe.decorators import finder, threaded, threadedDaemon

import time
from json import load as jsonLoad
from os import listdir

from PyWarframe.helpers import createId


class exportData():
    def __init__(self, directory, lang):
        self.createId = createId
        self.loadDir = directory
        self.jsonRefer = {}

        self.cleanupTime = 3

        self.dict = jsonLoad(open(directory + f'dict.{lang}.json','r'))

        #List of the used json files.
        for item in listdir(directory):
            #convieniently .json check means no checking if file actually exists. neato 
            if '.json' in item:
                if 'Export' in item:
                    debugLog(f'Found Export item: {item}', source='exportData')
                    itemRefer = item.replace('Export', '').replace('.json', '')
                    itemRefer = itemRefer[0].lower() + itemRefer[1:]
                    self.jsonRefer[itemRefer] = {
                        'data': None,
                        'used':[]
                    }
                    debugLog(f'Export Item Registered: {item} as {itemRefer}', source='exportData')


        #load all items via thread.
        for item in self.jsonRefer.keys():
            self.loadExport(item)

        #start cleaner thread. 
        self.cleaner()







    @threaded
    def loadExport(self, item):
        try:
            self.jsonRefer[item]['data'] = jsonLoad(open(self.loadDir + f'Export{item[0].upper() + item[1:]}.json', 'r'))
            debugLog(f'Loaded Export - {item}', source='exportData SubThread')
            return True
        except:
            debugLog(f'Failed to load export - {item}', source='exportData SubThread', logtype='error')
            return False

    #single threaded because this is not hard 
    def unloadItem(self, item):
        self.jsonRefer[item]['data'] = None



    def findItemClass(self, item):
        print(item)
        if 'Weapons' in item:
            item = 'weapons'
        elif 'Powersuits' in item:
            item = 'warframes'

        elif 'Projections' in item:
            item='relics'
        else:
            item='resources'

        return item


    #cleans up unused json data when possible. essentially garbage collection 
    @threadedDaemon
    def cleaner(self):
        while True:
            time.sleep(self.cleanupTime)
            for item in self.jsonRefer.keys():
                #if thread not used and is loaded
                if self.jsonRefer[item]['used'] == [] and not (self.jsonRefer[item]['data'] == None):
                    self.jsonRefer[item]['data'] = None
                    debugLog(f'Unloaded Export - {item}', source='Cleaner Thread')
                if self.jsonRefer[item]['used'] != []:
                    debugLog(f'Failed Unload - {item}', source='Cleaner Thread')

    #finds an item via the itemClass and itemUniqueName
    @finder
    def findItem(self, name, itemClass):
        debugLog(f'Found a loaded value: {name}', source='findItem Call')
        returnValue = self.jsonRefer[itemClass]['data'][name]

        return returnValue



    #expects a name relevent to the set language. 
    @finder
    def findUniqueName(self, name, itemClass):
        searchId = self.createId()


        for item in self.dict.keys():
            if self.dict[item] == name:
                #Reverse search. dict -> dict key -> itemName
                dictName = item
                break

        #we are using this 
        self.jsonRefer[itemClass]['used'].append(searchId)
        if self.jsonRefer[itemClass]['data'] == None:
            self.loadExport(itemClass).join()

        returnValue = False
        for item in self.jsonRefer[itemClass]['data'].keys():
            if self.jsonRefer[itemClass]['data'][item]['name'] == dictName:
                #returnValue prevents deload before we return the item
                returnValue = item

        #We are not using this anymore
        self.jsonRefer[itemClass]['used'].append(searchId)
        return returnValue

    #Find unique name of all in said itemclass
    @finder
    def findItems(self, itemClass):

        returnValue = []
        for item in self.jsonRefer[itemClass]['data'].keys():
            returnValue.append([item, self.dict[self.jsonRefer[itemClass]['data'][item]['name']]])

        return returnValue

    #we handle recipies and the such seperately because I am fucking lazy
    @finder
    def findRelicByName(self, era, catagory, itemClass='relics'):
        returnValue = False
        for key in self.jsonRefer[itemClass]['data'].keys():
            item = self.jsonRefer[itemClass]['data'][key]
            if era == item['era'] and catagory == item['category']:
                returnValue = key
                break
        return returnValue


    #finds the first recipy by the result type. 
    @finder
    def findRecipesByResult(self, result, itemClass = 'recipes'):
        returnValue = []
        for key in self.jsonRefer[itemClass]['data'].keys():
            item = self.jsonRefer[itemClass]['data'][key]
            if result == item['resultType']:
                returnValue.append(key)

        return returnValue

    @finder
    def findFullData(self, name, itemClass):
        returnValue = self.jsonRefer[itemClass]['data'][name]
        return returnValue

    @finder
    def constructRelicName(self, item, itemClass = 'relics'):

        returnValue = self.jsonRefer[itemClass]['data'][item]['era']+' '+ self.jsonRefer[itemClass]['data'][item]['category'] + ' Relic'

        return returnValue

    @finder
    def getRelicRewards(self, relic, itemClass = 'relics'):
        searchId = self.createId()
        #we are using this 


        relic = self.jsonRefer[itemClass]['data'][relic]['rewardManifest']

        returnValue = self.getRewardManifest(relic)

        return returnValue

    @finder
    def getRewardManifest(self, manifestPath, itemClass = 'rewards'):

        manifest = self.jsonRefer[itemClass]['data'][manifestPath]

        returnValue = manifest
        return returnValue