from operationscore.Behavior import *

class FadeOut(Behavior):
    """FadeOut is a transition behavior. It takes a python equation in t,
    <tEquation> which takes integer values in frames and turns them into
    color coefficients 0 to 1, and a timeout in seconds <TimeOut>, after
    which the color coefficient is always 0. Color coefficents are applied to
    the colors in all incoming inputs. The default equation is 
    1-t/(TimeOut*30.0) """

    def behaviorInit (self):
        state = {}
        if 'tEquation' in self.argDict:
            state['tEquation'] = self['tEquation']
        else:
            state['tEquation'] = '1-t/'+ str(self['TimeOut']*30.0)
        state['t'] = 0
        state['TimeOut'] = self['TimeOut'] * 30
        return [state]

    def processResponse (self, inputs, states):
        state = states[0]
        t = state['t']
        if t < state['TimeOut']:
            coeff = eval(state['tEquation'])
        else:
            coeff = 0
        state['t'] += 1

        outputs = []
        for inp in inputs:
            out = inp
            out['PixelEvent'].scale = coeff
            outputs.append(out)
        return (outputs, [state])
