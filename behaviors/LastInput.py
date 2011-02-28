from operationscore.Behavior import *
class LastInput(Behavior):
    def processResponse(self, sensors, recurs):
        if sensors:
            return (sensors, sensors)
        elif recurs:
            return (recurs, recurs)
        else:
            return ([],[])
