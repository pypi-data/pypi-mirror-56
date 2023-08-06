import logging as logger
import time

from machinelearning.stats.spark.statistics_calculator import CategoricalStatisticsCalculator, \
    ContinuousStatisticsCalculator, StatisticsCalculator
from machinelearning.tree.general_tree import GeneralTree
from machinelearning.tree.node.branch import Branch
from machinelearning.tree.node.treenode import TreeNode


class DecisionTree(GeneralTree):

    def __init__(self, trainingdata, target, attribute_randomizer=None):
        super().__init__(None)
        self.target = target
        self.attribute_randomizer = attribute_randomizer

    def train(self, trainingdata):
        logger.info("Training decision tree...")

        start_time = time.time()

        attribute_list = trainingdata[0].__fields__.copy()

        attribute_list.remove(self.target)

        super().set_root(self.decision_tree_learning(trainingdata, attribute_list, trainingdata))

        elapsed_time = time.time() - start_time
        logger.info("Decision tree trained in " + str(round(elapsed_time, 4)) + "seconds.")

    def decision_tree_learning(self, examples, attributes, parent_examples):
        if len(examples) == 0:
            return self.plurality_value(parent_examples)
        elif self.has_same_classification(examples):
            return TreeNode(examples[0][self.target])
        elif not attributes:
            return self.plurality_value(parent_examples)

        attribute = self.best_attribute(examples, attributes)

        new_attributes = attributes[:]
        new_attributes.remove(attribute)

        node = None
        if self.is_numeric(examples, attribute):
            node = self.create_subtree_continuous(examples, new_attributes, attribute)
        else:
            node = TreeNode(attribute)
            values = self.get_unique_attribute_values(examples, attribute)
            for value in values:
                sub_examples = self.filter_examples_by_value(examples, attribute, value)
                child = self.decision_tree_learning(sub_examples, new_attributes, attributes)
                node.add_child(Branch(self.value_test, child, value))

        return node

    def filter_examples_by_value(self, examples, attribute, value):
        filtered_examples = []
        for example in examples:
            if example[attribute] == value:
                filtered_examples.append(example)
        return filtered_examples

    def get_unique_attribute_values(self, examples, attribute):
        values = set()
        for example in examples:
            values.add(example[attribute])
        return list(values)

    def is_numeric(self, examples, attribute):
        sample_type = type(examples[0][attribute])
        return sample_type == int or sample_type == float

    def create_subtree_continuous(self, examples, attributes, attribute):
        stats = ContinuousStatisticsCalculator()
        node = TreeNode(attribute)
        split_point = self.best_split_point(examples, attribute)

        left = DecisionTree.filter_examples_by_split_point_left(examples, attribute, split_point)
        left_child = self.decision_tree_learning(left, attributes, examples)
        node.add_child(Branch(self.left_test, left_child, split_point))

        right = DecisionTree.filter_examples_by_split_point_right(examples, attribute, split_point)
        right_child = self.decision_tree_learning(right, attributes, examples)
        node.add_child(Branch(self.right_test, right_child, split_point))

        return node

    def value_test(self, value, test_value):
        return value == test_value

    def left_test(self, value, split_point):
        return value < split_point

    def right_test(self, value, split_point):
        return value >= split_point

    @staticmethod
    def filter_examples_by_split_point_left(examples, attribute, split_point):
        filtered_examples = []
        for example in examples:
            if example[attribute] < split_point:
                filtered_examples.append(example)
        return filtered_examples

    @staticmethod
    def filter_examples_by_split_point_right(examples, attribute, split_point):
        filtered_examples = []
        for example in examples:
            if example[attribute] >= split_point:
                filtered_examples.append(example)
        return filtered_examples

    def has_same_classification(self, examples):
        counts = {}
        for example in examples:
            count = counts.get(example[self.target])
            if count is None: count = 0
            counts.update({example[self.target]: count + 1})

        return len(counts.keys()) == 1

    def plurality_value(self, parent_examples):
        return TreeNode(label=StatisticsCalculator.mode(parent_examples, self.target))

    def importance(self, examples, attribute):
        target_entropy = CategoricalStatisticsCalculator.attribute_entropy(examples, self.target)
        attribute_entropy = 0.0

        if self.is_numeric(examples, attribute):
            best_split_point = self.best_split_point(examples, attribute)
            attribute_entropy = ContinuousStatisticsCalculator.attribute_entropy(examples, attribute, self.target,
                                                                                 best_split_point)
        else:
            attribute_entropy = CategoricalStatisticsCalculator.conditional_attribute_entropy(examples, attribute,
                                                                                              self.target)

        return ContinuousStatisticsCalculator.info_gain(target_entropy, attribute_entropy)

    def query(self, sample):
        return self.classify(self.get_root(), sample)

    def classify(self, node, sample):
        if not node.has_children():
            return node.get_label()
        for branch in node.get_children():
            if branch.value_test(sample[node.get_label()]):
                return self.classify(branch.get_node(), sample)

    def best_attribute(self, examples, attributes):
        if len(attributes) < 2:
            return attributes[0]

        selected_attributes = attributes

        if self.attribute_randomizer is not None:
            selected_attributes = self.attribute_randomizer(attributes)

        info_gains = []
        for selected_attribute in selected_attributes:
            info_gains.append((selected_attribute, self.importance(examples, selected_attribute)))

        max_id = max(info_gains, key=lambda info_gain: info_gain[1])[0]

        return max_id

    def extract_potential_split_points(self, examples, attribute):
        potentials = []

        sorted_examples = sorted(examples, key=lambda item: item[attribute])

        for index in range(0, len(sorted_examples) - 1):
            if sorted_examples[index][self.target] != sorted_examples[index + 1][self.target]:
                potentials.append(sorted_examples[index][attribute])

        return list(set(potentials))

    # TODO: Convert to spark
    def best_split_point(self, examples, attribute):
        potentials = self.extract_potential_split_points(examples, attribute)

        if len(potentials) == 1:
            return potentials[0]

        potentials = ContinuousStatisticsCalculator.midpoint_list(potentials);

        target_entropy = CategoricalStatisticsCalculator.attribute_entropy(examples, self.target)

        entropies = []
        for potential in potentials:
            entropies.append((potential,
                              ContinuousStatisticsCalculator.attribute_entropy(examples, attribute, self.target,
                                                                               potential)))

        info_gains = []
        for entropy in entropies:
            info_gains.append((entropy[0], ContinuousStatisticsCalculator.info_gain(target_entropy, entropy[1])))

        best_split_point = max(info_gains, key=lambda pair: pair[1])[0]

        return best_split_point
