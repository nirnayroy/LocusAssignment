'''

Diffusion Limited Aggregation(DLA)

author: Nirnay Roy(@nirnayroy)

Reference: http://paulbourke.net/fractals/dla/

'''
import numpy as np
from numpy import random
import matplotlib.pyplot as plt


N_POSSIBLE_NEIGHBORS = 8


class Particle:

    def __init__(self, pos: tuple, stickiness: float):
        '''
        Initialize a particle on the board

        Inout:
            pos: a tuple with particle position as (x, y)
            stickiness: the stickiness of the particle
        '''
        self.pos = pos
        self.stickiness = stickiness
        self.stuck = False

    def stick(self):
        '''
        Sticks a particle if a random float(betwn 0 & 1) is less than
        the stickiness of the particle.
        '''
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

    def seed_matrix(self, type='central_attractor'):
        '''
        Sticks the particles that exist before the aggregation process

        input:
            type: pattern of inital stuck particles currently implemented for
                  the 'central attractor' type
        '''
        firstParticle = self.spawn_particle((int(self.M/2), int(self.M/2)),
                                            stickiness=1)
        firstParticle.stick()

    def aggregate(self, n_particles: int, stickiness: float):
        '''
        Executes DLA by sticking a particle in the middle and
        aggregating particles that walk randomly and stick when a neighbouring
        cell has stuck particle

        input:
            n_particles: no. of particles to aggregate
            stickiness: stickiness of each particle
        '''
        print('Start!!!')
        for i in range(n_particles):
            particle = self.spawn_particle(pos=self.random_edge_position(),
                                           stickiness=stickiness)
            self.take_steps_until_stuck(particle)
            print('particle no.', i)
        print('End')

    def random_edge_position(self):
        '''
        returns a random tuple with positions from the edge of the matrix

        Output:
            (x, y): a random position from the edge of the tuple
        '''
        # get coordinates of the edge
        x = random.choice([0, self.M-1])
        y = random.randint(0, self.M)
        if random.random() > 0.5:
            x, y = y, x
        return (x, y)

    def spawn_particle(self, pos: tuple, stickiness: float):
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
        self.stick_if_neighbor_found(particle)
        return particle

    def take_steps_until_stuck(self, particle: Particle):
        '''
        Particle takes random steps
        until it sticks
        '''
        # walk randomly until the particle sticks
        while not particle.stuck:
            particle = self.random_step(particle)
            self.stick_if_neighbor_found(particle)
        return

    def random_step(self, particle: Particle):
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

        neighbors = self.get_empty_neighbors(particle)

        (x, y) = neighbors[random.randint(len(neighbors))]
        self.array[x, y] = 1
        particle.pos = (x, y)
        return particle

    def stick_if_neighbor_found(self, particle: Particle):
        '''
        check if neighbouring cells have a stuck particle and stick if
        a random float is less than the stickiness of the particle.

        input:
            particle: an object of particle class
        '''
        if len(self.get_empty_neighbors(particle)) < N_POSSIBLE_NEIGHBORS:
            particle.stick()

    def get_empty_neighbors(self, particle: Particle):
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
                if not(i == 0 and j == 0) and \
                   self.array[(x+i) % self.M, (y+j) % self.M] == 0:
                    neighbors.append(((x+i) % self.M, (y+j) % self.M))
        return neighbors


class Simulator:
    def __init__(self, M=51, n_particles=15, stickiness=1):
        '''
        Initialize a simulator class

        input:
            M: size of the matrix
            n_particles: no. of particles in the matrix
        '''
        self.M = M
        self.n_particles = n_particles
        self.stickiness = stickiness

    def run(self):
        '''
        runs the simulation
        '''
        matrix = Matrix(self.M)
        matrix.seed_matrix()
        matrix.aggregate(self.n_particles, self.stickiness)
        return matrix.array

    def show_image(self, matrix: Matrix):
        '''
        show image of the matrix mapping 0 to white and 1 to black

        input:
            matrix: A Matrix instance
        '''
        plt.imshow(matrix.array, cmap='Greys', interpolation='nearest')
        filename = f'M_{matrix.M}_NP_{self.n_particles}\
                     _ST_{self.stickiness}.png'
        plt.savefig(filename)

    def save_npy(self, matrix):
        '''
        saves a numpy array in the form of an .npy file

        input:
            matrix: A Matrix instance
        '''
        filename = f'M_{matrix.M}_NP_{self.n_particles}_ST_{self.stickiness}'
        np.save(filename, matrix.array)


def main():
    simulation = Simulator(M=251, n_particles=15000, stickiness=1)
    simulation.run()


if __name__ == '__main__':
    main()
