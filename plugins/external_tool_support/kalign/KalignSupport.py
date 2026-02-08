class KalignSupport(ExternalTool):
    def __init__(self, executable="kalign", version_arg="--version"):
        # Set id and name here
        super().__init__(id="kalign", name="Kalign", executable=executable, version_arg=version_arg)

    # Tool-specific method: alignment
    def align(self, input_fasta, output_alignment):
        self.detect()
        if not self.available:
            raise RuntimeError(f"{self.name} is not available")

        args = ["-i", input_fasta, "-o", output_alignment]

        task = KalignSupportTask(
        kalign_tool=kalign,
        input_fasta="input.fasta",
        output_alignment="aligned.aln")

        task.prepare()
        task.run()


        import subprocess
        subprocess.run([self.path] + args, check=True)
