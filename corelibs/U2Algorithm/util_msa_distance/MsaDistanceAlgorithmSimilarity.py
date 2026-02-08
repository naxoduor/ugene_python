import threading

class MsaDistanceAlgorithmSimilarity:
    def __init__(self, ma, exclude_gaps=False):
        self.ma = ma  # The MSA object
        self.exclude_gaps = exclude_gaps
        self.lock = threading.Lock()
        self.state_info = StateInfo()  # Placeholder for progress tracking

    def is_canceled(self):
        # Implement your cancellation logic here
        return False

    def set_distance_value(self, i, j, value):
        # Implement storing the distance/similarity value
        # Example: could be a 2D list or a dictionary
        print(f"Distance between {i} and {j}: {value}")

    def run(self):
        n_seq = self.ma.get_row_count()
        for i in range(n_seq):
            for j in range(i, n_seq):
                sim = 0
                for k in range(self.ma.get_length()):
                    if self.is_canceled():
                        return

                    similar = (self.ma.char_at(i, k) == self.ma.char_at(j, k))

                    if not self.exclude_gaps:
                        if similar:
                            sim += 1
                    else:
                        if similar and self.ma.char_at(i, k) != self.ma.GAP_CHAR:
                            sim += 1

                with self.lock:
                    self.set_distance_value(i, j, sim)

            self.state_info.set_progress(i * 100 // n_seq)


