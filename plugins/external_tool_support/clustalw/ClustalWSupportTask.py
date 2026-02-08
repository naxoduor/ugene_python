class ClustalSupportTask(ExternalToolRunTask):
    """
    Task for running Clustal Omega alignments.
    Inherits from ExternalToolRunTask for generic execution.
    """

    def __init__(self, clustal_tool, input_fasta, output_alignment):
        # Prepare default args for Clustal Omega
        args = ["-i", input_fasta, "-o", output_alignment]

        super().__init__(
            tool=clustal_tool,
            args=args,
            name="Clustal Omega multiple sequence alignment"
        )
