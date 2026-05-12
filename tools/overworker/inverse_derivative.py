"""Inverse derivative - tokenizes appraised endpoints into inverse derivatives."""
import hashlib
import json
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DerivativeToken:
    token_id: str
    underlying_endpoint: str
    inverse_value: float
    collateral_ratio: float
    maturity_date: str
    strike_price: float
    metadata: Dict


@dataclass
class DerivativePortfolio:
    tokens: List[DerivativeToken]
    total_notional: float
    weighted_inverse_value: float
    risk_score: float
    metadata: Dict


class InverseDerivativeEngine:
    def __init__(self):
        self.collateral_ratio = 0.5
        self.maturity_days = 30
    
    def create_inverse_derivatives(self, e_service_appraisal) -> DerivativePortfolio:
        tokens = [self._create_derivative_token(e) for e in e_service_appraisal.endpoints]
        total_notional = sum(t.inverse_value for t in tokens)
        weighted_inverse = sum(t.inverse_value * t.collateral_ratio for t in tokens)
        risk_score = self._compute_portfolio_risk(tokens)
        return DerivativePortfolio(
            tokens=tokens, total_notional=total_notional,
            weighted_inverse_value=weighted_inverse, risk_score=risk_score,
            metadata={"total_tokens": len(tokens), "avg_maturity_days": self.maturity_days, "collateral_requirement": self.collateral_ratio}
        )
    
    def _create_derivative_token(self, appraised_endpoint) -> DerivativeToken:
        token_id = hashlib.sha256(f"{appraised_endpoint.path}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        inverse_value = 1.0 / (appraised_endpoint.appraisal_value + 0.01)
        strike_price = appraised_endpoint.appraisal_value * 1.1
        from datetime import timedelta
        maturity_date = (datetime.utcnow() + timedelta(days=self.maturity_days)).isoformat()
        return DerivativeToken(
            token_id=token_id, underlying_endpoint=appraised_endpoint.path,
            inverse_value=inverse_value, collateral_ratio=self.collateral_ratio,
            maturity_date=maturity_date, strike_price=strike_price,
            metadata={"endpoint_category": appraised_endpoint.category.value, "complexity_score": appraised_endpoint.complexity_score, "liquidity_score": appraised_endpoint.liquidity_score, "method": appraised_endpoint.method.value}
        )
    
    def _compute_portfolio_risk(self, tokens):
        if not tokens: return 0.0
        unique_endpoints = len(set(t.underlying_endpoint for t in tokens))
        concentration = 1.0 - (unique_endpoints / len(tokens))
        inverse_values = [t.inverse_value for t in tokens]
        avg = sum(inverse_values) / len(inverse_values)
        variance = sum((v - avg) ** 2 for v in inverse_values) / len(inverse_values)
        volatility = min(variance / 10, 1.0)
        avg_collateral = sum(t.collateral_ratio for t in tokens) / len(tokens)
        collateral_risk = 1.0 - avg_collateral
        return min(concentration * 0.4 + volatility * 0.3 + collateral_risk * 0.3, 1.0)
    
    def compute_derivative_pricing(self, portfolio):
        if not portfolio.tokens: return {}
        fair_value = portfolio.total_notional * (1 - portfolio.risk_score * 0.2)
        required_collateral = portfolio.total_notional * self.collateral_ratio
        leverage = portfolio.total_notional / required_collateral if required_collateral > 0 else 0
        expected_return = (1 - portfolio.risk_score) * 0.15
        return {
            "fair_value": fair_value, "required_collateral": required_collateral,
            "leverage_ratio": leverage, "expected_return": expected_return,
            "risk_adjusted_return": expected_return * (1 - portfolio.risk_score),
            "notional_value": portfolio.total_notional
        }
    
    def export_derivative_manifest(self, portfolio):
        manifest = {
            "version": "1.0", "type": "inverse_derivative_portfolio",
            "created_at": datetime.utcnow().isoformat(),
            "portfolio": {
                "total_tokens": len(portfolio.tokens),
                "total_notional": portfolio.total_notional,
                "weighted_inverse_value": portfolio.weighted_inverse_value,
                "risk_score": portfolio.risk_score,
                "tokens": [{"token_id": t.token_id, "underlying_endpoint": t.underlying_endpoint, "inverse_value": t.inverse_value, "collateral_ratio": t.collateral_ratio, "maturity_date": t.maturity_date, "strike_price": t.strike_price, "metadata": t.metadata} for t in portfolio.tokens]
            },
            "pricing": self.compute_derivative_pricing(portfolio),
            "metadata": portfolio.metadata
        }
        return json.dumps(manifest, indent=2)
