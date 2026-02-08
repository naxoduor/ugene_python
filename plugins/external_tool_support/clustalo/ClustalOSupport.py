class ClustalSupport(ExternalTool):
    def __init__(self, executable="clustalo", version_arg="--version"):
        """
        Wrapper for Clustal Omega tool.
        """
        # Set id and name here
        super().__init__(id="clustal", name="Clustal Omega", executable=executable, version_arg=version_arg)

    # Tool-specific method: alignment
    def align(self, input_fasta, output_alignment):
        self.detect()
        if not self.available:
            raise RuntimeError(f"{self.name} is not available")

        args = ["-i", input_fasta, "-o", output_alignment]

        # Optional: if you want to force overwrite or specify format
        # args += ["--force", "--outfmt=clu"]  # uncomment if needed

        # Create task for pipeline integration
        task = ClustalSupportTask(
            clustal_tool=self,
            input_fasta=input_fasta,
            output_alignment=output_alignment
        )

        task.prepare()
        task.run()

        # Direct subprocess run (optional fallback)
        import subprocess
        subprocess.run([self.path] + args, check=True)
