from operationscore.LayoutEngine import *
#Simple layout class that simply makes a line of LEDs
class LineLayout(LayoutEngine):
    def layoutFunc(self, lastLocation):
        return (lastLocation[0]+self.argDict['spacing'], lastLocation[1])
