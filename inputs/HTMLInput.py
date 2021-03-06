from operationscore.Input import *
import urllib, re

"""
HTML Input, which takes 2 arguments:
- 'Src': a URL to a web page, and
- 'Regex': a Regex to parse data out of the web page.
The input parses the source code of the web page according to the regex, and processes the parsed regex groups.
"""
class HTMLInput(Input):
    def inputInit(self):
        self.src = self.argDict['Src']
        self.regex = self.argDict['Regex']
        
    def getHTML(self):
        self.sock = urllib.urlopen(self.src);
        self.html = self.sock.read()
        self.sock.close()

    def sensingLoop(self):
        try:
            self.getHTML()
            self.dataDict = {}

            pattern = re.compile(self.regex)
            matchObj = pattern.search(self.html)        
            dataList = matchObj.groups()
            self.dataDict['WindSpeed'] = dataList[0]
            self.dataDict['WindDir'] = dataList[1]
            #print self.dataDict
            self.respond(self.dataDict)
        except:
            pass
	
