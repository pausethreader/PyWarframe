from PyWarframe.debug import debugLog
from PyWarframe.decorators import threaded

from os import makedirs
from os.path import exists
from json import loads

import requests 


#This portion of the code isn't done. Use Warframe Extractor instead for the majority of these please. 

class browseWF():
    def __init__(self):
        print('fuck off ')
    
    @threaded
    def writeImage(self, dir, gameRef, content):
        debugLog(f'Writing img {gameRef}', source='writeImage')
        makedirs(dir)
        with open(dir+'/img.png', 'wb') as file:
            file.write(requests.get('http://browse.wf'+content['icon']).content)
        debugLog(f'done writing img {gameRef}', source='writeImage')



    def browsewfImg(self, gameRef):
        debugLog(f'Getting {gameRef} from Browse.WF', source='browsewfIMG')

        content = loads(requests.get('http://browse.wf'+gameRef).content)
        if ('resultType' in content.keys()) and (not (exists('./data/images/items/'+gameRef+'/img.png'))):
            self.browsewfImg(content['resultType'])
        else: 
            if not exists('./data/images/items/'+gameRef+'/img.png'):
                #self.writeImage(dir=('./data/images/items/'+gameRef+'/img.png'), content=content, gameRef=gameRef)
                pass

            debugLog(f'passing {gameRef}', source='writeImage')
            return './data/images/items/'+gameRef+'/img.png'
        