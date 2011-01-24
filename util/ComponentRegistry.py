import pdb
import hashlib 
from logger import main_log
#TODO: make component registry a singleton
def initRegistry():
    #TODO: don't overwrite existing registry
    if not 'Registry' in globals():
        globals()['Registry'] = {}

def clearRegistry():
    initRegistry()

def removeComponent(cid):
    globals()['Registry'].pop(cid)

def getComponent(cid):
    return globals()['Registry'][cid]

#Registry of all components of the light system
#TODO: pick a graceful failure behavior and implement it
def registerComponent(component, cid=None):
    if cid != None:
        globals()['Registry'][cid] = component
    else:
        try:
            cid = component['Id']
        except KeyError:
            cid = getNewId() 
            component['Id'] = cid 
            main_log.debug(cid + 'automatically assigned')
        globals()['Registry'][cid] = component
    return cid

def verifyUniqueId(cid):
    return not cid in globals()['Registry']

def removeComponent(cid):
    globals()['Registry'].pop(cid)

def getComponent(cid):
    return globals()['Registry'][cid]

def getNewId():
    trialKey = len(globals()['Registry'])
    trialId = hashlib.md5(str(trialKey)).hexdigest()
    while trialId in globals()['Registry']:
        trialKey += 1
        trialId = hashlib.md5(str(trialKey)).hexdigest()
    return trialId
