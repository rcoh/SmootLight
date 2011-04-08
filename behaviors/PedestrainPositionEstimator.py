##NOT STATELESS
"""Locations are only x, *not* tuples of (x,y) as in common in other locations
Units are in U/Second where U is whatever unit you use in your layouts -- generally inches
"""
class PedestrianPositionEstimator(Behavior):
    DETECTION_CERTAINTY = .99
    def updateLocations(self, locations,velocities, deltaT):
        """Returns a list of dict representing the new locations.
            Locations is dict of dicts: {PedestrianId: {Loc, Prob}}
            Velocities is a dict of dicts: {PedestrainId: {Vel, Prob}}
        """
        updatedLocations = {}
        for pedestrianId in locations:
            for location in locations[pedestrianId]:
                locProb = locations[pedestrianId][location]
                newPedDict = {}
                for velocity in velocities[pedestrianId]:
                    newProb = locProb*velocity[velocities]
                    newPedDict[int(location+velocity*deltaT)] = newProb*locProb 
                    """^quantization of location"""
                updatedLocations[pedestrianId] = newPedDict
        return updatedLocations

    def updateVelocities(self, velocities, preLocations, postLocations, deltaT):
        """
        Given: old velocities, old locations, new locations, deltaT:
            Updates the velocity dict using incorporateVelObs
            The newVel is (w_Avg preLoc_i - w_Avg postLoc_i) / deltaT for i in preLoc 
        """
        newVelocities = {}
        for pedestrianId in preLocations:
            preAvgLoc = self.weightedAverage(preLocations[pedestrianId])
            postAvgLoc = self.weightedAverage(postLocations[pedestrianId])
            newVel = (postAvgLoc-preAvgLoc)/deltaT
            newVelocities[pedestrianId] = self.incorporateVelObs(velocities[pedestrianId], newVel)
        
        return newVelocities

    def incorporateVelObs(self, velocityDict, newVel):
        raise NotImplementedError

    def incorporateObservation(self, observationMatrix, locations):
        """In place.  
        Observation is a location -- an int. 
        Locations is {PedId:{Loc, Prob}}
        Incorporates observations with Bayesian Inference:
        P(H|E)=P(E|H)*P(H) / P(E)
        P(E) = Sum [ P(E | H_i)*P(H_i)
        We then take P(H)*(1-P(E|H))+P(H|E)*P(E|H)
        """
        for pedestrianId in locations:
            if observation in 
            
