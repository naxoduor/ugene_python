class MafftSupportTask(ExternalToolRunTask):
    """
    Task for running MAFFT alignments.
    Inherits from ExternalToolRunTask for generic execution.
    """

    def __init__(self, mafft_tool, input_fasta, output_alignment):
        args = ["--auto", "-i", input_fasta, "-o", output_alignment]

        super().__init__(
            tool=mafft_tool,
            args=args,
            name="MAFFT multiple sequence alignment"
        )
