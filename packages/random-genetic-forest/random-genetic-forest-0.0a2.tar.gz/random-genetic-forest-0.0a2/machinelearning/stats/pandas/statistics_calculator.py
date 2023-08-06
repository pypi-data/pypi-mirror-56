
import math
import logging
import time
import sys


class StatisticsCalculator:


    def attribute_entropy(self):
        pass

    def get_conditional_probabilities(self, examples, target):
        return examples.groupby(target).size().apply(lambda x: x / len(examples))

    def entropy(self,probabilities):
        entropy = 0.0
        entropy = probabilities.apply(lambda x: x*math.log2(x)).sum()
        return -entropy

    def info_gain(self,target_entropy, cond_entropy):
        return target_entropy - cond_entropy

    def midpoint(self, value1, value2):
        return (value1 + value2)/2

    def midpoint_list(self, items):
        midpoint_list = []
        for x in range(len(items)-1):
            midpoint_list.append(self.midpoint(items[x], items[x+1]))
        return midpoint_list


class CategoricalStatisticsCalculator(StatisticsCalculator):

    def attribute_entropy(self, examples, attribute, target=None):
        if target == None:
            probabilities = examples.groupby(attribute).size().div(len(examples))
            return self.entropy(probabilities)
        else:
            average_entropy = 0.0
            for value in examples[attribute].unique():
                filtered = examples.where(examples[attribute] == value,inplace=False,axis=None).dropna()
                probability_list = self.get_conditional_probabilities(filtered, target)
                filtered_probability = (len(filtered)/len(examples))
                average_entropy += filtered_probability * self.entropy(probability_list)
            return average_entropy

class ContinuousStatisticsCalculator(StatisticsCalculator):


    def attribute_entropy(self, df, attribute, target, split_point):
        start = time.time()
        left_df = df.where(df[attribute] < split_point, inplace=False).dropna()
        right_df = df.where(df[attribute] >= split_point, inplace=False).dropna()

        left_prob_list = self.get_conditional_probabilities(left_df,target)
        right_prob_list = self.get_conditional_probabilities(right_df,target)

        left_prob = (len(left_df)/len(df))
        right_prob = (len(right_df) / len(df))

        entropy = left_prob * self.entropy(left_prob_list) + right_prob * self.entropy(right_prob_list)
        end = time.time()
        logging.debug("Entropy for " + str(attribute) + " at split point " + str(split_point) + " is " + str(entropy))
        logging.debug("Calculated entropy in {} seconds.".format(round(end - start,4)))
        return entropy