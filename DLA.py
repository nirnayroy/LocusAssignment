'''

Diffusion Limited Aggregation(DLA)

author: Nirnay Roy(@nirnayroy)

Reference: http://paulbourke.net/fractals/dla/

'''
import numpy as np
from numpy import random
import matplotlib.pyplot as plt

POSSIBLE_DIRECTIONS = 8

class Particle:

    def __init__(self, pos: tuple, stickiness: float):
        '''
        Initialize a particle on the board

        pos: a tuple with particle position as (x, y)
        '''
        self.pos = pos
        self.stickiness = stickiness
        self.stuck = False

    def stick(self):
        if random.random() < self.stickiness:
            self.stuck = True


class Matrix:

    def __init__(self, M: int):
        '''
        Initialize Matrix for DLA

        input:
            M: size of the 2d matrix
        '''

        self.M = M
        self.array = np.zeros((M, M))

    def seedMatrix(self, type= 'central_attractor'):
        firstParticle = self.spawnParticle((int(self.M/2), int(self.M/2)),
                                           stickiness=1)
        firstParticle.stick()

    def aggregate(self, nParticles: int, stickiness: float):
        '''
        Executes DLA by sticking a particle in the middle and
        aggregating particles that walk randomly and stick when a neighbouring
        cell has stuck particle

        nParticles: no. of particles to aggregate
        '''
        print('Start!!!')
        for i in range(nParticles):
            particle = self.spawnParticle(pos=self.posAtEdges(), stickiness = stickiness)
            self.walkParticle(particle)
            print('particle no.', i)
        print('End')

    def posAtEdges(self):
        # get coordinates of the edge
        x = random.choice([0, self.M-1])
        y = random.randint(0, self.M)
        if random.random() > 0.5:
            x, y = y, x
        return (x, y)

    def spawnParticle(self, pos: tuple, stickiness: float):
        '''
        Initializes a particle at the given position

        input:
            pos: position to initialize particle
            stickiness: stickiness of the particle

        output:
            particle: a Particle instance
        '''
        particle = Particle(pos, stickiness)
        self.array[pos[0], pos[1]] = 1
        # spawn a particle and check if it has stuck neighbours
        self.checkNeighboursAndStick(particle)
        return particle

    def walkParticle(self, particle: Particle):
        '''
        Particle takes random steps
        until it sticks
        '''
        # walk randomly until the particle sticks
        while not particle.stuck:
            particle = self.moveParticle(particle)
            self.checkNeighboursAndStick(particle)
        return

    def moveParticle(self, particle: Particle):
        '''
        moves a particle from its position to a randomly selected neighbouring
        position

        input:
            particle: a Particle instance

        output:
            particle: Particle instance with new postion
        '''
        x, y = particle.pos
        self.array[x, y] = 0

        neighbors = self.getNeighbours(particle)

        (x, y) = neighbors[random.randint(len(neighbors))]
        self.array[x, y] = 1
        particle.pos = (x, y)
        return particle

    def checkNeighboursAndStick(self, particle: Particle):#
        '''
        check if neighbouring cells have a stuck particle and stick if
        a random float is less than the stickiness of the particle.

        input:
            particle: an object of particle class
        '''
        if len(self.getNeighbours(particle)) < POSSIBLE_DIRECTIONS:
            particle.stick()

    def getNeighbours(self, particle: Particle):
        '''
        returns a list of positions that a particle can move to next
        excluding the positions of the stuck particle

        input:
            particle: a particle object

        output:
            neighbors: a list containing the position of the neighbors
        '''
        x, y = particle.pos
        move = [-1, 0, 1]

        neighbors = []
        for i in move:
            for j in move:
                if not(i == 0 and j == 0) and self.array[(x+i)%self.M, (y+j)%self.M] == 0:
                    neighbors.append(((x+i)%self.M, (y+j)%self.M))
        return neighbors


class Simulator:
    def __init__(self, M=51, nParticles=15, stickiness = 1):
        '''
        Initialize a simulator class

        input:
            M: size of the matrix
            nParticles: no. of particles in the matrix
        '''
        self.M = M
        self.nParticles = nParticles
        self.stickiness = stickiness

    def run(self):
        '''
        runs the simulation
        '''
        matrix = Matrix(self.M)
        matrix.seedMatrix()
        matrix.aggregate(self.nParticles, self.stickiness)
        return matrix.array

    def showImage(self, matrix: Matrix):
        '''
        show image of the matrix mapping 0 to white and 1 to black

        input:
            matrix: A Matrix instance
        '''
        plt.imshow(matrix.array, cmap='Greys', interpolation='nearest')
        filename = f'M_{matrix.M}_NP_{self.nParticles}_ST_{self.stickiness}.png'
        plt.savefig(filename)
    
    def saveNpy(self, matrix):
        '''
        saves a numpy array in the form of an .npy file

        input:
            matrix: A Matrix instance
        '''
        filename = f'M_{matrix.M}_NP_{self.nParticles}_ST_{self.stickiness}'
        np.save(filename, matrix.array)

def main():
    simulation = Simulator(M=251, nParticles=15000, stickiness = 1)
    simulation.run()

if __name__ == '__main__':
    main()
