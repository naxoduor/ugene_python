from typing import List

# ---------------------------------------------------------------------------
# Constants and Character Groups
# ---------------------------------------------------------------------------
BASE_DNA_CHARS = "ACGTU"
EXT_DNA_CHARS_ONE_OF_TWO = "WRMKYS"
EXT_DNA_CHARS_ONE_OF_THREE = "BVHD"
EXT_DNA_CHARS_ONE_OF_FOUR = "N"
ALL_EXT_DNA_CHARACTERS = BASE_DNA_CHARS + EXT_DNA_CHARS_ONE_OF_TWO + EXT_DNA_CHARS_ONE_OF_THREE + EXT_DNA_CHARS_ONE_OF_FOUR

GROUP1_LAST_IDX = len(BASE_DNA_CHARS) - 1
GROUP2_LAST_IDX = GROUP1_LAST_IDX + len(EXT_DNA_CHARS_ONE_OF_TWO)
GROUP3_LAST_IDX = GROUP2_LAST_IDX + len(EXT_DNA_CHARS_ONE_OF_THREE)

def get_character_group(idx: int) -> int:
    if idx <= GROUP1_LAST_IDX:
        return 0
    elif idx <= GROUP2_LAST_IDX:
        return 1
    elif idx <= GROUP3_LAST_IDX:
        return 2
    else:
        return 3

# ---------------------------------------------------------------------------
# DNA Masks
# ---------------------------------------------------------------------------
class DnaExtMask:
    NoneMask = 0
    A = 1 << 0
    C = 1 << 1
    G = 1 << 2
    T = 1 << 3
    U = T
    W = A | T
    R = A | G
    M = A | C
    K = T | G
    Y = T | C
    S = G | C
    B = C | G | T
    V = A | C | G
    H = A | C | T
    D = A | G | T
    N = A | C | G | T

# Map character to mask
CHAR_2_MASK = {c: DnaExtMask.NoneMask for c in map(chr, range(256))}
CHAR_2_MASK.update({
    'A': DnaExtMask.A,
    'C': DnaExtMask.C,
    'G': DnaExtMask.G,
    'T': DnaExtMask.T,
    'U': DnaExtMask.U,
    'W': DnaExtMask.W,
    'R': DnaExtMask.R,
    'M': DnaExtMask.M,
    'K': DnaExtMask.K,
    'Y': DnaExtMask.Y,
    'S': DnaExtMask.S,
    'B': DnaExtMask.B,
    'V': DnaExtMask.V,
    'H': DnaExtMask.H,
    'D': DnaExtMask.D,
    'N': DnaExtMask.N,
})

# Create mask to character mapping
MASK_2_CHAR = [None] * 16
for c, mask in CHAR_2_MASK.items():
    if 0 <= mask < len(MASK_2_CHAR):
        MASK_2_CHAR[mask] = c

# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------
def register_hit(data: List[int], c: str):
    """Increment frequency table according to Levitsky extended DNA rules."""
    idx = ord(c)
    data[idx] += 1

    if c == 'A':
        for x in "WRMVHD":
            data[ord(x)] += 1
    elif c == 'C':
        for x in "MYSBVHN":
            data[ord(x)] += 1
    elif c == 'G':
        for x in "RKSBVDN":
            data[ord(x)] += 1
    elif c in 'TU':
        for x in "WKYBHDN":
            data[ord(x)] += 1

def merge_chars_into_mask(chars: str) -> int:
    """Combine multiple DNA chars into a single mask."""
    mask = 0
    for c in chars:
        mask |= CHAR_2_MASK.get(c, 0)
    return mask

# ---------------------------------------------------------------------------
# Algorithm Factory (metadata)
# ---------------------------------------------------------------------------
class MsaConsensusAlgorithmFactoryLevitsky:
    def __init__(self):
        self.name = "Levitsky"
        self.description = (
            "The algorithm proposed by Victor Levitsky to work with DNA alignments.\n"
            "Collects global alignment frequency for every symbol using extended (15 symbols) DNA alphabet first.\n"
            "For every column selects the most rare symbol in the whole alignment with percentage in the column "
            "greater or equals to the threshold value."
        )
        self.min_threshold = 50
        self.max_threshold = 100
        self.default_threshold = 90
        self.threshold_suffix = "%"
        self.is_sequence_like_result_flag = True

    def create_algorithm(self, msa, ignore_trailing_leading_gaps=False):
        return MsaConsensusAlgorithmLevitsky(self, msa, ignore_trailing_leading_gaps)

# ---------------------------------------------------------------------------
# Consensus Algorithm Skeleton
# ---------------------------------------------------------------------------
class MsaConsensusAlgorithmLevitsky:
    def __init__(self, factory: MsaConsensusAlgorithmFactoryLevitsky, msa, ignore_trailing_leading_gaps: bool):
        self.factory = factory
        self.ignore_trailing_leading_gaps = ignore_trailing_leading_gaps
        self.global_freqs = [0] * 256
        self.reinitialize_data(msa)

    def reinitialize_data(self, msa):
        """Compute global frequencies for all characters in the MSA."""
        for row in msa:
            for c in row:
                register_hit(self.global_freqs, c)

# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Mock multiple sequence alignment as list of strings
    msa = [
        "ATGC",
        "AAGC",
        "ATCC",
    ]

    factory = MsaConsensusAlgorithmFactoryLevitsky()
    algo = factory.create_algorithm(msa)
    print("Global frequencies:", algo.global_freqs[:ord('Z')+1])
