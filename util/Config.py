from xml.etree.ElementTree import *
import re
import sys
import xml
import pdb
import util.Strings as Strings
import util.Search as Search
from logger import main_log, exception_log
classArgsMem = {}
CONFIG_PATH = 'config/'
DEFAULT_OVERRIDE_MODE = 'Merge'

def loadParamRequirementDict(className):
    if not className in classArgsMem: #WOO CACHING
        classArgsMem[className] = fileToDict(CONFIG_PATH + className) 
    return classArgsMem[className]

def loadConfigFile(fileName): #TODO: error handling etc.
    """Loads a config file.  If its an xml file, inheritances are automatically resolved."""
    try:
        if '.params' in fileName:
            return fileToDict(fileName)
        if '.xml' in fileName:
            config = ElementTree() 
            config.parse(fileName)
            resolveDocumentInheritances(config.getroot())
            return config
    except Exception as inst:
        if '.xml' in fileName:
            main_log.error('Error loading config file ' + fileName)#, inst) TODO: log exception too
            main_log.error(str(inst))
        return None
def getElement(el):
    """Takes an Element or an ElementTree.  If it is a tree, it returns its root.  Otherwise, just returns
    it"""
    if xml.etree.ElementTree.iselement(el):
        return el
    elif el.__class__ == ElementTree:
        return el.getroot()
def compositeXMLTrees(parentTree, overridingTree): 
    """XML tree composition.  Returns the resulting tree, but happens in-place in the overriding
    tree."""
    #TODO: break up into sub-methods, change it to use .find()
    if parentTree == None:
        return overridingTree
    if overridingTree == None:
        return parentTree #TODO: this will probably cause a bug since it isn't in-place on
        #overridingTree
    parentTree = getElement(parentTree)
    overridingTree = getElement(overridingTree)
    parentItems = parentTree.getchildren()
    overrideItems = overridingTree.getchildren()
    #first, lets figure out what tags we have in the override tree:
    tagCollection = [el.tag for el in overrideItems] #we can speed this up with a dict if necessary
    for item in parentItems:
        if not item.tag in tagCollection or 'Append' in item.attrib: #no override 
            overridingTree.insert(-1, item) #insert the new item at the end
        else:
            #do we merge or replace?
            intersectingElements = findElementsByTag(item.tag, overrideItems)
            if len(intersectingElements) > 1:
                main_log.warn('ABUSE!  Override of multiple items isn\'t well defined.  Don\'t do\
                it!')
            interEl = intersectingElements[0]
            mode = DEFAULT_OVERRIDE_MODE
            if Strings.OVERRIDE_BEHAVIOR in interEl.attrib:
                mode = interEl.attrib[Strings.OVERRIDE_BEHAVIOR] 
            if mode != 'Replace' and mode != 'Merge':
                main_log.warn('Bad Override Mode.  Choosing to replace.')
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
        with open(fileName) as f:
            for line in f:
                fileText += line.rstrip('\n').lstrip('\t') + ' ' 
    except IOError:
        main_log.info('Failure reading ' + fileName)
        return {}
    if fileText == '':
        return {}
    try:
        resultDict = eval(fileText)
        main_log.info(fileName + ' read and parsed')
        return resultDict
    except:
        main_log.exception(fileName + ' is not a well formed python dict.  Parsing failed') 
    return eval(fileText)

def pullArgsFromItem(parentNode):
    """Parses arguments into python objects if possible, otherwise leaves as strings"""
    attribArgs = {}
    for arg in parentNode.attrib: #automatically pull attributes into the argdict
        attribArgs[arg] = attemptEval(parentNode.attrib[arg])
    argNode = parentNode.find('Args')
    args = generateArgDict(argNode)
    for key in attribArgs:
        args[key] = attribArgs[key]
    return args

def attemptEval(val):
    """Runs an eval if possible, or converts into a lambda expression if indicated.  Otherwise,
    leaves as a string."""
    try:
        if '${' in val and '}$' in val: #TODO: this could be a little cleaner
            dictVal = re.sub("'\$\{(.+?)\}\$'", "b['\\1']", val) #replace expressions '${blah}$' with b['blah']
            dictVal = re.sub("\$\{(.+?)\}\$", "a['\\1']", dictVal) #replace all expressions like {blah} with a['blah']
            if "'${" and "}$'" in val: #nested lambda madness
                lambdaVal = eval('lambda a: lambda b: ' + dictVal)
            else:
                lambdaVal = eval('lambda a:'+dictVal) #TODO: nested lambdas
            return lambdaVal  #convert referential objects to lambda expressions which can be
            #resolved dynamically.
        else:
            val = eval(val)
    except (NameError, SyntaxError):
        val = str(val)
    return val

def generateArgDict(parentNode, recurse=False):
    args = {}
    for arg in parentNode.getchildren():
        key = arg.tag
        if arg.getchildren() != []:
            value = generateArgDict(arg, True)
        else:
            #convert into python if possible, otherwise don't
            value = attemptEval(arg.text)
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
def resolveDocumentInheritances(el):
    """In place resolution of document inheritances.  Doesn't return anything."""
    abstractMembers = Search.parental_tree_search(el, '.getchildren()', '.tag==\'InheritsFrom\'')
    for subel in abstractMembers:
        subel = resolveInheritance(subel)
def resolveInheritance(el):
    """In place resolution of inheritence.  Doesn't return anything."""
    parentClass = el.find('InheritsFrom')
    if parentClass != None:
        parentTree = loadConfigFile(parentClass.text)
        if parentTree == None:
            main_log.warn('Inheritance Failed.  ' + parentClass.text + 'does not exist')
            main_log.error('Inheritance Failed.  ' + parentClass.text + 'does not exist')
            return el
        el = compositeXMLTrees(parentTree, el) 
        el.remove(parentClass) #get rid of the inheritance flag
