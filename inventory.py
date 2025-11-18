from json import load as jsonLoad


class inventory():
    def __init__(self, path):
        self.data = jsonLoad(open(path, 'r'))
        #Loads all weapons into a dictionary. These are all loaded at once. 
        self.weapons = {
            'Primary':self.data['LongGuns'],
            'Secondary':self.data['Pistols'],
            'Melee':self.data['Melee']
        }
        #Loads all other items. 
        self.miscItems = self.data['MiscItems']
        self.flavorItems = self.data['FlavourItems']
        self.upgrades = {
            'raw':self.data['RawUpgrades'],
            'leveled':self.data['Upgrades']
        }
        self.relics = self.getRelics()
        self.recipes = self.data['Recipes']



    def getRelics(self):
        returnValue = []
        for item in self.miscItems:

            if '/Projections/' in item['ItemType']:
                returnValue.append(item)

        return returnValue