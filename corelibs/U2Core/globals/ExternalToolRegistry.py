class ExternalToolRegistry:
    def __init__(self):
        self._tools = {}

    def register_tool(self, tool: ExternalTool):
        self._tools[tool.id] = tool

    def get_tool(self, tool_id: str) -> Optional[ExternalTool]:
        return self._tools.get(tool_id)

    def detect_tools(self):
        for tool in self._tools.values():
            tool.detect()
