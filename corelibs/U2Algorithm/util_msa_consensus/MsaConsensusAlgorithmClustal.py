class MsaConsensusAlgorithmFactory:
    def __init__(self, algorithm_id, flags):
        self.algorithm_id = algorithm_id
        self.flags = flags
        self.name = ""
        self.description = ""


class BuiltInConsensusAlgorithms:
    CLUSTAL_ALGO = "clustal"


ConsensusAlgorithmFlags_AllAlphabets = "all_alphabets"


class MsaConsensusAlgorithmClustal:
    def __init__(self, factory, ignore_trailing_leading_gaps=False):
        self.factory = factory
        self.ignore_trailing_leading_gaps = ignore_trailing_leading_gaps


class MsaConsensusAlgorithmFactoryClustal(MsaConsensusAlgorithmFactory):
    def __init__(self):
        super().__init__(
            BuiltInConsensusAlgorithms.CLUSTAL_ALGO,
            ConsensusAlgorithmFlags_AllAlphabets,
        )

        self.name = "ClustalW"
        self.description = (
            "Emulates ClustalW program and file format behavior."
        )

    def create_algorithm(self, msa, ignore_trailing_leading_gaps):
        return MsaConsensusAlgorithmClustal(
            self,
            ignore_trailing_leading_gaps,
        )




class MsaConsensusAlgorithmClustal:
    GAP_CHAR = "-"
    INVALID_CONS_CHAR = " "

    STRONG_GROUPS = [
        "STA",
        "NEQK",
        "NHQK",
        "NDEQ",
        "QHRK",
        "MILV",
        "MILF",
        "HY",
        "FYW",
    ]

    WEAK_GROUPS = [
        "CSA",
        "ATV",
        "SAG",
        "STNK",
        "STPA",
        "SGND",
        "SNDEQK",
        "NDEQHK",
        "NEQHRK",
        "FVLIM",
        "HFY",
    ]

    MAX_STRONG_GROUP_LEN = 4
    MAX_WEAK_GROUP_LEN = 6

    def __init__(self, ignore_trailing_leading_gaps=False):
        self.ignore_trailing_leading_gaps = ignore_trailing_leading_gaps

    def get_consensus_char(self, msa, pos, is_amino=False):
        """
        msa: list[str]
            Multiple sequence alignment rows.
        pos: int
            Column index.
        is_amino: bool
            True for protein alignment, False for nucleotide alignment.
        """

        seq_idx = self.pick_rows_to_use_in_consensus(msa, pos)

        if self.ignore_trailing_leading_gaps and not seq_idx:
            return self.INVALID_CONS_CHAR

        # -----------------------------
        # NUCLEOTIDE LOGIC
        # -----------------------------
        if not is_amino:
            default_char = " "

            if seq_idx:
                pc = msa[seq_idx[0]][pos]
                n_seq = len(seq_idx)
            else:
                pc = msa[0][pos]
                n_seq = len(msa)

            if pc == self.GAP_CHAR:
                pc = default_char

            for s in range(1, n_seq):
                idx = seq_idx[s] if seq_idx else s
                c = msa[idx][pos]

                if c != pc:
                    pc = default_char
                    break

            return "*" if pc != default_char else default_char

        # -----------------------------
        # AMINO ACID LOGIC
        # -----------------------------
        current_group = []

        n_seq = len(seq_idx) if seq_idx else len(msa)

        for s in range(n_seq):
            idx = seq_idx[s] if seq_idx else s
            c = msa[idx][pos]

            if c not in current_group:
                current_group.append(c)

        # Exact conservation
        if len(current_group) == 1:
            return " " if current_group[0] == self.GAP_CHAR else "*"

        current_len = len(current_group)

        # Strong groups
        if current_len <= self.MAX_STRONG_GROUP_LEN:
            for sgroup in self.STRONG_GROUPS:
                matches = all(c in sgroup for c in current_group)

                if matches:
                    return ":"

        # Weak groups
        if current_len <= self.MAX_WEAK_GROUP_LEN:
            for wgroup in self.WEAK_GROUPS:
                matches = all(c in wgroup for c in current_group)

                if matches:
                    return "."

        return " "

    def pick_rows_to_use_in_consensus(self, msa, pos):
        """
        Placeholder for original UGENE logic.

        Currently returns all row indices.
        """
        return list(range(len(msa)))


# ---------------------------------------------------
# Example usage
# ---------------------------------------------------

msa = [
    "MILV",
    "MILL",
    "MIFV",
]

algo = MsaConsensusAlgorithmClustal()

for i in range(len(msa[0])):
    c = algo.get_consensus_char(msa, i, is_amino=True)
    print(i, c)