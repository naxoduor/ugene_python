class MsaConsensusAlgorithmDefault(MsaConsensusAlgorithm):
    def get_consensus_char_and_score(self, ma, pos):
        """
        Returns (consensus_char, count)
        """

        # Pick rows used in consensus
        seq_idx = self.pickRowsToUseInConsensus(ma, pos)

        if self.ignoreTrailingAndLeadingGaps and not seq_idx:
            return INVALID_CONS_CHAR, 0

        # Frequency table: [count, char]
        frequencies = [[0, '-'] for _ in range(32)]

        # Number of sequences
        n_seq = len(seq_idx) if seq_idx else ma.getRowCount()

        for i in range(n_seq):
            row = seq_idx[i] if seq_idx else i
            c = ma.charAt(row, pos)

            if 'A' <= c <= 'Z':
                idx = ord(c) - ord('A')
                frequencies[idx][0] += 1
                frequencies[idx][1] = c

        # Sort like std::sort(QPair<int, char>)
        frequencies.sort()

        p1 = frequencies[-1][0]
        p2 = frequencies[-2][0]

        if p1 == 0 or (p1 == 1 and n_seq > 1):
            ch = U2Msa.GAP_CHAR
            cnt = 0
        else:
            c1 = frequencies[-1][1]
            ch = '+' if p1 == p2 else c1
            cnt = p1

        # Lowercase alpha chars with < threshold% content
        current_threshold = self.getThreshold()
        cnt_to_use_lowercase = int(current_threshold / 100.0 * n_seq)

        if cnt < cnt_to_use_lowercase and 'A' <= ch <= 'Z':
            ch = ch.lower()

        return ch, cnt
