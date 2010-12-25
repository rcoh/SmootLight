import pdb
#component registry, a singleton
import thread
#class ComponentRegistry:
#    def __init__(self):
#        self.regDict = {}
#    @staticmethod
#    def getRegistry(self):
#        if self.instance == None:
#            self.instance = self.__class__() 
#        return self.instance
#    def registerComponent(component, cid=None):
#        if cid != None:
#            globals()['Registry'][cid] = component
#        else:
#            try:
#                cid = component['Id']
#                globals()['Registry'][cid] = component
#            except:
#                raise Exception('Must specify Id, component did not store it')
#def registerDefault(
def removeComponent(cid):
    globals()['Registry'].pop(cid)
def getComponent(cid):
    return globals()['Registry'][cid]
#Registry of all components of the light system
#TODO: pick a graceful failure behavior and implement it
def initRegistry():
    globals()['Registry'] = {}
def registerComponent(component, cid=None):
    if cid != None:
        globals()['Registry'][cid] = component
    else:
        try:
            cid = component['Id']
            globals()['Registry'][cid] = component
        except:
            raise Exception('Must specify Id, component did not store it')
#def registerDefault(
def removeComponent(cid):
    globals()['Registry'].pop(cid)
def getComponent(cid):
    return globals()['Registry'][cid]
