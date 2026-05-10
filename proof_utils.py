"""
MEMBRA Proof Hash Utilities
Standard proof hashing and Devnet memo generation for ProofBook.
"""

import hashlib
import json
from typing import Any


def canonical_json(data: dict[str, Any]) -> str:
    """
    Convert a dictionary to canonical JSON string.
    Ensures consistent hashing across different JSON serializers.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def proof_hash(proof_json: dict[str, Any]) -> str:
    """
    Generate SHA-256 proof hash from proof JSON.
    This hash is used as the canonical identifier for proof records.
    """
    payload = canonical_json(proof_json)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def memo_payload(entry_id: str, hash_value: str) -> str:
    """
    Generate Devnet memo transaction payload.
    Format: MEMBRA:v1:proofbook:{entry_id}:{hash_value}
    """
    return f"MEMBRA:v1:proofbook:{entry_id}:{hash_value}"


def devnet_explorer_url(signature: str) -> str:
    """
    Generate Solana Devnet explorer URL for a transaction signature.
    """
    return f"https://explorer.solana.com/tx/{signature}?cluster=devnet"


def mainnet_explorer_url(signature: str) -> str:
    """
    Generate Solana Mainnet explorer URL for a transaction signature.
    """
    return f"https://explorer.solana.com/tx/{signature}"


def verify_proof_hash(proof_json: dict[str, Any], expected_hash: str) -> bool:
    """
    Verify that a proof JSON matches an expected hash.
    """
    computed_hash = proof_hash(proof_json)
    return computed_hash == expected_hash
