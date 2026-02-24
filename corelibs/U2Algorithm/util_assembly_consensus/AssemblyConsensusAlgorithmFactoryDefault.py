# Python translation of AssemblyConsensusAlgorithmDefault.cpp
# Assumes UGENE-like classes/types exist in Python:
#   U2Region, U2DbiIterator[U2AssemblyRead], U2OpStatus,
#   U2AssemblyReadIterator, AssemblyBasesFrequenciesStat,
#   U2AssemblyBasesFrequenciesInfo, AssemblyConsensusAlgorithm, etc.

class AssemblyConsensusAlgorithmFactoryDefault(AssemblyConsensusAlgorithmFactory):
    def __init__(self):
        super().__init__(BuiltInAssemblyConsensusAlgorithms.DEFAULT_ALGO)

    def getName(self) -> str:
        return "Default"

    def getDescription(self) -> str:
        return "Returns simply the most frequent base and 'N' are no reads intersecting this position"

    def createAlgorithm(self):
        return AssemblyConsensusAlgorithmDefault(self)


class AssemblyConsensusAlgorithmDefault(AssemblyConsensusAlgorithm):
    def getConsensusRegion(self, region, reads, reference_fragment, os):
        s = AssemblyBasesFrequenciesStat()
        s.frequencyInfos.resize(region.length)

        while reads.hasNext():
            r = reads.next()
            read_region = U2Region(r.leftmostPos, r.effectiveLen)
            read_cropped_region = read_region.intersect(region)

            offset_in_read = read_cropped_region.startPos - read_region.startPos
            offset_in_array = read_cropped_region.startPos - region.startPos
            length = read_cropped_region.length

            read_iterator = U2AssemblyReadIterator(r.readSequence, r.cigar, offset_in_read)

            for i in range(int(length)):
                fi = s.frequencyInfos[int(offset_in_array + i)]
                if read_iterator.hasNext():
                    c = read_iterator.nextLetter()
                    fi.addToCharFrequency(c)
                else:
                    break

            if os.isCoR():
                break

        return s.getConsensusFragment()