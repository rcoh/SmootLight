from xml.etree.ElementTree import ElementTree
classArgsMem = {}
CONFIG_PATH = 'config/'
def loadParamRequirementDict(className):
    if not className in classArgsMem: #WOO CACHING
        classArgsMem[className] = fileToDict(CONFIG_PATH + className) 
    return classArgsMem[className]
def loadConfigFile(fileName): #TODO: error handling etc.
    #try:
        fileName = CONFIG_PATH + fileName
        if '.params' in fileName:
            return fileToDict(fileName)
        if '.xml' in fileName:
            config = ElementTree()
            config.parse(fileName)
            return config
    #except:
        return None
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
