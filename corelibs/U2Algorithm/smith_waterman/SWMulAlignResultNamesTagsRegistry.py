SEQ_NAME_PREFIX_LENGTH = 10
SEQ_NAME_PREFIX_TAG_SHORTHAND = "SN"
SEQ_NAME_PREFIX_TAG_LABEL = "Reference sequence name prefix"
PTRN_NAME_PREFIX_TAG_SHORTHAND = "PN"
PTRN_NAME_PREFIX_TAG_LABEL = "Pattern sequence name prefix"

SUBSEQ_START_POS_TAG_SHORTHAND = "S"
SUBSEQ_START_POS_TAG_LABEL = "Subsequence start position"
SUBSEQ_END_POS_TAG_SHORTHAND = "E"
SUBSEQ_END_POS_TAG_LABEL = "Subsequence end position"
SUBSEQ_LENGTH_TAG_SHORTHAND = "L"
SUBSEQ_LENGTH_TAG_LABEL = "Subsequence length"

DATE_TAG_SHORTHAND = "MDY"
DATE_TAG_LABEL = "Date"
TIME_TAG_SHORTHAND = "hms"
TIME_TAG_LABEL = "Time"
COUNTER_TAG_SHORTHAND = "C"
COUNTER_TAG_LABEL = "Counter"

NOT_FOUND_SUBSTR_INDEX = -1



class SWMulAlignResultNamesTagsRegistry:
    def __init__(self):
        self.tags = []

        # Register tags
        self.register_tag(SWMulAlignSeqPrefixTag(SEQ_NAME_PREFIX_TAG_SHORTHAND, SEQ_NAME_PREFIX_TAG_LABEL, SEQ_NAME_PREFIX_LENGTH))
        self.register_tag(SWMulAlignSeqPrefixTag(PTRN_NAME_PREFIX_TAG_SHORTHAND, PTRN_NAME_PREFIX_TAG_LABEL, SEQ_NAME_PREFIX_LENGTH))

        self.register_tag(SWMulAlignSubseqPropTag(SUBSEQ_START_POS_TAG_SHORTHAND, SUBSEQ_START_POS_TAG_LABEL, SWMulAlignSubseqPropTag.START))
        self.register_tag(SWMulAlignSubseqPropTag(SUBSEQ_END_POS_TAG_SHORTHAND, SUBSEQ_END_POS_TAG_LABEL, SWMulAlignSubseqPropTag.END))
        self.register_tag(SWMulAlignSubseqPropTag(SUBSEQ_LENGTH_TAG_SHORTHAND, SUBSEQ_LENGTH_TAG_LABEL, SWMulAlignSubseqPropTag.LENGTH))

        self.register_tag(SWMulAlignExternalPropTag(DATE_TAG_SHORTHAND, DATE_TAG_LABEL, SWMulAlignExternalPropTag.DATE))
        self.register_tag(SWMulAlignExternalPropTag(TIME_TAG_SHORTHAND, TIME_TAG_LABEL, SWMulAlignExternalPropTag.TIME))
        self.register_tag(SWMulAlignExternalPropTag(COUNTER_TAG_SHORTHAND, COUNTER_TAG_LABEL, SWMulAlignExternalPropTag.COUNTER))

    def register_tag(self, tag):
        self.tags.append(tag)


    def get_tags_with_correct_order(self):
        result = [None] * len(self.tags)  # Create a list with None, the size of self.tags
        tag_shorthand_to_index = {
            SEQ_NAME_PREFIX_TAG_SHORTHAND: 0,
            PTRN_NAME_PREFIX_TAG_SHORTHAND: 1,
            SUBSEQ_START_POS_TAG_SHORTHAND: 2,
            SUBSEQ_END_POS_TAG_SHORTHAND: 3,
            SUBSEQ_LENGTH_TAG_SHORTHAND: 4,
            COUNTER_TAG_SHORTHAND: 5,
            DATE_TAG_SHORTHAND: 6,
            TIME_TAG_SHORTHAND: 7
        }

        for tag in self.tags:
            tag_shorthand = tag.get_shorthand()

            # Assign the tag to the correct index based on shorthand
            if tag_shorthand in tag_shorthand_to_index:
                tag_index = tag_shorthand_to_index[tag_shorthand]
                result[tag_index] = tag
            else:
                raise ValueError(f"Unexpected tag shorthand: {tag_shorthand}")

        return result



# Example usage
registry = SWMulAlignResultNamesTagsRegistry()

# Print all registered tags
for tag in registry.tags:
    print(f"Shorthand: {tag.shorthand}, Label: {tag.label}, Type: {tag.prop_type if hasattr(tag, 'prop_type') else 'N/A'}, Length: {getattr(tag, 'length', 'N/A')}")
