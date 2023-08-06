from pyspark import SparkContext

import time
import random
import logging as logger

from machinelearning.metrics import MLMetrics
from machinelearning.tree.decision_tree import DecisionTree


class RandomForest:

    def __init__(self,num_trees, m_try, target):
        self.num_trees = num_trees
        self.m_try = m_try
        self.trees = []
        self.target = target

    def train(self, training_set):
        logger.info("Training random forest algorithm...")
        start_time = time.time()
        self.trees = []

        self.generate_trees(training_set)

        elapsed_time = time.time() - start_time

        logger.info("Trained random forest in " + str(round(elapsed_time,4)) + " seconds.")

    def test(self,test_set):
        classes = list(test_set.select(self.target).distinct().rdd.map(lambda row: row[self.target]).collect())

        results = test_set.rdd.map(lambda sample: (self.query(sample),sample[self.target])).collect()

        MLMetrics.describe_results(classes,results)

    def generate_boostrap_sample(self, training_dataset):
        return training_dataset.sample(True, 0.3)

    def generate_trees(self, training_dataset):
        bootstrap_samples = self.generate_bootstrap_samples(training_dataset)
        samples = SparkContext.getOrCreate().parallelize(bootstrap_samples)
        self.trees = samples.map(lambda sample: self.generate_tree(sample)).collect()

    def generate_bootstrap_samples(self,training_dataset):
        bootstrap_samples = []
        for i in range(self.num_trees):
            bootstrap_samples.append(self.generate_boostrap_sample(training_dataset).rdd.collect().copy())
        return bootstrap_samples

    def generate_tree(self,training_dataset):
        dt = DecisionTree(training_dataset, self.target,
                          attribute_randomizer=self.randomly_select_attributes)
        dt.train(training_dataset)
        return dt

    def randomly_select_attributes(self,attributes):
        return random.sample(attributes, self.m_try)

    def query(self, example):
        votes = {}

        for tree in self.trees:
            prediction = tree.query(example)
            if prediction not in votes.keys():
                votes[prediction] = 1
            else:
                votes[prediction] += 1

        classification = max(votes,key=lambda key: votes[key])
        return classification