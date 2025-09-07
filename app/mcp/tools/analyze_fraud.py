from typing import Optional

from app.mcp.types.tool_io import FraudAnalyzeInput, FraudAnalysis, FraudIndicator


def analyze_fraud(account_id: Optional[str] = None, transaction_id: Optional[str] = None, time_range: str = "30d") -> dict:
    """Placeholder fraud analysis tool.

    Query-first, context-aware flow will be integrated in the next step by
    calling services.query_engine then services.fraud_engine.
    """
    _ = FraudAnalyzeInput(account_id=account_id, transaction_id=transaction_id, time_range=time_range)
    analysis = FraudAnalysis(
        account_id=account_id,
        total_transactions=0,
        fraud_indicators=[
            FraudIndicator(rule_id="DEMO", name="Demo Only", severity="LOW").model_dump()
        ],
        risk_score=0.0,
        risk_level="LOW",
        context_analysis={},
    )
    return analysis.model_dump()

