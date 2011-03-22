from operationscore.PixelMapper import *
import util.Geo as Geo
from numpy import exp, square, array

class GaussianMapper(PixelMapper):
    """GaussianMapper is a PixelMapper which weights pixels around an event proportional to a
    gaussian surface.  Specify:
    <Height> -- The height of the gaussian surface
    <Width> -- The width of the gaussian surface
    <MinWeight> -- the minimum weight event that can be returned
    <CutoffDist> -- the maximum radius considered
    """
    def mappingFunction(self, loc, screen):
        h, w, d = self.Height, self.Width, self.CutoffDist
        temp = screen.tree.query(loc, k=None, distance_upper_bound=d)
        dists, indices = array(temp[0]), array(temp[1])
        weights = h * exp(-square(dists/w)/2)
        valid = weights > self.MinWeight
        return zip(indices[valid], weights[valid])
