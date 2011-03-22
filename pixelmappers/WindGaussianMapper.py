from operationscore.PixelMapper import *
import util.Geo as Geo
import math
class WindGaussianMapper(PixelMapper):
    def mappingFunction(self, loc, screen):
        h, w, d = self.Height, self.Width, self.CutoffDist
        temp = screen.tree.query(loc, k=None, distance_upper_bound=d)
        dists, indices = array(temp[0]), array(temp[1])
        x, y = screen.locs[indices] - loc
        weights = h * exp(-square(x/w)/2) * square(exp(-y/w/.2))
        valid = weights > self.MinWeight
        return zip(indices[valid], weights[valid])
    
