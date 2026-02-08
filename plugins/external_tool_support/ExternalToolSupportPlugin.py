class ExternalToolSupportPlugin:
    """
    Python analogue of UGENE ExternalToolSupportPlugin
    """

    def __init__(self, registry):
        self.registry = registry
        self.init_external_tools()
        self.init_supports()

    def init_external_tools(self):
        """
        Register all external tools (UGENE plugin phase)
        """
        raise NotImplementedError

    def init_supports(self):
        """
        Register all ExternalToolSupports
        """
        raise NotImplementedError
