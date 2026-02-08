class SWMulAlignSubseqPropTag:
    def __init__(self, pos_type):
        self.pos_type = pos_type

    def expand_tag(self, argument):
        # Equivalent to: assert(argument.canConvert<U2Region>())
        assert isinstance(argument, U2Region)

        subsequence = argument

        if self.pos_type == PosType.START:
            tag_expansion = subsequence.start_pos + 1
        elif self.pos_type == PosType.END:
            tag_expansion = subsequence.end_pos()
        elif self.pos_type == PosType.LENGTH:
            tag_expansion = subsequence.length
        else:
            raise AssertionError("Invalid pos_type")

        # Equivalent to QString::number(tagExpansion)
        return str(tag_expansion)



from enum import Enum

class PosType(Enum):
    START = 1
    END = 2
    LENGTH = 3


class U2Region:
    def __init__(self, start_pos: int, length: int):
        self.start_pos = start_pos
        self.length = length

    def end_pos(self):
        return self.start_pos + self.length
