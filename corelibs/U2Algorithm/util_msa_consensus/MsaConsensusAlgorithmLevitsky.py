class MsaConsensusAlgorithmLevitsky:
    def __init__(self, factory, msa, ignore_trailing_leading_gaps=False):
        self.factory = factory
        self.ignore_trailing_leading_gaps = ignore_trailing_leading_gaps
        self.global_freqs = [0] * 256
        self.msa = msa
        self.reinitialize_data(msa)

    def reinitialize_data(self, msa):
        """Compute global frequencies for all characters in the MSA."""
        self.global_freqs = [0] * 256
        for row in msa:
            for c in row:
                register_hit(self.global_freqs, c)

    def get_threshold(self) -> float:
        """Return threshold as a fraction (e.g., 0.9 for 90%)."""
        return self.factory.default_threshold / 100.0

    def pick_rows_to_use_in_consensus(self, column: int) -> List[int]:
        """Return row indices to consider in consensus (ignoring leading/trailing gaps)."""
        if not self.ignore_trailing_leading_gaps:
            return list(range(len(self.msa)))
        # Example: skip rows that are gaps in this column
        return [i for i, row in enumerate(self.msa) if row[column] != '-']

    def get_consensus_char(self, column: int) -> str:
        seq_idx = self.pick_rows_to_use_in_consensus(column)
        if not self.ignore_trailing_leading_gaps and not seq_idx:
            raise ValueError("Invalid consensus character (no sequences available)")

        # Count column-local frequencies
        local_freqs = [0] * 91  # max tracked 'Z' index
        n_seq = len(seq_idx) if seq_idx else len(self.msa)
        for i in range(n_seq):
            row_idx = seq_idx[i] if seq_idx else i
            c = self.msa[row_idx][column]
            if 'A' <= c <= 'Z':
                register_hit(local_freqs, c)

        # Find symbols with frequency >= threshold and lowest global frequency
        selected_global_percentage = 2.0  # init > 100%
        threshold_score = self.get_threshold()
        selected_group_index = -1
        selected_chars = []

        for i, c in enumerate(ALL_EXT_DNA_CHARACTERS):
            local_percentage = local_freqs[ord(c)] / n_seq
            if local_percentage < threshold_score:
                continue

            global_percentage = self.global_freqs[ord(c)] / (n_seq * len(self.msa[0]))
            if global_percentage > selected_global_percentage:
                continue

            group_index = get_character_group(i)
            if global_percentage < selected_global_percentage:
                selected_chars = [c]
                selected_global_percentage = global_percentage
                selected_group_index = group_index
            elif group_index == selected_group_index:
                selected_chars.append(c)

        if not selected_chars:
            return '-'  # gap if no character found

        if len(selected_chars) == 1:
            return selected_chars[0]

        # Merge multiple selected characters into mask
        mask = merge_chars_into_mask(''.join(selected_chars))
        return MASK_2_CHAR[mask]

    def clone(self):
        """Return a copy of this algorithm instance."""
        return MsaConsensusAlgorithmLevitsky(self.factory, self.msa, self.ignore_trailing_leading_gaps)

# ------------------------
# Example Usage
# ------------------------
if __name__ == "__main__":
    msa = [
        "ATGC",
        "AAGC",
        "ATCC",
    ]
    factory = MsaConsensusAlgorithmFactoryLevitsky()
    algo = factory.create_algorithm(msa)

    consensus_sequence = "".join(algo.get_consensus_char(col) for col in range(len(msa[0])))
    print("Consensus:", consensus_sequence)
