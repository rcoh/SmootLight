from operationscore.Behavior import *
class Bar(Behavior):

    """Generalization of the Vertical Bar Behavior, takes Slope for an
    args and then will draw a line with that slope through every point
    given to Bar."""

    def behaviorInit (self):
        
        slope = self['Slope']

        if slope == None:
            self.cond = '{x} == '
            self.cons = (1, 0)
        elif slope > 1 or slope < -1:
            self.cond = 'int({x} + ' + str(slope) + ' * {y}) == '
            self.cons = (1, slope)
        elif slope != 0:
            self.cond = 'int({y} + ' + str(1/slope) + ' * {x}) == '
            self.cons = (1/slope, 1)
        else:
            self.cond = '{y} == '
            self.cons = (0, 1)

        print self.cond
        print self.cons

    def processResponse(self, inputs, recurs):
        ret = []
        inputs = list(inputs)
        for inputset in inputs:
            inputset = dict(inputset) 
            if 'xLoc' not in inputset:
                inputset['xLoc'] = inputset['Location'][0]
            if 'yLoc' not in inputset:
                inputset['yLoc'] = inputset['Location'][1]
            xLoc = inputset['xLoc']
            yLoc = inputset['yLoc']

            condition = self.cond + str(self.cons[0]*xLoc + self.cons[1]*yLoc)

            if self['Combine']:
                inputset['Location'] += ',' + condition
            else:
                inputset['Location'] = condition 

            ret.append(inputset)
        return (ret, [])

