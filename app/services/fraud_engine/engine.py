from typing import List, Dict, Any
from datetime import datetime


class FraudEngine:
    async def analyze(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze fraud for an account or transaction."""

        if not transactions:
            return {
                "risk_level": "LOW",
                "score": 0.0,
                "reasoning": "No transactions to analyze",
                "flags": []
            }

        risk_score = 0.0
        flags = []

        # Rule 1: High amount transactions
        high_amount_count = sum(1 for txn in transactions if txn.get("amount", 0) > 1000)
        if high_amount_count > 0:
            risk_score += high_amount_count * 0.3
            flags.append(f"{high_amount_count} high-amount transactions (>$1000)")
        
        # Rule 2: Failed payments
        failed_count = sum(1 for txn in transactions if txn.get("payment_success") == 0)
        if failed_count > 0:
            risk_score += failed_count * 0.4
            flags.append(f"{failed_count} failed payment attempts")
        
        # Rule 3: Multiple locations in short time
        locations = set(txn.get("location", "") for txn in transactions)
        if len(locations) > 2:
            risk_score += 0.3
            flags.append(f"Transactions from {len(locations)} different locations")
        
        # Rule 4: E-commerce transactions (higher risk)
        ecom_count = sum(1 for txn in transactions if txn.get("transaction_type") == "ECOM")
        if ecom_count > 0:
            risk_score += ecom_count * 0.2
            flags.append(f"{ecom_count} e-commerce transactions")
        
        # Determine risk level
        if risk_score >= 1.0:
            risk_level = "HIGH"
        elif risk_score >= 0.5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "risk_level": risk_level,
            "score": round(risk_score, 2),
            "reasoning": f"Risk assessment based on {len(transactions)} transactions",
            "flags": flags,
            "transaction_count": len(transactions)
        }
