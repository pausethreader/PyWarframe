from PyWarframe import fileManage
from PyWarframe.debug import debugLog

import requests
import time

from json import loads


class market():
    def __init__(self, dataDir='./data/runtimeGathered/', staleTime=5184000):

        if fileManage.check.freshData(dataDir+'market/marketItems.json', timeDiff=staleTime):
            self.items = fileManage.load.loadFromDir(dataDir+'market/', fileName='marketItems.json')
        else:
            self.items = loads(requests.get('https://api.warframe.market/v2/items').content)['data']
            fileManage.save.saveJsonToPath(dataDir+'market/marketItems.json', self.items)



        self.tradable = []


        for item in self.items:
            self.tradable.append(item['gameRef'])

        self.grab = time.time()
        self.cooldown = .4


    def cooldownCheck(self):
        if time.time() <= self.grab:
            debugLog('Cooldown Triggered', source='Market')
        while time.time() <= self.grab:
            pass
        self.grab = time.time() + self.cooldown

    def getItemData(self, name):
        self.cooldownCheck()

        for item in self.items:
            if item['gameRef'] == name:
                return loads(requests.get('https://api.warframe.market/v2/orders/item/' + item['slug'] + '/top/').content)['data']

        return False

    def getSetData(self, name):
        self.cooldownCheck()
        resets=0
        while resets<5:
            try:
                debugLog(f'Grabbing {name}', source='getSetData', logtype='error')
                data = loads(requests.get('https://api.warframe.market/v2/item/' + name + '/set/').content)['data']
                resets = 6
            except requests.exceptions.ConnectionError:
                debugLog(f'Encountered grab error with {name}, Retrying', source='getSetData', logtype='error')
                resets+=1

        return data['items']