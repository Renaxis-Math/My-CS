"""
Create a class that will determine if we've-seen • a certain rate of rejects given a threshold and• timespan
In the constructor
- threshold is the-number. of rejections within the timespan that will cause an• alert
- timespan is the time window in microseconds
handleReject accepts a timestamp-in•microseconds
- returns true if. the rate of rejections• rea the threshold within the timespan
-• returns false• otherwise
"""

from collections import deque

class RejectAlert:
    def __init__(self, threshold, timespan):
        """
        Time Complexity: O(1) worst case
        Space Complexity: O(threshold) worst case
        threshold = reject count threshold
        """
        self.threshold = threshold
        self.timespan = timespan
        self.reject_timestamp_deque = deque()  # timestamp

    def handleReject(self, timestamp):
        """
        Time Complexity: Worst Case: O(1); Amortized O(1)
        Space Complexity: Worst case: O(threshold)
        """
        if self.threshold <= 0:
            return True

        self.reject_timestamp_deque.append(timestamp)

        if len(self.reject_timestamp_deque) > self.threshold:
            self.reject_timestamp_deque.popleft()

        if len(self.reject_timestamp_deque) < self.threshold:
            return False

        oldest_timestamp = self.reject_timestamp_deque[0]
        return timestamp - oldest_timestamp <= self.timespan