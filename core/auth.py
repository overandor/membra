from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class AuthContext:
    user_id: str
    tenant_id: str
    role: str
    permissions: set[str]


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "platform_admin": {
        "assets.read",
        "assets.write",
        "campaigns.read",
        "campaigns.write",
        "proofbook.read",
        "proofbook.append",
        "proofbook.verify",
        "wallet.read",
        "wallet.review",
        "billing.read",
        "billing.reconcile",
        "admin.review",
        "tenant.manage",
        "config.manage",
    },
    "reviewer": {
        "assets.read",
        "proofbook.read",
        "proofbook.verify",
        "admin.review",
    },
    "asset_owner": {
        "assets.read",
        "assets.write",
        "campaigns.read",
        "wallet.read",
    },
}



def build_context(user_id: str, tenant_id: str, role: str) -> AuthContext:
    return AuthContext(
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
        permissions=set(ROLE_PERMISSIONS.get(role, set())),
    )



def has_permissions(context: AuthContext, required: Iterable[str]) -> bool:
    required_set = set(required)
    return required_set.issubset(context.permissions)
