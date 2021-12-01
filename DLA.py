'''

Diffusion Limited Aggregation(DLA)

author: Nirnay Roy(@nirnayroy)

Reference: http://paulbourke.net/fractals/dla/

'''
import numpy as np
from numpy import random
import matplotlib.pyplot as plt


class Matrix:

    def __init__(self, M: int):
        '''
        Initialize Matrix for DLA

        M: size of the 2d matrix
        '''

        self.M = M
        self.array = np.zeros((M, M))
        self.stuckParticles = []

    class Particle:

        def __init__(self, pos: tuple, stickiness: float):
            '''
            Initialize a particle on the board

            pos: a tuple with particle position as (x, y)
            '''
            self.pos = pos
            self.stickiness = stickiness
            self.stuck = False

    def aggregate(self, nParticles):
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
        Initializes a particle at the given position and of gven stickiness

        input:
            pos: position to initialize particle
            stickiness: stickiness of the particle

        output:
            particle: a Particle instance
        '''
        particle = self.Particle(pos, stickiness)
        self.array[particle.pos[0], particle.pos[1]] = 1
        return particle

    def moveParticle(self, particle):
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

        for neighbor in neighbors:
            if neighbor in self.stuckParticles:
                neighbors.remove(neighbor)

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
        self.stuckParticles.append(particle.pos)

    def getNeighbours(self, particle: Particle):
        '''
        returns a list of positions that a particle can move to next

        input:
            particle: a particle object

        output:
            neighbors: a list containing the position of the neighbors
        '''
        x, y = particle.pos

        def directionList(coordinate):
            '''
            checks whether a coordinate is on the boundary and returns a
            list contating the directions it can move

            input:
                coordinate: 1st or 2nd index in the position

            output:
                direction: list of the directions to move
            '''
            if coordinate == 0:
                direction = [0, 1]
            elif coordinate == self.M-1:
                direction = [-1, 0]
            else:
                direction = [-1, 0, 1]
            return direction

        dx, dy = directionList(x), directionList(y)

        neighbors = []
        for i in dx:
            for j in dy:
                if not(i == 0 and j == 0):
                    neighbors.append((x+i, y+j))
        return neighbors

    def checkNeighboursAndStick(self, particle):
        '''
        check if neighbouring cells have a stuck particle and stick if
        a random float is less than the stickiness of the particle.

        input:
            particle: an object of particle class
        '''
        for neighbor in self.getNeighbours(particle):
            if neighbor in self.stuckParticles \
               and random.random() < particle.stickiness:
                self.stickParticle(particle)
                break

    def showImage(self):
        '''
        show image of the matrix mapping 0 to white and 1 to black
        '''
        plt.imshow(self.array, cmap='Greys', interpolation='nearest')
        plt.show()


def main():
    matrix = Matrix(M=100)
    matrix.aggregate(nParticles=500)
    matrix.showImage()


if __name__ == '__main__':
    main()
