import unittest
import sys
import logging as logger
import random

from bitstring import BitArray

from machinelearning.optimization.genetic_algorithm import GeneticAlgorithm


logger.basicConfig(level=logger.INFO, format="%(asctime)s %(levelname)s - %(message)s",
            handlers=[
            logger.FileHandler("{0}/{1}.log".format(".", "rgf")),
            logger.StreamHandler(sys.stdout)
        ])


class TestGeneticAlgorithm(unittest.TestCase):

    def test_random_encoding_generation(self):
        ga = GeneticAlgorithm(5,2,.10)
        logger.info(ga.generate_random_encoding())

    def test_random_initial_population(self):
        ga = GeneticAlgorithm(20,1000,.10)
        population = ga.initialize_population()
        logger.info(population)

    def test_reproduce(self):
        ga = GeneticAlgorithm(5,2,.10)
        child = ga.reproduce(BitArray('0b10101'),BitArray('0b11000'))
        logger.info("Child: {}".format(child.bin))

    def test_encoding_selection(self):
        ga = GeneticAlgorithm(6, 3,.10)
        parent = ga.select_encoding(ga.initialize_population(),lambda encoding: random.randint(1, 100))
        logger.info(parent.bin)

    def test_find_best_fit(self):
        ga = GeneticAlgorithm(6, 3,.20)
        best_fit = ga.find_best_fit_encodings(ga.initialize_population(), self.randomize_fitness,70)
        logger.info(best_fit)
        assert len(best_fit) > 0

    def test_mutation(self):
        ga = GeneticAlgorithm(6, 3,.5)
        random_encoding = ga.generate_random_encoding()
        mutated_encoding = ga.mutate(random_encoding)
        logger.info("Initial encoding: {} mutated encoding: {}".format(random_encoding,mutated_encoding))

    def test_potentially_mutate(self):
        ga = GeneticAlgorithm(6, 3,.20)
        random_encoding = ga.generate_random_encoding()
        mutated_encoding = ga.potentially_mutate(random_encoding)
        logger.info("Initial encoding: {} mutated encoding: {}".format(random_encoding,mutated_encoding))
        if random_encoding != mutated_encoding:
            logger.info("Mutation occurred. ")


    def test_optimize(self):
        ga = GeneticAlgorithm(6, 3, .20)
        optimized_encodings = ga.optimize(self.randomize_fitness,70)
        logger.info(optimized_encodings)

    def randomize_fitness(self,encoding):
        return random.randint(1, 100)
