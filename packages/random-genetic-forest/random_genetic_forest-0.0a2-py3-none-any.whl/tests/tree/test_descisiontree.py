import cProfile
import logging as logger
import sys
import unittest

from pyspark import SparkContext, SQLContext

from machinelearning.tree.decision_tree import DecisionTree
from machinelearning.tree.node.branch import Branch
from machinelearning.tree.node.treenode import TreeNode

logger.basicConfig(level=logger.INFO, format="%(asctime)s %(levelname)s - %(message)s",
                   handlers=[
                       logger.FileHandler("{0}/{1}.log".format(".", "rgf")),
                       logger.StreamHandler(sys.stdout)
                   ])


@unittest.skip
class TestDecisionTree(unittest.TestCase):
    TARGET = "class"
    DATASET_DIR = "tests/datasets/"

    @classmethod
    def setUpClass(self):
        self.sc = SparkContext.getOrCreate()
        self.sqlContext = SQLContext(self.sc)
        self.iris_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema",
                                                                                               "true").option(
            "mode",
            "DROPMALFORMED").load(self.DATASET_DIR + "iris.csv").rdd
        self.election_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema",
                                                                                                   "true").option(
            "mode", "DROPMALFORMED").load(self.DATASET_DIR + "house-votes-84.csv")

    def test_has_same_classification(self):
        logger.info("Performing has same classification tests...")
        dt = DecisionTree(self.iris_dataset, "class")
        assert not dt.has_same_classification(self.iris_dataset.collect())

    def test_decision_tree_iris(self):
        dt = DecisionTree(self.iris_dataset, "class")
        dataset = self.iris_dataset.collect()
        dt.train(dataset)

        sample = dataset[69]

        logger.info(
            "Predicted Class for Iris Dataset: " + str(dt.classify(dt.get_root(), sample)) + " Actual Class: " + str(
                dataset[69]["class"]))

    def test_plurality_value(self):
        logger.info("Testing plurality value...")

        dt = DecisionTree(self.iris_dataset, "class")
        classification = dt.plurality_value(self.iris_dataset.collect()).get_label()

        logger.info("Plurality classification: " + classification)

        assert classification == "Iris-setosa"

    def test_importance(self):
        dt = DecisionTree(self.iris_dataset, "class")

        ig = dt.importance(self.iris_dataset.collect(), "petal_length")
        print(ig)
        assert ig > 0

    def test_attribute_test(self):
        logger.info("test_attribute_test")

        branch = Branch(lambda value, test_value: value > test_value, TreeNode('sepal_width'), 4.3)

        sample = self.iris_dataset.collect()[8]['sepal_length']
        logger.info(sample)

        assert branch.value_test(sample)

    def test_query(self):
        dt = DecisionTree(self.iris_dataset, "class")
        dt.query(self.iris_dataset.collect()[8])

    def test_decision_tree_election(self):
        logger.info("Running election dataset decision tree tests...")

        sample_dataset = self.election_dataset.sample(fraction=.10, withReplacement=True).rdd.collect()

        dt = DecisionTree(sample_dataset, "class")
        dt.train(sample_dataset)
        dt.depth_first_traversal(dt.get_root())

        sample = sample_dataset[10]

        logger.info("Predicted Class for Election Dataset: " + str(
            dt.classify(dt.get_root(), sample)) + " Actual Class: " + str(sample_dataset[10]["class"]))

    def test_best_split_point(self):
        dt = DecisionTree(self.iris_dataset, "class")

        logger.info(dt.best_split_point(self.iris_dataset.collect(), "petal_length"))

    def test_best_attribute(self):
        logger.info("Running best attribute tests...")

        dt = DecisionTree(self.iris_dataset, "class")

        dataset = self.iris_dataset.collect()

        attributes = dataset[0].__fields__.copy()
        attributes.remove(self.TARGET)

        logger.info("Best attribute is {}".format(dt.best_attribute(dataset, attributes)))

    def test_extract_potential_split_points(self):
        dt = DecisionTree(self.iris_dataset, "class")

        logger.info(dt.extract_potential_split_points(self.iris_dataset.collect(), "petal_length"))

    @unittest.skip
    def test_decision_tree_profile(self):
        sample_dataset = self.election_dataset.sample(fraction=.10, withReplacement=True)
        dt = DecisionTree(sample_dataset, self.TARGET)
        cProfile.runctx('dt.train(sample_dataset)', locals={'sample_dataset': sample_dataset, 'dt': dt}, globals=None)


if __name__ == "__main__":
    unittest.main()
