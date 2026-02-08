class KalignSupportTask(ExternalToolRunTask):
    """
    Task for running Kalign alignments.
    Inherits from ExternalToolRunTask for generic execution.
    """

    def __init__(self, kalign_tool, input_fasta, output_alignment):
        # Prepare default args for Kalign
        args = ["-i", input_fasta, "-o", output_alignment]

        super().__init__(
            tool=kalign_tool,
            args=args,
            name="Kalign multiple sequence alignment"
        )
