from prettytable import PrettyTable
from statistics import mean

class MLMetrics:

    @staticmethod
    def f_measure(precision,recall):
        return 2 * ((precision*recall)/(precision+recall))

    @staticmethod
    def precision(true_positives,false_positives):
        return true_positives/(true_positives + false_positives)

    @staticmethod
    def recall(true_positives,false_negatives):
        return true_positives / (true_positives + false_negatives)

    @staticmethod
    def class_precision(class_index,confusion_matrix):
        true_positives = confusion_matrix[class_index][class_index]
        false_positives = 0
        for index in range(len(confusion_matrix[class_index])):
            if index != class_index:
                false_positives += confusion_matrix[class_index][index]
        return MLMetrics.precision(true_positives,false_positives)

    @staticmethod
    def class_recall(class_index,confusion_matrix):
        true_positives = confusion_matrix[class_index][class_index]
        false_negatives = 0
        for index in range(len(confusion_matrix[class_index])):
            if index != class_index:
                false_negatives += confusion_matrix[index][class_index]
        return MLMetrics.precision(true_positives, false_negatives)

    @staticmethod
    def describe_results(classes,results):
        confusion_matrix = MLMetrics.create_confusion_matrix(classes,results)
        MLMetrics.print_confusion_matrix(classes, confusion_matrix)

        MLMetrics.print_metrics(classes,confusion_matrix)

    @staticmethod
    def print_metrics(classes,confusion_matrix):
        class_metrics = PrettyTable(["Class", "Precision", "Recall", "F-Measure"])
        weighted_metrics = PrettyTable(["Weighted Precision","Weighted Recall","Weighted F-Measure"])
        precisions = []
        recalls = []
        f_measures = []
        for class_index,cls in enumerate(classes,start=0):
            precision = MLMetrics.class_precision(class_index,confusion_matrix)
            precisions.append(precision)
            recall = MLMetrics.class_recall(class_index,confusion_matrix)
            recalls.append(recall)
            f_measure = MLMetrics.f_measure(precision,recall)
            f_measures.append(f_measure)
            class_metrics.add_row([cls,precision,recall,f_measure])
        print(class_metrics)

        weighted_metrics.add_row([mean(precisions),mean(recalls),mean(f_measures)])
        print(weighted_metrics)

    @staticmethod
    def create_confusion_matrix(classes,results):
        confusion_matrix = MLMetrics.init_confusion_matrix(classes)

        for result in results:
            row_index = classes.index(result[0])
            col_index = classes.index(result[1])
            confusion_matrix[row_index][col_index] += 1
        return confusion_matrix

    @staticmethod
    def init_confusion_matrix(classes):
        confusion_matrix = []
        for i in range(len(classes)):
            row = []
            for j in range(len(classes)):
                row.append(0)
            confusion_matrix.append(row)
        return confusion_matrix

    @staticmethod
    def print_confusion_matrix(classes,confusion_matrix):
        pt = PrettyTable([''] + classes)
        pt.title = "Confusion Matrix"
        for i in range(len(classes)):
            class_record = [classes[i]]
            for j in range(len(classes)):
                class_record.append(confusion_matrix[i][j])
            pt.add_row(class_record)

        print(pt)
