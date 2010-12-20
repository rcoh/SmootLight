import pdb
#Registry of all components of the light system
#TODO: pick a graceful failure behavior and implement it
registry = {}
def registerComponent(component, cid=None):
    if cid != None:
        registry[cid] = component
    else:
        try:
            cid = component['Id']
            registry[cid] = component
        except:
            raise Exception('Must specify Id, component did not store it')
def removeComponent(cid):
    registry.pop(cid)
def getComponent(cid):
    return registry[cid]
