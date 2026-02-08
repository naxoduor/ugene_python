import threading

class MsaDistanceAlgorithmHamming:
    GAP_CHAR = '-'  # equivalent to U2Msa::GAP_CHAR

    def __init__(self, msa, exclude_gaps=False):
        """
        :param msa: multiple sequence alignment object
                    must implement:
                      - get_row_count()
                      - get_length()
                      - char_at(row, col)
        :param exclude_gaps: bool
        """
        self.ma = msa
        self.exclude_gaps = exclude_gaps
        self.lock = threading.Lock()
        self.distances = {}
        self._canceled = False

    def is_canceled(self):
        return self._canceled

    def cancel(self):
        self._canceled = True

    def set_distance_value(self, i, j, value):
        """Store distance (symmetric)."""
        self.distances[(i, j)] = value
        self.distances[(j, i)] = value

    def set_progress(self, percent):
        """Progress callback (placeholder)."""
        pass

    def run(self):
        n_seq = self.ma.get_row_count()

        for i in range(n_seq):
            for j in range(i, n_seq):
                sim = 0

                for k in range(self.ma.get_length()):
                    if self.is_canceled():
                        return

                    c1 = self.ma.char_at(i, k)
                    c2 = self.ma.char_at(j, k)
                    dissimilar = (c1 != c2)

                    if not self.exclude_gaps:
                        if dissimilar:
                            sim += 1
                    else:
                        if dissimilar and c1 != self.GAP_CHAR and c2 != self.GAP_CHAR:
                            sim += 1

                with self.lock:
                    self.set_distance_value(i, j, sim)

            self.set_progress(i * 100 // n_seq)
