import hashlib 
from logger import main_log
import thread
#TODO: make component registry a singleton
def initRegistry():
    globals()['trialKey'] = 0
    #TODO: don't overwrite existing registry
    if not 'Registry' in globals():
        globals()['Registry'] = {}
    makelock()
        
        
def makelock():
    global utilLock
    utilLock = thread.allocate_lock()
def clearRegistry():
    initRegistry()

def removeComponent(cid):
    global Registry
    Registry.pop(cid)

def getLock():
    global utilLock
    return utilLock
def getComponent(cid):
    global Registry
    return Registry[cid]

#Registry of all components of the light system
#TODO: pick a graceful failure behavior and implement it
def registerComponent(component, cid=None):
    global Registry
    if cid != None:
        Registry[cid] = component
    else:
        cid = component['Id']
        if cid == None:
            cid = getNewId() 
            component['Id'] = cid 
            main_log.debug(cid + 'automatically assigned')
        if cid in Registry:
            main_log.warn(cid + 'overwritten.')
        Registry[cid] = component
    return cid

def verifyUniqueId(cid):
    global Registry
    return not cid in Registry

def removeComponent(cid):
    global Registry
    Registry.pop(cid)

def getNewId():
    global trialKey
    trialKey += 1
    trialId = hashlib.md5(str(trialKey)).hexdigest()
    while trialId in Registry:
        trialKey += 1
        trialId = hashlib.md5(str(trialKey)).hexdigest()
    return trialId
