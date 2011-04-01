"""
Layout Generator.

Current Layout is set according to '03-22-11-pixel-strips-numbering-convention.pdf':
*12 SpacingUnit = 1 Inch
"""

# ---------------
# FUNCTIONS
# ---------------
def makeSection(id, numPixels, pixelSpacing, numRows, rowSpacing, numStrips):
    sectionInfo = {'Id': id, 'NumPixels': numPixels, 'PixelSpacing': pixelSpacing, \
                   'NumRows': numRows, 'RowSpacing': rowSpacing, 'NumStrips': numStrips}
    return sectionInfo

def generateStripXml(section):
    # Generate the strip xml like the following example
    """
    <PixelStrip>
    <Class>layouts.LineLayout</Class>
    <Args>
        <pixelToPixelSpacing>4</pixelToPixelSpacing>
        <step>(4,0)</step> 
        <numPixels>50</numPixels>
    </Args>
    </PixelStrip>
    """
    
    stripStr = ''
    stripStr += '<PixelStrip>\n' + \
                tab(1) + '<Class>layouts.LineLayout</Class>\n' + \
                tab(1) + '<Args OverrideBehavior="Merge">\n' + \
                tab(2) + toXmlArgNode('pixelToPixelSpacing', section['PixelSpacing']) + '\n' + \
                tab(2) + toXmlArgNode( 'step', (section['PixelSpacing'], 0) ) + '\n' + \
                tab(2) + toXmlArgNode('numPixels', section['NumPixels']) + '\n' + \
                tab(1) + '</Args>\n' + \
                '</PixelStrip>'
    #print stripStr
    return stripStr

def generateLayoutXml(sections, reverseStrips, rowToDiffuser):
    # Generate layout xml like the following
    """
    <PixelConfiguration>
    <PixelStrip Id="strip1.1" originLocation="(0,0)" Reverse="True">
        <InheritsFrom>layouts/50PixelStrip.xml</InheritsFrom>
    </PixelStrip>
    <PixelStrip Id="strip1.2" originLocation="(200,0)">
        <InheritsFrom>layouts/50PixelStrip.xml</InheritsFrom>
    </PixelStrip>
    ...
    </PixelConfiguration>
    """
    layoutStr = '<PixelConfiguration>\n'
    idCounter = 1
    locCounter = [0,0]
    
    for section in sections:
        layoutStr += genSectionLayoutStr(section, idCounter, locCounter, reverseStrips, rowToDiffuser) + '\n'
        idCounter += section['NumRows'] * section['NumStrips']
    
    layoutStr += '</PixelConfiguration>'
    print layoutStr
    return layoutStr

def genSectionLayoutStr(section, idCounter, locCounter, reverseStrips, rowToDiffuser):
    """
    -- SECTION INFO
    'Id': id, 'NumPixels': numPixels, 'PixelSpacing': pixelSpacing,
    'NumRows': numRows, 'RowSpacing': rowSpacing, 'NumStrips': numStrips
    """
    sectionLayoutStr = ''
    secTotalStripNum = section['NumStrips'] * section['NumRows']

    rowCounter = 1
    xLoc = locCounter[0]
    yLoc = locCounter[1]
    for i in range(idCounter, idCounter + secTotalStripNum):
        
        # Arg:Id
        sectionLayoutStr += tab(1)+'<PixelStrip ' + \
                            'Id="'+str(i) + '"'

        # Arg:diffuser
        sectionLayoutStr += ' diffuser="' + str(rowToDiffuser[rowCounter]) + '"'

        # Arg:originLocation
        sectionLayoutStr += ' originLocation="('+ str(xLoc)+','+str(yLoc) +')"'
        if rowCounter == section['NumRows']:
            locCounter[0] += section['PixelSpacing'] * section['NumPixels']
            locCounter[1] = 0
            xLoc = locCounter[0]
            yLoc = locCounter[1]
            rowCounter = 1
        else:
            yLoc = (i%section['NumRows']) * section['RowSpacing']
            rowCounter += 1            
        
        # Arg:Reverse
        if i in reverseStrips:
            sectionLayoutStr += ' Reverse="True"'


        sectionLayoutStr += '>\n'
        sectionLayoutStr += tab(2)+'<InheritsFrom>layouts/10kLayout/' + section['Id']+'Strip.xml' + '</InheritsFrom>\n'
        sectionLayoutStr += tab(1)+'</PixelStrip>\n'

    #print sectionLayoutStr
    return sectionLayoutStr


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
# LAYOUT INFO
# ---------------
"""
makeSection(id, numPixels, pixelSpacing, numRows, rowSpacing, numStrips):
"""
sections = []
# 10k layout info

sections.append( makeSection('Section1', 50, 4, 4, 48, 23) )
sections.append( makeSection('Section2', 50, 9, 4, 108, 8) )
sections.append( makeSection('Section3', 50, 10, 4, 120, 10) )
sections.append( makeSection('Section4', 50, 12, 4, 144, 7) )

# smaller test
"""
sections.append( makeSection('Section1', 20, 4, 4, 48, 1) )
sections.append( makeSection('Section2', 20, 9, 4, 48, 1) )
sections.append( makeSection('Section3', 20, 10, 4, 48, 1) )
sections.append( makeSection('Section4', 20, 12, 4, 48, 1) )
"""
#print sections

reverseStrips = []
reverseStrips += range(13, 17) +\
                 range(25, 29) +\
                 range(37, 45) +\
                 range(53, 57) +\
                 range(65, 77) +\
                 range(81, 85) +\
                 range(89, 93) +\
                 range(97, 101) +\
                 range(113, 117) +\
                 range(121, 125) +\
                 range(133, 137) +\
                 range(173, 177) +\
                 range(181, 185)
#print reverseStrips

rowToDiffuser = {1: '(0, -1)', 2: '(0, 1)', 3: '(0, -1)', 4: '(0, 1)'}


# ---------------
# GENERATION
# ---------------
dir = 'layouts/10kLayout/'

for section in sections:
    writeToFile( generateStripXml(section), dir + section['Id']+'Strip.xml' )

writeToFile( generateLayoutXml(sections, reverseStrips, rowToDiffuser), dir + '10kLayout.xml' )

