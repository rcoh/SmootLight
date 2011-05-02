"""
Renderer XML Generator for the 10K Layout.
"""

# ---------------
# FUNCTIONS
# ---------------
def generateRendererXml(className, ipSubnet, stripNum):
    """
<Renderer>
    <Class>renderers.IndoorRenderer</Class>
    <Args>
        <Id>indoorRenderer</Id>
        <!--Insert IP Addresses as necessary -->
        <PowerSupply>
            <IP>10.32.0.21</IP>
            <PortMapping>{'strip1':1, 'strip2':2}</PortMapping>
        </PowerSupply>
        <PowerSupply>
            <IP>10.32.0.22</IP>
            <PortMapping>{'strip3':1, 'strip4':2}</PortMapping>
        </PowerSupply>
    </Args>
</Renderer>
    """
    tabNum = 0
    xmlStr = ''
    
    xmlStr = '<Renderer>\n'
    xmlStr += tab(1) + '<Class>' + className  + '</Class>\n'
    xmlStr += tab(1) + '<Args>\n'
    xmlStr += tab(2) + toXmlArgNode('Id', '10kRenderer') + '\n'

    for i in range(1, stripNum/2+1):
        xmlStr += tab(2) + '<PowerSupply>\n'
        xmlStr += tab(3) + toXmlArgNode('IP', ipSubnet + str(i)) + '\n'
        xmlStr += tab(3) + '<PortMapping>{'
        xmlStr += '\'s' + str(2*i-1) + '\':' + str(1) + ', \'s' + str(2*i) + '\':' + str(2)
        xmlStr += '}</PortMapping>\n'
        xmlStr += tab(2) + '</PowerSupply>\n'
        
    xmlStr += tab(1) + '</Args>\n'
    xmlStr += '</Renderer>\n'

    print(xmlStr)
    return xmlStr

## -----------
## HELPERS
## -----------
def tab(num):
    return '  ' * num

def toXmlArgNode(argName, val):
    return '<'+str(argName)+'>' + str(val) + '</'+str(argName)+'>'
#print toXmlArgNode('someSample', 12321)

def writeToFile(xmlStr, destFile):
    f = open(destFile, 'w')
    f.write(xmlStr)
#writeToFile('testing', 'testfile.xml')


# ---------------
# GENERATION
# ---------------
dir = 'renderers/'

writeToFile( generateRendererXml('renderers.IndoorRenderer', '10.32.0.', 192), dir + '10kRenderer.xml' )

