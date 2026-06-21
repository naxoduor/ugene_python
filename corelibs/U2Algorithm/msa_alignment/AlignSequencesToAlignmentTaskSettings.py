from dataclasses import dataclass, field
from typing import List, Optional
import copy as pycopy


@dataclass
class AlignSequencesToAlignmentTaskSettings(AbstractAlignmentTaskSettings):
    msaRef: Optional["U2EntityRef"] = None
    alphabet: Optional["U2AlphabetId"] = None

    addedSequencesRefs: List = field(default_factory=list)
    addedSequencesNames: List = field(default_factory=list)

    addAsFragments: bool = False
    reorderSequences: bool = False
    referenceRowId: int = -1
    maxSequenceLength: int = 0

    def __init__(self,
                 msaRef: Optional["U2EntityRef"] = None,
                 newAlphabet: Optional["U2AlphabetId"] = None,
                 addAsFragments: bool = False):
        super().__init__()  # AbstractAlignmentTaskSettings default init

        self.msaRef = msaRef
        self.alphabet = newAlphabet

        self.addedSequencesRefs = []
        self.addedSequencesNames = []

        self.addAsFragments = addAsFragments
        self.reorderSequences = False
        self.referenceRowId = -1
        self.maxSequenceLength = 0

    @classmethod
    def from_existing(cls, s: "AlignSequencesToAlignmentTaskSettings"):
        """Copy constructor equivalent."""
        obj = cls()
        obj.msaRef = s.msaRef
        obj.alphabet = s.alphabet

        obj.addedSequencesRefs = list(s.addedSequencesRefs)
        obj.addedSequencesNames = list(s.addedSequencesNames)

        obj.addAsFragments = s.addAsFragments
        obj.reorderSequences = s.reorderSequences
        obj.referenceRowId = s.referenceRowId
        obj.maxSequenceLength = s.maxSequenceLength

        return obj

    def isValid(self) -> bool:
        return (
            super().isValid()
            and len(self.addedSequencesRefs) > 0
            and len(self.addedSequencesNames) > 0
        )