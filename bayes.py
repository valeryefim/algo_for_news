import math
from collections import Counter, defaultdict


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.class_probs = defaultdict(float)
        self.feature_probs = defaultdict(lambda: defaultdict(float))

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""

        num_samples = len(y)
        class_counts = Counter(y)
        for class_, count in class_counts.items():
            self.class_probs[class_] = math.log(count / num_samples)
        self.class_counts = class_counts

        for xi, yi in zip(X, y):
            for feature in xi:
                self.feature_probs[yi][feature] += 1

        for class_ in class_counts.keys():
            for feature, count in self.feature_probs[class_].items():
                self.feature_probs[class_][feature] = math.log(
                    (count + self.alpha)
                    / (class_counts[class_] + self.alpha * len(self.feature_probs[class_]))
                )

    def predict(self, X):
        """Perform classification on an array of test vectors X."""

        y_pred = []
        for xi in X:
            class_probs = self.class_probs.copy()
            for class_ in class_probs.keys():
                for feature in xi:
                    class_probs[class_] += self.feature_probs[class_].get(
                        feature,
                        math.log(
                            self.alpha
                            / (
                                self.class_counts[class_]
                                + self.alpha * len(self.feature_probs[class_])
                            )
                        ),
                    )
            y_pred.append(max(class_probs, key=class_probs.get))
        return y_pred

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""

        y_pred = self.predict(X_test)
        return sum(y_true == y_pred for y_true, y_pred in zip(y_test, y_pred)) / len(y_test)
