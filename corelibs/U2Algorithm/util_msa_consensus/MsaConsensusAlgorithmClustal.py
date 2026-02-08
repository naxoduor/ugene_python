class MsaConsensusAlgorithmClustal(MsaConsensusAlgorithm):
    GAP_CHAR = '-'  # assuming U2Msa::GAP_CHAR

    def __init__(self, factory, ignore_trailing_leading_gaps: bool = False):
        self.factory = factory
        self.ignore_trailing_leading_gaps = ignore_trailing_leading_gaps

    def pick_rows_to_use_in_consensus(self, msa, pos):
        # Placeholder for your selection logic
        return list(range(msa.get_row_count()))

    def get_consensus_char(self, msa, pos: int) -> str:
        seq_idx = self.pick_rows_to_use_in_consensus(msa, pos)
        if self.ignore_trailing_leading_gaps and not seq_idx:
            return ' '  # INVALID_CONS_CHAR equivalent

        if not msa.get_alphabet().is_amino():  # nucleic case
            default_char = ' '
            pc = (msa.get_row(0 if not seq_idx else seq_idx[0]).char_at(pos))
            if pc == self.GAP_CHAR:
                pc = default_char

            n_seq = len(seq_idx) if seq_idx else msa.get_row_count()
            for s in range(1, n_seq):
                c = msa.get_row(s if not seq_idx else seq_idx[s]).char_at(pos)
                if c != pc:
                    pc = default_char
                    break
            return default_char if pc == default_char else '*'

        else:  # amino acid case
            strong_groups = ["STA", "NEQK", "NHQK", "NDEQ", "QHRK",
                             "MILV", "MILF", "HY", "FYW"]
            weak_groups = ["CSA", "ATV", "SAG", "STNK", "STPA",
                           "SGND", "SNDEQK", "NDEQHK", "NEQHRK",
                           "FVLIM", "HFY"]

            max_strong_len = 4
            max_weak_len = 6

            # Collect all unique residues at this position
            n_seq = len(seq_idx) if seq_idx else msa.get_row_count()
            current_group = set()
            for s in range(n_seq):
                c = msa.get_row(s if not seq_idx else seq_idx[s]).char_at(pos)
                current_group.add(c)

            if len(current_group) == 1:
                cons_char = '*' if list(current_group)[0] != self.GAP_CHAR else ' '
                return cons_char

            # Check strong groups
            ok = False
            if len(current_group) <= max_strong_len:
                for group in strong_groups:
                    if all(c in group for c in current_group):
                        ok = True
                        break
                if ok:
                    return ':'

            # Check weak groups
            if len(current_group) <= max_weak_len:
                for group in weak_groups:
                    if all(c in group for c in current_group):
                        ok = True
                        break
                if ok:
                    return '.'

            return ' '  # default if nothing matches

    def clone(self):
        # In Python, shallow copy is enough unless deep copy needed
        import copy
        return copy.copy(self)
