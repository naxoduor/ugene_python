class ExternalToolRegistry:
    def __init__(self):
        # Maps lowercase tool IDs to ExternalTool objects
        self.tool_by_lowercase_id_map = {}
        # Event listeners (simple Python callback approach)
        self.on_tool_added_listeners = []
        self.on_tool_about_to_be_removed_listeners = []

    # ---------- Event subscription ----------
    def on_tool_added(self, callback):
        """Register a callback for tool added events."""
        self.on_tool_added_listeners.append(callback)

    def on_tool_about_to_be_removed(self, callback):
        """Register a callback for tool removal events."""
        self.on_tool_about_to_be_removed_listeners.append(callback)

    # ---------- Register a tool ----------
    def register_entry(self, tool):
        """
        Add a new tool to the registry.

        Args:
            tool: ExternalTool instance

        Returns:
            bool: True if registered successfully, False if ID already exists
        """
        tool_id = tool.get_id()
        lower_id = tool_id.lower()
        if lower_id in self.tool_by_lowercase_id_map:
            return False  # Already registered

        self.tool_by_lowercase_id_map[lower_id] = tool

        # Emit event
        for callback in self.on_tool_added_listeners:
            callback(tool_id)

        return True

    # ---------- Unregister a tool ----------
    def unregister_entry(self, tool_id):
        """
        Remove a tool from the registry.

        Args:
            tool_id (str): ID of the tool to remove

        Raises:
            KeyError: If tool ID does not exist
        """
        lower_id = tool_id.lower()
        if lower_id not in self.tool_by_lowercase_id_map:
            raise KeyError(f"Tool ID '{tool_id}' not found")

        # Emit event before deletion
        for callback in self.on_tool_about_to_be_removed_listeners:
            callback(tool_id)

        # Remove the tool
        del self.tool_by_lowercase_id_map[lower_id]
