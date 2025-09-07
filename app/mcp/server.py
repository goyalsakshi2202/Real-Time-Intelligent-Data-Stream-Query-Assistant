import asyncio
from typing import Any, Dict

from app.mcp.tool_registry import ToolRegistry, load_default_tools


class MCPServer:
    """Minimal placeholder MCP host for local development.

    In production, this will be replaced with a proper MCP-compliant server
    wired to Claude tool-use. For now, we expose a simple async dispatch
    that mimics tool invocation.
    """

    def __init__(self) -> None:
        self.registry = ToolRegistry()
        load_default_tools(self.registry)

    async def call_tool(self, name: str, params: Dict[str, Any]) -> Any:
        handler = self.registry.get(name)
        if asyncio.iscoroutinefunction(handler):
            return await handler(**params)
        return handler(**params)


async def _dev_demo() -> None:
    server = MCPServer()
    # Example dry run call (will no-op with placeholder handlers)
    try:
        res = await server.call_tool("query_database", {"query_type": "account_transactions", "parameters": {"account_id": "demo", "time_range": "7d"}})
        print("query_database =>", str(res)[:160])
    except Exception as e:
        print("Dev demo error:", e)


if __name__ == "__main__":
    asyncio.run(_dev_demo())

