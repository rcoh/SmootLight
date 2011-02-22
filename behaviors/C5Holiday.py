from operationscore.Behavior import *
import util.TimeOps as time
class C5Holiday(Behavior):
    def processResponse(self, sensors, recurs):
        ret = []
        logo = {'Location':'True@cl.all', 'Color':(255,0,0)}
        conner = {'Location':'True@c5.con', 'Color':(255,255,255)}
        five = {'Location':'True@c5.five', 'Color':(0,0,255)}
        clist = [(255,0,0),(255,255,255), (0,0,255)]
        borderColor = clist[int(time.time()/1000) % 3]
        welcomeColor = clist[(int(time.time()/1000)+1) % 3]
        borders = {'Location':'True@ts.all ls.all rs.all bs.all', 'Color':borderColor}
        welcome = {'Location':'True@wt.all', 'Color':welcomeColor}
        
        ret.append(logo)
        ret.append(conner)
        ret.append(five)
        ret.append(borders)
        ret.append(welcome)
        return (ret,[])
        
