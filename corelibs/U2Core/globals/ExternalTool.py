class ExternalTool:
    def __init__(self, id: str, name: str, executable: str, version_arg: str = "--version"):
        self.id = id
        self.name = name
        self.executable = executable
        self.version_arg = version_arg
        self.path = None
        self.version = None
        self.available = False

    def detect(self):
        import shutil
        import subprocess
        self.path = shutil.which(self.executable)
        self.available = self.path is not None
        if self.available:
            try:
                result = subprocess.run(
                    [self.executable, self.version_arg],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                self.version = result.stdout.strip().splitlines()[0]
            except Exception:
                self.version = None
