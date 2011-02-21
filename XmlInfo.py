#!/usr/bin/python
import util.Config as config
import util.Search as search
import sys
"""XmlInfo.py is a module for quick introspection of XML Documents.  It will print all the Ids of
the components defined in an XML document and (if possible) their Doc strings.  Usage:
    python XmlInfo.py [fileName] [-b] [-i]
    Example:
    python XmlInfo.py config/C5Sign.xml

With no flags all components are printed.  With -b, behaviors are printed.  With -i, inputs are
printed.  (And both if both are specified)
"""
def loadFile(args):
    fileName = args[1]
    parentTags = []
    if '-b' in args:
        parentTags.append('BehaviorConfiguration')
    if '-i' in args:
        parentTags.append('InputConfiguration')
    if not parentTags: 
        parentTags = ['InputConfiguration', 'BehaviorConfiguration','PixelConfiguration',
                  'RendererConfiguration']
    confRoot = config.loadConfigFile(fileName).getroot()
    for tag in parentTags: 
        subTree = confRoot.find(tag)
        print tag + ':\n'
        nodesWithArgs = search.parental_tree_search(subTree,'.getchildren()', ".tag=='Args'")
        nodesWithDocs = search.parental_tree_search(subTree,'.getchildren()', ".tag=='Doc'")
        for obj in nodesWithArgs:
            args = obj.find('Args')
            cidEl = args.find('Id')
            docEl = args.find('Doc') or obj.find('Doc')
            classEl = obj.find('Class')
            cid = None
            doc = None
            className = None
            if cidEl != None:
                cid = cidEl.text
            if docEl != None and args != None:
                argDict = config.pullArgsFromItem(obj)
                doc = docEl.text
                try:
                    doc = doc % argDict
                except:
                    doc = docEl.text 
            if classEl != None:
                className = classEl.text
                print '\t%(id)s : %(class)s\n\t\t%(doc)s\n' % {'id':cid, 'doc':doc,
                                                                                'class':className}
if __name__ == "__main__":
    loadFile(sys.argv)
