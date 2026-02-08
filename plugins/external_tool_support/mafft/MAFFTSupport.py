class MafftSupport(ExternalTool):
    def __init__(self, executable="mafft", version_arg="--version"):
        """
        Wrapper for MAFFT tool.
        """
        super().__init__(id="mafft", name="MAFFT", executable=executable, version_arg=version_arg)

    # Tool-specific method: alignment
    def align(self, input_fasta, output_alignment):
        self.detect()
        if not self.available:
            raise RuntimeError(f"{self.name} is not available")

        # Basic MAFFT command: auto strategy
        args = ["--auto", "-i", input_fasta, "-o", output_alignment]

        # Create task for pipeline integration
        task = MafftSupportTask(
            mafft_tool=self,
            input_fasta=input_fasta,
            output_alignment=output_alignment
        )

        task.prepare()
        task.run()

        # Direct subprocess fallback
        import subprocess
        subprocess.run([self.path] + args, check=True)
