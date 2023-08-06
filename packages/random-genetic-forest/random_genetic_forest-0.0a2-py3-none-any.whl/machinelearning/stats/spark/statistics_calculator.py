
import math

class StatisticsCalculator:

    def attribute_entropy(self):
        pass

    @staticmethod
    def get_probabilities(examples,attribute):
        size = len(examples)
        counts = {}
        probabilities = []
        for example in examples:
            count = counts.get(str(example[attribute]))
            if count is None: count = 0
            counts.update({example[attribute]: count + 1})
        for count in counts.values():
            probabilities.append(count/size)
        return probabilities

    @staticmethod
    def entropy(probabilities):
        entropy = 0.0
        for probability in probabilities:
            entropy += probability * math.log2(probability)
        return -entropy

    @staticmethod
    def info_gain(target_entropy, cond_entropy):
        return target_entropy - cond_entropy

    @staticmethod
    def midpoint(value1, value2):
        return (value1 + value2) / 2

    @staticmethod
    def mode(examples,attribute):
        counts = {}
        for example in examples:
            count = counts.get(str(example[attribute]))
            if count is None: count = 0
            counts.update({example[attribute]: count + 1})
        max_key = max(counts,key=lambda key: counts[key])
        return max_key

    @staticmethod
    def midpoint_list(items):
        midpoint_list = []
        for x in range(len(items) - 1):
            midpoint_list.append(StatisticsCalculator.midpoint(items[x], items[x + 1]))
        return midpoint_list


class CategoricalStatisticsCalculator(StatisticsCalculator):

    @staticmethod
    def attribute_entropy(examples,attribute):
        probabilities = CategoricalStatisticsCalculator.get_probabilities(examples,attribute)
        return CategoricalStatisticsCalculator.entropy(probabilities)

    @staticmethod
    def conditional_attribute_entropy(examples,attribute,target):
        size = len(examples)
        average_entropy = 0.0
        attribute_values = CategoricalStatisticsCalculator.get_distinct_attribute_values_from_dataset(examples,attribute)
        for value in attribute_values:
            filtered_examples = list(filter(lambda example: example[attribute] == value,examples))
            probability_list = CategoricalStatisticsCalculator.get_probabilities(filtered_examples,target)
            filtered_probability = (len(filtered_examples)/size)
            average_entropy += filtered_probability * CategoricalStatisticsCalculator.entropy(probability_list)
        return average_entropy

    @staticmethod
    def get_attribute_values_from_pairs(attribute_pairs):
        attribute_values = []
        for attribute_pair in attribute_pairs:
            attribute_values.append(attribute_pair[0])
        return attribute_values

    @staticmethod
    def get_target_values_from_pairs(attribute_pairs):
        target_values = []
        for attribute_pair in attribute_pairs:
            target_values.append(attribute_pair[1])
        return target_values

    @staticmethod
    def get_distinct_attribute_values_from_dataset(examples,attribute):
        attribute_values = set()
        for example in examples:
            attribute_values.add(example[attribute])
        return list(attribute_values)

class ContinuousStatisticsCalculator(StatisticsCalculator):

    @staticmethod
    def attribute_entropy(examples,attribute,target, split_point):
        left_examples = list(filter(lambda row: row[attribute] < split_point, examples))
        right_examples = list(filter(lambda row: row[attribute] >= split_point, examples))

        left_prob_list = ContinuousStatisticsCalculator.get_probabilities(left_examples,target)
        right_prob_list = ContinuousStatisticsCalculator.get_probabilities(right_examples,target)

        left_prob = (len(left_examples) / len(examples))
        right_prob = (len(right_examples) / len(examples))

        entropy = left_prob * ContinuousStatisticsCalculator.entropy(left_prob_list) + right_prob * ContinuousStatisticsCalculator.entropy(right_prob_list)
        return entropy
