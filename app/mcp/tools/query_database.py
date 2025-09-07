from typing import Dict, Any

from app.mcp.types.tool_io import QueryDatabaseInput, QueryResult


def query_database(query_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder tool: routes to query engine (to be wired next).

    For now, returns a well-formed envelope so downstream pieces can be
    integrated incrementally.
    """
    payload = QueryDatabaseInput(query_type=query_type, parameters=parameters)
    return QueryResult(status="success", source="placeholder", data={
        "query_type": payload.query_type,
        "parameters": payload.parameters,
        "note": "Wire this to services.query_engine.engine in next step"
    }).model_dump()

