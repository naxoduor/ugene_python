import subprocess

class ExternalToolRunTask:
    """
    Generic task for running an ExternalTool executable.
    """

    def __init__(self, tool, args=None, name=None):
        """
        :param tool: An instance of ExternalTool (or similar)
        :param args: List of command-line arguments
        :param name: Optional task name for logging/debug
        """
        self.tool = tool
        self.args = args or []
        self.name = name or f"Run {tool.name}"
        self.available = False

    def prepare(self):
        """
        Detect tool availability and prepare arguments.
        """
        self.tool.detect()
        self.available = self.tool.available
        if not self.available:
            raise RuntimeError(f"{self.tool.name} is not available")

    def run(self, capture_output=False):
        """
        Execute the external tool with prepared arguments.

        :param capture_output: If True, return stdout as string
        :return: CompletedProcess if capture_output, else None
        """
        if not self.available:
            raise RuntimeError(f"{self.tool.name} is not available")

        cmd = [self.tool.path] + self.args

        try:
            if capture_output:
                result = subprocess.run(
                    cmd, check=True, capture_output=True, text=True
                )
                return result.stdout
            else:
                subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Execution of {self.tool.name} failed with code {e.returncode}"
            ) from e
