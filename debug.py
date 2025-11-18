
from datetime import datetime

bcolors = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKCYAN": '\033[96m',
    "OKGREEN": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m'
}

#DebugLog will print output to the terminal if debug is set to true
def debugLog(log, source='undefined', logtype='log'):
    debug = True
    if debug:
        if logtype == 'log':
            logColor = bcolors['OKCYAN']
        elif logtype == 'error':
            logColor = bcolors['WARNING']
        print('[' + bcolors['OKCYAN'],datetime.now(), bcolors['ENDC']+ f'] - {bcolors['OKBLUE'] + source + bcolors['ENDC']} - '+logColor, log, bcolors['ENDC'])

