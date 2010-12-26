from xml.etree.ElementTree import *
import xml
import pdb
import util.Strings as Strings
classArgsMem = {}
CONFIG_PATH = 'config/'
def loadParamRequirementDict(className):
    if not className in classArgsMem: #WOO CACHING
        classArgsMem[className] = fileToDict(CONFIG_PATH + className) 
    return classArgsMem[className]
#Loads a config file.  If its an xml file, inheritances are automatically resolved.
def loadConfigFile(fileName): #TODO: error handling etc.
    #try:
        #fileName = CONFIG_PATH + fileName
        if '.params' in fileName:
            return fileToDict(fileName)
        if '.xml' in fileName:
            config = ElementTree() #use .fromstring, and resolve xincludes
            config.parse(fileName)
            config = ElementTree(resolveConfigInheritance(config.getroot()))
            return config
    #except:
        return None
#Takes an Element or an ElementTree.  If it is a tree, it returns its root.  Otherwise, just returns
#it
def getElement(el):
    if xml.etree.ElementTree.iselement(el):
        return el
    elif el.__class__ == ElementTree:
        return el.getroot()
def compositeXMLTrees(parentTree, overridingTree): #TODO: break up into sub-methods, change it to
#use .find()
    #type checking -- convert ElementTrees to their root elements
    parentTree = getElement(parentTree)
    overridingTree = getElement(overridingTree)
    parentItems = parentTree.getchildren()
    overrideItems = overridingTree.getchildren()
    #first, lets figure out what tags we have in the override tree:
    tagCollection = [el.tag for el in overrideItems] #we can speed this up with a dict if necessary
    for item in parentItems:
        if not item.tag in tagCollection: #no override 
            overridingTree.insert(-1, item) #insert the new item at the end
        else:
            #do we merge or replace?
            intersectingElements = findElementsByTag(item.tag, overrideItems)
            if len(intersectingElements) > 1:
                print 'ABUSE!'
            interEl = intersectingElements[0]
            mode = 'Replace'
            if Strings.OVERRIDE_BEHAVIOR in interEl.attrib:
                mode = interEl.attrib[Strings.OVERRIDE_BEHAVIOR] 
            if mode != 'Replace' and mode != 'Merge':
                print 'Bad Mode.  Choosing to replace.'
                mode = 'Replace'
            if mode == 'Replace':
                pass #we don't need to do anything
            if mode == 'Merge': 
                interEl = compositeXMLTrees(item, interEl)
    for item in overrideItems: #resolve appendages
        if item.tag == 'APPEND':
            children = item.getchildren()
            for child in children:
                overrideItems.insert(-1, child)
            overrideItems.remove(item)
    return overridingTree
def findElementsByTag(tag, eList):
    return [el for el in eList if el.tag == tag]
def fileToDict(fileName):
    fileText = ''
    try:
        print 'File Read'
        with open(fileName) as f:
            for line in f:
                fileText += line.rstrip('\n').lstrip('\t') + ' ' 
    except IOError:
        return {}
    if fileText == '':
        return {}
    return eval(fileText)
#parses arguments into python objects if possible, otherwise leaves as strings
def generateArgDict(parentNode, recurse=False):
    args = {}
    for arg in parentNode.getchildren():
        key = arg.tag
        if arg.getchildren() != []:
            value = generateArgDict(arg, True)
        else:
            #convert into python if possible, otherwise don't
            try:
                value = eval(arg.text)
            except (NameError,SyntaxError):
                value = str(arg.text)
        if key in args: #build of lists of like-elements
            if type(args[key]) != type([]):
                args[key] = [args[key]]
            args[key].append(value)
        else:
            args[key]=value
    #if we should be a list but we aren't:
    if len(args.keys()) == 1 and recurse:
        return args[args.keys()[0]]
    return args

def resolveConfigInheritance(el):
    parentClass = el.find('InheritsFrom')
    if parentClass != None:
        parentTree = loadConfigFile(parentClass.text)
        el = compositeXMLTrees(el, parentTree) 
        el.remove(parentClass) #get rid of the inheritance flag
    return el
