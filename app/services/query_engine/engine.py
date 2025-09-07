from datetime import datetime, timedelta
from typing import List, Dict, Any


def _parse_time_range_to_start(time_range: str) -> datetime:
    """Convert a shorthand like '7d', '30d', '12h' into a UTC start datetime.

    Defaults to 30 days if parsing fails.
    """
    now = datetime.utcnow()
    try:
        unit = time_range[-1]
        amount = int(time_range[:-1])
        if unit == "d":
            return now - timedelta(days=amount)
        if unit == "h":
            return now - timedelta(hours=amount)
    except Exception:
        pass
    return now - timedelta(days=30)


class QueryEngine:
    async def get_account_transactions(self, account_id: str, time_range: str = "30d", limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Return a paginated list of stub transactions for an account.

        Phase 1 stub: later this will call Hive/DB2 DAOs and normalize results.
        """
        start = _parse_time_range_to_start(time_range)
        base = start.replace(minute=0, second=0, microsecond=0)

        # Generate more transactions for pagination demo
        all_transactions = []
        for i in range(10):  # Generate 10 transactions for demo
            all_transactions.append({
                "transaction_id": f"TXN-{i+1:03d}",
                "account_id": account_id,
                "timestamp": (base + timedelta(hours=i+1)).isoformat() + "Z",
                "amount": 100.00 + (i * 50.00),
                "payment_success": 1 if i != 3 else 0,  # TXN-004 fails
                "status": "COMPLETED" if i != 3 else "FAILED",
                "merchant": f"Store {chr(65 + i)}",  # Store A, B, C, etc.
                "location": ["NY", "CA", "TX", "FL", "WA", "IL", "GA", "OH", "NC", "MI"][i],
                "transaction_type": "ECOM" if i % 2 == 0 else "POS",
                "source": "stub:hive" if i % 2 == 0 else "stub:db2",
            })
        
        # Apply pagination
        return all_transactions[offset:offset + limit]

    async def get_transaction_by_id(self, transaction_id: str, time_range: str ='30d') -> Dict[str, Any]:
        """Return a transaction by id. Lists the details of the transactions
            """
        start = _parse_time_range_to_start(time_range)
        base = start.replace(minute=0, second=0, microsecond=0)

        return {
                "transaction_id": transaction_id,
                "account_id": "1234567890",
                "timestamp": (base + timedelta(hours=1)).isoformat() + "Z",
                "amount": 125.50,
                "payment_success": 1,
                "status": "COMPLETED",
                "merchant": "Store A",
                "location": "NY",
                "transaction_type": "POS",
                "source": "stub:hive",
                }

    async def get_transaction_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Return a list of transactions by date range.
        """
        base = start_date.replace(minute=0, second=0, microsecond=0)

        return [
            {
                "transaction_id": "TXN-001",
                "account_id": "1234567890",
                "timestamp": (base + timedelta(hours=1)).isoformat() + "Z",
                "amount": 125.50,
                "payment_success": 1,
                "status": "COMPLETED",
                "merchant": "Store A",
                "location": "NY",
                "transaction_type": "POS",
                "source": "stub:hive",
            },
            {
                "transaction_id": "TXN-002",
                "account_id": "1234567890",
                "timestamp": (base + timedelta(hours=2)).isoformat() + "Z",
                "amount": 4800.00,
                "payment_success": 1,
                "status": "COMPLETED",
                "merchant": "Online Shop",
                "location": "CA",
                "transaction_type": "ECOM",
                "source": "stub:db2",
            },
            {
                "transaction_id": "TXN-003",
                "account_id": "1234567890",
                "timestamp": (base + timedelta(hours=3)).isoformat() + "Z",
                "amount": 75.25,
                "payment_success": 0,
                "status": "FAILED",
                "merchant": "Gas Station",
                "location": "TX",
                "transaction_type": "POS",
                "source": "stub:hive",
            },
            {
                "transaction_id": "TXN-004",
                "account_id": "1234567890",
                "timestamp": (base + timedelta(hours=4)).isoformat() + "Z",
                "amount": 2500.00,
                "payment_success": 1,
                "status": "COMPLETED",
                "merchant": "Electronics Store",
                "location": "FL",
                "transaction_type": "ECOM",
                "source": "stub:db2",
            }
        ]