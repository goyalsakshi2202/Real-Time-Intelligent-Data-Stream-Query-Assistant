from typing import Optional, Dict, Any

from app.mcp.types.tool_io import FraudAnalyzeInput, FraudAnalysis, FraudIndicator
from app.services.query_engine.engine import QueryEngine
from app.services.fraud_engine.engine import FraudEngine


async def analyze_fraud(account_id: Optional[str] = None, transaction_id: Optional[str] = None, time_range: str = "30d") -> Dict[str, Any]:
    """Analyze fraud by first querying transactions, then applying fraud rules.
    
    Flow: QueryEngine → FraudEngine → Analysis Result
    """
    # Step 1: Get transactions using QueryEngine
    query_engine = QueryEngine()
    fraud_engine = FraudEngine()
    
    transactions = []
    
    if account_id:
        # Get all transactions for the account
        transactions = await query_engine.get_account_transactions(account_id, time_range)
    elif transaction_id:
        # Get specific transaction
        transaction = await query_engine.get_transaction_by_id(transaction_id, time_range)
        transactions = [transaction] if transaction else []
    else:
        return {
            "status": "error", 
            "message": "Either account_id or transaction_id is required"
        }
    
    # Step 2: Analyze transactions using FraudEngine
    fraud_analysis = await fraud_engine.analyze(transactions)
    
    # Step 3: Format response
    return {
        "status": "success",
        "source": "fraud_engine",
        "data": {
            "account_id": account_id,
            "transaction_id": transaction_id,
            "time_range": time_range,
            "transaction_count": len(transactions),
            "fraud_analysis": fraud_analysis,
            "transactions_analyzed": transactions
        }
    }

