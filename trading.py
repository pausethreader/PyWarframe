from PyWarframe import fileManage
from PyWarframe.debug import debugLog
from PyWarframe.inventory import inventory
from PyWarframe.market import market


class trading():
    #profile = inventory class, market = market class, dataDir = save data dir, staleTime = time since update (default 24h)
    def __init__(self, profile=inventory, market=market, dataDir='./data/runtimeGathered/', staleTime=5184000):
        #Get what we need from the profile
        self.profile = profile
        self.market = market
        self.items = []
        self.items += self.profile.miscItems
        self.items += self.profile.upgrades['raw']
        self.items += self.profile.upgrades['leveled']
        self.items += self.profile.recipes


        #Filter out useless data to avoid consuming literally all of my debicated wam 
        itemFilter = []
        for item in self.items:
            itemAppend = {
                'type': item['ItemType']
            }

            if 'ItemCount' in item.keys():
                itemAppend['count'] = item['ItemCount']
            else:
                itemAppend['count'] = 1

            itemFilter.append(itemAppend)

        self.items = itemFilter

        self.dataDir = dataDir
        #Runtime gathered data loaded here
        if fileManage.check.freshData(dataDir+'market/sets.json', timeDiff=staleTime):
            self.sets = fileManage.load.loadFromDir(dataDir+'market/', fileName='sets.json')
        else:
            self.sets = self.getSets()


        if fileManage.check.freshData(dataDir+'market/inventory.json', timeDiff=staleTime):
            self.tradable = fileManage.load.loadFromDir(dataDir+'market/', fileName='inventory.json')
        else:
            self.tradable = self.getInventoryTradable()

    #Gets provided sets from warframe market
    def getSets(self):
        sets={}
        for set in self.market.items:
            if 'set' in set['tags']:
                debugLog('Found Set: ' + set['slug'], source='Trading')

                sets[set['slug']] = {'items':[], 'owned':False}
                for item in self.market.getSetData(set['slug']):

                    if item['setRoot']:
                        continue

                    owned = 0
                    for inventoryItem in self.items:
                        if item['gameRef'] == inventoryItem['type']:
                            owned=inventoryItem['count']
                            break



                    sets[set['slug']]['items'].append({
                        'slug':item['slug'],
                        'gameRef':item['gameRef'],
                        'owned':owned
                    })

        for set in sets.keys():
            setParts = len(sets[set]['items'])
            ownedParts = 0
            for item in sets[set]['items']:
                if item['owned'] > 0:
                    ownedParts+=1

            if ownedParts == setParts:
                sets[set]['owned'] = True

        fileManage.save.saveJsonToPath(self.dataDir+'market/', sets, 'sets.json')
        return sets

    #Gets items that are likely tradable within your 
    def getInventoryTradable(self):
        tradableItems=[]
        for item in self.market.items:
            if 'set' in item['tags']:
                debugLog('Found Set: ' + item['slug'] + ' Ignoring.', source='Trading')
                continue



            for item2 in self.items:
                if item['gameRef'] == item2['type']:
                    tradableItems.append(item2)
                    debugLog('Found ' + item2['type'] + ' With ' + str(item2['count']), source='Trading')
                    break

        fileManage.save.saveJsonToPath(self.dataDir+'market/', tradableItems, 'inventory.json')



        return tradableItems