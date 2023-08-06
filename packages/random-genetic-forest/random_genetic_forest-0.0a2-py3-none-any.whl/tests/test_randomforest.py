import unittest
import pandas as pd
import numpy as np
import logging as logger
import sys

from pyspark import SparkContext, SQLContext

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from machinelearning.randomforest import RandomForest

logger.basicConfig(level=logger.INFO, format="%(asctime)s %(levelname)s - %(message)s",
            handlers=[
                logger.FileHandler("{0}/{1}.log".format(".", "rgf")),
                logger.StreamHandler(sys.stdout)
            ])


@unittest.skip
class TestRandomForest(unittest.TestCase):
    TARGET = "class"
    DATASET_DIR = "tests/datasets/"

    @classmethod
    def setUpClass(self):
        self.sc = SparkContext.getOrCreate()
        self.sqlContext = SQLContext(self.sc)
        self.iris_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema", "true").option(
            "mode", "DROPMALFORMED").load(
            self.DATASET_DIR + "iris.csv")
        self.election_dataset = self.sqlContext.read.format("csv").option("header", "true").option("inferschema",
                                                                                                        "true").option(
            "mode", "DROPMALFORMED").load(
            self.DATASET_DIR + "house-votes-84.csv")

    @unittest.skip
    def test_mlib_random_forest(self):
        logger.info("Testing mlib random forest...")
        labels = np.array(self.iris_dataset["class"])
        print(labels)
        features = self.iris_dataset.drop("class",axis=1)
        print(features)
        feature_list = features.columns
        features = np.array(features)

        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.1,
                                                                                    random_state=42)
        rf = RandomForestClassifier(n_estimators=1000, random_state=42)
        rf.fit(train_features, train_labels);
        rf.predict(test_features)

    @unittest.skip
    def test_randomforest_iris(self):
        rf = RandomForest(40, 2, "class")
        rf.train(self.iris_dataset)
        rf.test(self.iris_dataset)
    @unittest.skip
    def test_randomforest_election(self):
        rf = RandomForest(40, 2, "class")
        rf.train(self.election_dataset)
        rf.test(self.election_dataset)