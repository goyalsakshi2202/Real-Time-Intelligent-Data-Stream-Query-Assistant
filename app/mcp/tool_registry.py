from typing import Callable, Dict


# Minimal tool registry to decouple MCP host from tool modules
class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable) -> None:
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = handler

    def get(self, name: str) -> Callable:
        return self._tools[name]

    def list_tools(self) -> Dict[str, Callable]:
        return dict(self._tools)


def load_default_tools(registry: ToolRegistry) -> None:
    from app.mcp.tools.query_database import query_database
    from app.mcp.tools.analyze_fraud import analyze_fraud

    registry.register("query_database", query_database)
    registry.register("analyze_fraud", analyze_fraud)

