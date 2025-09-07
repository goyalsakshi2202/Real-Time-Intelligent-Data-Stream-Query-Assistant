from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AccountQueryInput(BaseModel):
    account_id: str = Field(..., description="Target account identifier")
    time_range: Optional[str] = Field("30d", description="Lookback window, e.g., 7d, 30d")


class TransactionQueryInput(BaseModel):
    transaction_id: str


class QueryDatabaseInput(BaseModel):
    query_type: str = Field(..., description="account_transactions | transaction_details | custom_sql")
    parameters: Dict[str, Any] = Field(default_factory=dict)


class QueryResult(BaseModel):
    status: str
    source: str
    data: Any


class FraudAnalyzeInput(BaseModel):
    account_id: Optional[str] = None
    transaction_id: Optional[str] = None
    time_range: Optional[str] = "30d"


class FraudIndicator(BaseModel):
    rule_id: str
    name: str
    severity: str
    description: Optional[str] = None


class FraudAnalysis(BaseModel):
    account_id: Optional[str] = None
    total_transactions: int
    fraud_indicators: List[FraudIndicator]
    risk_score: float
    risk_level: str
    context_analysis: Dict[str, Any] = Field(default_factory=dict)

