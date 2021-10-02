from collections import Counter

# memory efficient counter of averages of set of percents
class AvgPercentCounter():
    def __init__(self):
        self.data = Counter()

    def put_value(self, value):
        index = round(value)
        self.data[index] += 1

    def get_average(self):
        if not self.data:
            return 0.0
        return sum([(p * v) for p, v in self.data.items()]) / \
            sum([v for _, v in self.data.items()])

""" no unit tests here, tested manually
import avg_counter
a = AvgPercentCounter()
a.get_average()

a.put_value(10)
a.get_average()

a.put_value(30)
a.get_average()

a.put_value(10)
a.put_value(10)
a.put_value(30)
a.put_value(30)
a.put_value(10)
a.put_value(30)
a.get_average()
"""