import unittest
import pandas as pd
import logging as logger
import sys

from machinelearning.stats.pandas.statistics_calculator import StatisticsCalculator, \
    CategoricalStatisticsCalculator

logger.basicConfig(level=logger.INFO, format="%(asctime)s %(levelname)s - %(message)s",
            handlers=[
            logger.FileHandler("{0}/{1}.log".format(".", "rgf")),
            logger.StreamHandler(sys.stdout)
        ])


class TestStatsCalculator(unittest.TestCase):
    TARGET = "class"

    iris_dataset = pd.read_csv("../datasets/iris.csv")
    election_dataset = pd.read_csv("../datasets/house-votes-84.csv")

    def test_entropy(self):
        stats = StatisticsCalculator()
        stats.entropy(stats.get_conditional_probabilities(self.iris_dataset, self.TARGET))

    def test_categorical_conditional_probabilities(self):
        cat_stats = CategoricalStatisticsCalculator()
        probabilities = cat_stats.get_conditional_probabilities(self.election_dataset, self.election_dataset["handicapped-infants"] == "n", self.TARGET)
        print(probabilities)

    def test_categorical_attribute_entropy_with_target(self):
        cat_stats = CategoricalStatisticsCalculator()
        logger.info("Attribute entropy: " + cat_stats.attribute_entropy(self.election_dataset,"handicapped-infants",self.TARGET))

    def test_info_gain(self):
        cat_stats = CategoricalStatisticsCalculator()
        info_gain = cat_stats.info_gain(cat_stats.attribute_entropy(self.election_dataset,self.TARGET),cat_stats.attribute_entropy(self.election_dataset,"handicapped-infants",self.TARGET))
        logger.info("Info gain: " + str(info_gain))


if __name__ == '__main__':
    unittest.main()
