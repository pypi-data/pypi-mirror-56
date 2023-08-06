import logging as logger

import math
from bitstring import BitArray, Bits
import random


class GeneticAlgorithm:

    MAX_MUTATION_RANGE = 10000

    def __init__(self, encoding_length, init_population_size,mutation_rate):
        self.encoding_length = encoding_length
        self.max_encodings = math.factorial(encoding_length)
        self.init_population_size = init_population_size
        self.parent_selection_ratio = .5
        self.mutation_rate = mutation_rate

        logger.info("""
            Initial genetic algorithm configuration: 
            encoding length: {} 
            maximum encodings: {} 
            initial population size: {}
        """.format(self.encoding_length,self.max_encodings,self.init_population_size))

    def optimize(self, fitness_function, fitness_threshold):
        logger.info("Optimizing with genetic algorithm...")

        population = self.initialize_population()

        evolved_population = self.evolve_population(population,fitness_function)

        return self.find_best_fit_encodings(evolved_population,fitness_function,fitness_threshold)

    def evolve_population(self, population,fitness_function):
        logger.info("Evolving population...")

        population_local = population.copy()

        converged = False
        while not converged:
            new_population = set()
            for i in range(len(population_local)):
                parent1 = self.select_encoding(population_local,fitness_function)
                parent2 = self.select_encoding(population_local,fitness_function)
                child = self.reproduce(parent1, parent2)
                child = self.potentially_mutate(child)
                new_population.add(child)
            population_size = len(population_local)
            population_local.union(new_population)
            converged = population_size == len(population_local)
        return population_local

    def select_encoding(self,population,fitness_function):
        best_encoding = None
        best_fitness = 0
        for i in range(math.ceil(len(population) * self.parent_selection_ratio)):
            encoding = random.choice(tuple(population))
            fitness = fitness_function(encoding)
            logger.debug("Selected encoding: {} encoding fitness: {}".format(encoding,fitness))
            if fitness >= best_fitness:
                best_encoding = encoding
                best_fitness = fitness
        return best_encoding

    def initialize_population(self):
        logger.info("Initializing randomized population....")
        population = set()
        for i in range(self.init_population_size):
            population.add(self.generate_random_encoding())

        return population

    def generate_random_encoding(self):
        encoding = '0b'
        for i in range(self.encoding_length):
            encoding += str(random.randint(0, 1))
        return Bits(encoding)


    def find_best_fit_encodings(self,population,fitness_function,fitness_threshold):
        best_encodings = []
        max_fitness = 0
        best_encoding = None
        for encoding in population:
            fitness = fitness_function(encoding)
            if fitness >= fitness_threshold:
                best_encodings.append(encoding)
            if fitness >= max_fitness:
                best_encoding = encoding
                max_fitness = fitness

        if not best_encodings:
            best_encodings.append(encoding)

        return best_encodings

    def potentially_mutate(self,encoding):
        if self.mutation_occurs():
            return self.mutate(encoding)
        else:
            return encoding

    def mutation_occurs(self):
        random_number = random.randint(1, self.MAX_MUTATION_RANGE)
        return random_number >= (self.MAX_MUTATION_RANGE * self.mutation_rate)

    def mutate(self,encoding):
        mutated_encoding = BitArray(encoding)

        selected_bit = random.randint(0, self.encoding_length - 1)
        selected_value = random.randint(0,1)

        mutated_encoding[selected_bit] = selected_value

        return Bits(bin=mutated_encoding.bin)

    def reproduce(self,parent1, parent2):
        child = None

        crossover_point = random.randint(1,self.encoding_length - 1)

        parent1_genes = BitArray(parent1)[:crossover_point]
        parent2_genes = BitArray(parent2)[-(self.encoding_length - crossover_point):]

        child = parent1_genes + parent2_genes

        return Bits(bin=child.bin)




