class MsaConsensusAlgorithmStrict(MsaConsensusAlgorithm):
    def get_consensus_char(self, ma, column) -> str:
        # Pick the rows to use for consensus
        seq_idx = self.pick_rows_to_use_in_consensus(ma, column)

        if not self.ignore_trailing_and_leading_gaps or not seq_idx:
            pass  # Equivalent to CHECK in C++; can raise exception if needed
        else:
            raise ValueError("Invalid consensus character")

        # Initialize frequency array for all possible 256 ASCII characters
        freqs_by_char = [0] * 256
        non_gaps = 0

        # Fill frequencies and get the top character
        top_char = MsaConsensusUtils.get_column_freqs(ma, column, freqs_by_char, non_gaps, seq_idx)

        # Determine number of sequences to consider
        n_seq = len(seq_idx) if seq_idx else ma.get_row_count()

        # Compute threshold count
        current_threshold = self.get_threshold()
        cnt_to_use_gap = current_threshold / 100.0 * n_seq
        top_freq = freqs_by_char[top_char]

        # Return gap if top frequency below threshold, else the character
        res = U2Msa.GAP_CHAR if top_freq < cnt_to_use_gap else chr(top_char)
        return res

    def clone(self):
        # Return a copy of this algorithm
        return MsaConsensusAlgorithmStrict()
