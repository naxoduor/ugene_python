# NOTE: This is a structural translation. It assumes Python bindings for:
#   bam_lplbuf_init, bam_lplbuf_reset, bam_lplbuf_push, bam_lplbuf_destroy,
#   bcf_call_init, bcf_call_destroy, bcf_call_glfgen,
#   seq_nt16_table, seq_nt16_str
# and UGENE-like types: U2Region, U2OpStatus, U2DbiIterator, U2AssemblyRead.

class AssemblyConsensusAlgorithmFactorySamtools:
    def __init__(self):
        super().__init__("SAMTOOLS_ALGO")

    def getName(self) -> str:
        return "SAMtools"

    def getDescription(self) -> str:
        return "Uses SAMtools to calculate consensus with regard to quality of reads"

    def createAlgorithm(self):
        return AssemblyConsensusAlgorithmSamtools(self)


class AlgorithmInternal:
    def __init__(self, region, reference_fragment: bytes, os):
        self.region = region
        self.os = os
        self.reference_fragment = reference_fragment
        self.result = bytearray([AssemblyConsensusAlgorithm.EMPTY_CHAR] * region.length)

        self.lplbuf = bam_lplbuf_init(AlgorithmInternal.processBaseCallback, self)
        bam_lplbuf_reset(self.lplbuf)

        self.bca = bcf_call_init(0.83, 13)

    def processReads(self, reads):
        samtools_reads = ReadsContainer()

        self.os.setDescription("Fetching reads from database and converting to SAMtools format")
        SamtoolsAdapter.reads2samtools(reads, self.os, samtools_reads)
        if self.os.isCoR():
            return

        self.os.setDescription("Sorting reads")
        samtools_reads.sortByStartPos()

        self.os.setDescription("Calculating consensus")
        reads_count = samtools_reads.size()
        for i in range(reads_count):
            bam_lplbuf_push(samtools_reads[i], self.lplbuf)
            self.os.setProgress(i * 100 // reads_count)
            if self.os.isCoR():
                return

        bam_lplbuf_push(None, self.lplbuf)

    def processBase(self, tid, pos, n, pl):
        if pos < self.region.startPos or pos >= self.region.endPos() or self.os.isCoR():
            return

        pos_in_array = pos - self.region.startPos

        # From bam_tview.c, tv_pl_func function
        call = 0
        bcr = bcf_callret1_t()

        rb = ord('N')
        if self.reference_fragment:
            rb = self.reference_fragment[pos_in_array]

        qsum = [0, 0, 0, 0]
        prior = 30.0

        bcf_call_glfgen(n, pl, seq_nt16_table[rb], self.bca, bcr)

        for i in range(4):
            qsum[i] = (int(bcr.qsum[i]) << 2) | i

        # insertion sort, descending
        for i in range(1, 4):
            j = i
            while j > 0 and qsum[j] > qsum[j - 1]:
                qsum[j], qsum[j - 1] = qsum[j - 1], qsum[j]
                j -= 1

        a1 = qsum[0] & 3
        a2 = qsum[1] & 3

        p0 = bcr.p[a1 * 5 + a1]
        p1 = bcr.p[a1 * 5 + a2] + prior
        p2 = bcr.p[a2 * 5 + a2]

        rb_upper = chr(rb).upper()
        if "ACGT"[a1] != rb_upper:
            p0 += prior + 3
        if "ACGT"[a2] != rb_upper:
            p2 += prior + 3

        if p0 < p1 and p0 < p2:
            call = ((1 << a1) << 16) | int((min(p1, p2) - p0) + 0.499)
        elif p2 < p1 and p2 < p0:
            call = ((1 << a2) << 16) | int((min(p0, p1) - p2) + 0.499)
        else:
            call = ((1 << a1) | (1 << a2)) << 16 | int((min(p0, p2) - p1) + 0.499)

        consensus_char = seq_nt16_str[(call >> 16) & 0xF]
        self.result[pos_in_array] = ord(consensus_char)

    @staticmethod
    def processBaseCallback(tid, pos, n, pl, data):
        algorithm = data
        algorithm.processBase(tid, pos, n, pl)
        return 0

    def getResult(self) -> bytes:
        return bytes(self.result)

    def __del__(self):
        bcf_call_destroy(self.bca)
        bam_lplbuf_destroy(self.lplbuf)


class AssemblyConsensusAlgorithmSamtools(AssemblyConsensusAlgorithm):
    def getConsensusRegion(self, region, reads, reference_fragment: bytes, os):
        algorithm = AlgorithmInternal(region, reference_fragment, os)
        algorithm.processReads(reads)
        return algorithm.getResult()