from typing import Dict, Any
from datetime import datetime

from app.mcp.types.tool_io import QueryDatabaseInput, QueryResult
from app.services.query_engine.engine import QueryEngine


async def query_database(query_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder tool: routes to query engine (to be wired next).

    For now, returns a well-formed envelope so downstream pieces can be
    integrated incrementally.
    """
    payload = QueryDatabaseInput(query_type=query_type, parameters=parameters)
    if payload.query_type == "account_transactions":
        account_id = payload.parameters.get("account_id")
        time_range = payload.parameters.get("time_range", "30d")
        limit = payload.parameters.get("limit", 100)
        offset = payload.parameters.get("offset", 0)
        data = await QueryEngine().get_account_transactions(account_id, time_range, limit, offset)
        return {"status": "success", "source": "query_engine", "data": data}

    if payload.query_type == "transaction_details":
        transaction_id = payload.parameters.get("transaction_id")
        time_range = payload.parameters.get("time_range")
        data = await QueryEngine().get_transaction_by_id(transaction_id, time_range)
        return {"status": "success", "source": "query_engine", "data": data}

    if payload.query_type == "transaction_by_date_range":
        start_date_str = payload.parameters.get("start_date")
        end_date_str = payload.parameters.get("end_date")
        
        # Convert string dates to datetime objects
        try:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return {"status": "error", "message": "Invalid date format. Use ISO format like '2025-01-01T00:00:00Z'"}
        
        data = await QueryEngine().get_transaction_by_date_range(start_date, end_date)
        return {"status": "success", "source": "query_engine", "data": data}

    return {"status": "error", "source": "query_engine", "data": "Invalid query type" , "message" : "Unknown query type: " + payload.query_type}

