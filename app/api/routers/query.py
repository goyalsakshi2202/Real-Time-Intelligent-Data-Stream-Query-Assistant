from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from app.mcp.server import MCPServer

router = APIRouter()
_server = MCPServer()

class QueryReq(BaseModel):
    query_type: str = Field(..., description="Type of query: account_transactions, transaction_details, or transaction_by_date_range")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")

class FraudAnalyzeReq(BaseModel):
    account_id: Optional[str] = Field(None, description="Account ID to analyze")
    transaction_id: Optional[str] = Field(None, description="Specific transaction ID to analyze")
    time_range: str = Field("30d", description="Time range for analysis (e.g., 7d, 30d)")

@router.post("/query")
async def run_query(req: QueryReq):
    """Query transactions from the database."""
    try:
        # Validate query_type
        valid_query_types = ["account_transactions", "transaction_details", "transaction_by_date_range"]
        if req.query_type not in valid_query_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid query_type. Must be one of: {valid_query_types}"
            )
        
        # Validate required parameters based on query_type
        if req.query_type == "account_transactions":
            if "account_id" not in req.parameters:
                raise HTTPException(
                    status_code=400,
                    detail="account_id is required for account_transactions query"
                )
            # Validate pagination parameters
            if "limit" in req.parameters:
                try:
                    limit = int(req.parameters["limit"])
                    if limit < 1 or limit > 1000:
                        raise HTTPException(
                            status_code=400,
                            detail="limit must be between 1 and 1000"
                        )
                except (ValueError, TypeError):
                    raise HTTPException(
                        status_code=400,
                        detail="limit must be a valid integer"
                    )
            if "offset" in req.parameters:
                try:
                    offset = int(req.parameters["offset"])
                    if offset < 0:
                        raise HTTPException(
                            status_code=400,
                            detail="offset must be >= 0"
                        )
                except (ValueError, TypeError):
                    raise HTTPException(
                        status_code=400,
                        detail="offset must be a valid integer"
                    )
        elif req.query_type == "transaction_details":
            if "transaction_id" not in req.parameters:
                raise HTTPException(
                    status_code=400,
                    detail="transaction_id is required for transaction_details query"
                )
        elif req.query_type == "transaction_by_date_range":
            if "start_date" not in req.parameters or "end_date" not in req.parameters:
                raise HTTPException(
                    status_code=400,
                    detail="start_date and end_date are required for transaction_by_date_range query"
                )
        
        return await _server.call_tool("query_database", req.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/analyze")
async def analyze_fraud(req: FraudAnalyzeReq):
    """Analyze fraud for an account or specific transaction."""
    try:
        # Validate input
        if not req.account_id and not req.transaction_id:
            raise HTTPException(
                status_code=400,
                detail="Either account_id or transaction_id is required"
            )
        
        # Validate time_range format
        if req.time_range:
            import re
            if not re.match(r'^\d+[dh]$', req.time_range):
                raise HTTPException(
                    status_code=400,
                    detail="time_range must be in format 'Nd' (days) or 'Nh' (hours), e.g., '7d', '24h'"
                )
        
        return await _server.call_tool("analyze_fraud", req.model_dump())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")