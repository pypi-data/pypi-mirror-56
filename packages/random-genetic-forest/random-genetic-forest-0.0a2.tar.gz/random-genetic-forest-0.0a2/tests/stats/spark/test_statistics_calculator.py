import unittest
from pyspark.sql.context import SQLContext
from pyspark import SparkContext

from machinelearning.stats.spark.statistics_calculator import CategoricalStatisticsCalculator, ContinuousStatisticsCalculator


@unittest.skip
class TestStatisticsCalculator(unittest.TestCase):
    TARGET = "class"
    DATASET_DIR = "tests/datasets/"

    @classmethod
    def setUpClass(self):
        self.sc = SparkContext.getOrCreate()
        self.sqlContext = SQLContext(self.sc)
        self.iris_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema", "true").option(
            "mode", "DROPMALFORMED").load(self.DATASET_DIR + "iris.csv").rdd
        self.election_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema", "true").option(
            "mode", "DROPMALFORMED").load(self.DATASET_DIR + "house-votes-84.csv").rdd

    def test_entropy(self):
        probabilities = [.32,.45,.123,.43]
        print("Entropy: {} ",CategoricalStatisticsCalculator.entropy(probabilities))

    def test_categorical_conditional_probabilities(self):
        probabilities = CategoricalStatisticsCalculator.get_probabilities(self.iris_dataset.collect(),"class")
        print(probabilities)

    def test_categorical_attribute_entropy_with_target(self):
        print("Attribute entropy: " + str(CategoricalStatisticsCalculator.conditional_attribute_entropy(self.election_dataset.collect(),"water-project-cost-sharing","class")))

    def test_info_gain(self):
        examples = self.election_dataset.collect()
        attribute1_entropy = CategoricalStatisticsCalculator.attribute_entropy(examples,"water-project-cost-sharing")
        attribute2_entropy = CategoricalStatisticsCalculator.attribute_entropy(examples,"class")

        info_gain = CategoricalStatisticsCalculator.info_gain(attribute2_entropy,attribute1_entropy)

        print("Info gain: " + str(info_gain))

    def test_continuous_attribute_entropy(self):
        attribute_entropy = ContinuousStatisticsCalculator.attribute_entropy(self.iris_dataset.collect(),"petal_length","class",2.0)
        print("Attribute Entropy: " + str(attribute_entropy))


if __name__ == '__main__':
    unittest.main()