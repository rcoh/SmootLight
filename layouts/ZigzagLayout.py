from operationscore.PixelAssembler import *
import pdb
#Slightly more complex layout class that makes a zig-Zag Led Pattern
#Inheriting classes must specify zigLength, the length in lights of a of a zig
#and zig Axis, the direction of the long X axis (X or Y).
#EG: zig length = 4, zig Axis = X would give:
# X-X-X-X
#       |
# X-X-X-X
# |
# X-X-X-X etc.
class ZigzagLayout(PixelAssembler):
    def initLayout(self):
        if not 'zigLength' in self.argDict:
            raise Exception('zigLength must be defined in argDict') 
        if not 'zigAxis' in self.argDict:
            raise Exception('zigAxis must be defined in argDict')
        if not 'xDirection' in self.argDict:
            self.argDict['xDirection'] = 1 #right
        if not 'yDirection' in self.argDict:
            self.argDict['yDirection'] = 1 #down
    def layoutFunc(self, lastLocation):
        if not 'buildQueue' in self.argDict:
            self.argDict['buildQueue'] = self.argDict['zigLength']
        
        newLoc = list(lastLocation) 
        if self.argDict['buildQueue'] > 1:
            if self.argDict['zigAxis'] == 'X':
                newLoc[0] += self.argDict['spacing'] * self.argDict['xDirection']
            else:
                newLoc[1] += self.argDict['spacing'] * self.argDict['yDirection']
            self.argDict['buildQueue'] -= 1
        else:
            self.argDict['buildQueue'] = self.argDict['zigLength']
            if self.argDict['zigAxis'] == 'X':
                newLoc[1] += self.argDict['spacing'] * self.argDict['yDirection']
            else:
                newLoc[0] += self.argDict['spacing'] * self.argDict['xDirection']
            if self.argDict['zigAxis'] == 'X':
                self.argDict['xDirection'] *= -1
            else:
                self.argDict['yDirection'] *= -1
        return newLoc 

   
