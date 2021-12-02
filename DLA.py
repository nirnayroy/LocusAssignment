'''

Diffusion Limited Aggregation(DLA)

author: Nirnay Roy(@nirnayroy)

Reference: http://paulbourke.net/fractals/dla/

'''
import numpy as np
from numpy import random
import matplotlib.pyplot as plt


class Particle:

    def __init__(self, pos: tuple, stickiness: float):
        '''
        Initialize a particle on the board

        pos: a tuple with particle position as (x, y)
        '''
        self.pos = pos
        self.stickiness = stickiness
        self.stuck = False


class Matrix:

    def __init__(self, M: int):
        '''
        Initialize Matrix for DLA

        input:
            M: size of the 2d matrix
        '''

        self.M = M
        self.array = np.zeros((M, M))

    def aggregate(self, nParticles: int):
        '''
        Executes DLA by sticking a particle in the middle and
        aggregating particles that walk randomly and stick when a neighbouring
        cell has stuck particle

        nParticles: no. of particles to aggregate
        '''
        firstParticle = self.spawnParticle((int(self.M/2), int(self.M/2)),
                                           stickiness=1)
        self.stickParticle(firstParticle)
        for i in range(nParticles):
            self.spawnAndWalkParticle()

    def spawnAndWalkParticle(self):
        '''
        Spawns a particle on the edge and takes random steps
        until it sticks
        '''
        # get coordinates of the edge
        x = random.choice([0, self.M-1])
        y = random.randint(0, self.M)
        if random.random() > 0.5:
            x, y = y, x

        # spawn a particle and check if it has stuck neighbours
        particle = self.spawnParticle((x, y), stickiness=1)
        self.checkNeighboursAndStick(particle)

        # walk randomly until the particle sticks
        while not particle.stuck:
            particle = self.moveParticle(particle)
            self.checkNeighboursAndStick(particle)
        return

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
        self.array[particle.pos[0], particle.pos[1]] = 1
        return particle

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

    def stickParticle(self, particle: Particle):
        '''
        Stick a particle to a given position

        input:
            particle: a Particle instance
        '''
        particle.stuck = True

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

    def checkNeighboursAndStick(self, particle: Particle):#
        '''
        check if neighbouring cells have a stuck particle and stick if
        a random float is less than the stickiness of the particle.

        input:
            particle: an object of particle class
        '''
        if len(self.getNeighbours(particle)) < 8 and random.random() < particle.stickiness:
            self.stickParticle(particle)

    def showImage(self):
        '''
        show image of the matrix mapping 0 to white and 1 to black
        '''
        plt.imshow(self.array, cmap='Greys', interpolation='nearest')
        plt.show()




def main():
    matrix = Matrix(M=251)
    matrix.aggregate(nParticles=15000)
    matrix.showImage()


if __name__ == '__main__':
    main()
