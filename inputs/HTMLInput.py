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
        self.getHTML()
        self.dataList = []
        
        pattern = re.compile(self.regex)
        matchObj = pattern.search(self.html)        
        self.dataList = matchObj.groups()

        self.respond(self.dataList)
	
