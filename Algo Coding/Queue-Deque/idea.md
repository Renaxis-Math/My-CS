To make all operations WORST-CASE O(1), 4 main ideas:
- Force a fixed-size queue, anytime queue.size() > threshold, pop
- Buckets: Instead of storing events individually, you aggregate them into fixed buckets.
- Math: e.g Running Average

For amortized O(1):
- Monotonic elements