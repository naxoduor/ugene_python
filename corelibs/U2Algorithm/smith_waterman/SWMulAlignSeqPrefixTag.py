import re

REG_EXP_PATTERN_FOR_WORDS_SEPARATORS = r"\s|_"


class SWMulAlignSeqPrefixTag:
    def __init__(self, prefix_length: int):
        self.prefixLength = prefix_length

    def expand_tag(self, argument: str) -> str:
        assert isinstance(argument, str)
        seq_name = argument
        assert seq_name

        # Consider only the prefix range
        prefix_end = self.prefixLength - 1
        prefix_slice = seq_name[: self.prefixLength]

        # Find all separators in the prefix slice
        matches = list(re.finditer(REG_EXP_PATTERN_FOR_WORDS_SEPARATORS, prefix_slice))

        if matches:
            last_word_end_position = matches[-1].start()
        else:
            last_word_end_position = prefix_end

        return seq_name[:last_word_end_position]
