import competition
from geneticAlgorithm import *

class SO(Chromosome):
    def __init__(self):
        reason = competition.compete()
        
        self.runTime = reason["Armature Run Time"]
        self.speed = reason["Armature Speed"]
        self.Ek = reason["Armature Ek"]
        self.eta = reason["Armature Eta"]
    
    def fitness(self):
        return self.eta * self.speed

    @classmethod
    def random_instance(cls):
        pass

    def crossover(self, other):
        pass
        
    def mutate(self):
        pass

if __name__ == "__main__":
    pass