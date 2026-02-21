import psutil, os, time

class Metrics:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def ram_mb(self):
        return self.process.memory_info().rss / (1024 ** 2)

    def enforce_limit(self, max_mb: float):
        current = self.ram_mb()
        if current > max_mb:
            raise MemoryError(
                f"RAM limit exceeded: {current:.2f} MB > {max_mb:.2f} MB"
            )

    def timed(self, fn):
        start = time.time()
        result = fn()
        end = time.time()
        return result, end - start
