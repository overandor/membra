"""
MEMBRA Proof Hash Utilities

Provides proof hash generation, memo payload construction, and mainnet explorer URL generation.
"""

import hashlib
import json


def proof_hash(proof_json: dict) -> str:
    """
    Generate SHA-256 hash of canonical proof JSON.
    
    Args:
        proof_json: Dictionary containing proof data
        
    Returns:
        Hexadecimal SHA-256 hash
    """
    payload = json.dumps(proof_json, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def memo_payload(entry_id: str, hash_value: str) -> str:
    """
    Construct memo payload for Solana mainnet transaction.
    
    The memo format: MEMBRA:v1:proofbook:<entry_id>:<sha256_hash>
    
    Args:
        entry_id: Unique identifier for the ProofBook entry
        hash_value: SHA-256 hash of the proof JSON
        
    Returns:
        Memo payload string
    """
    return f"MEMBRA:v1:proofbook:{entry_id}:{hash_value}"


def mainnet_explorer_url(signature: str) -> str:
    """
    Generate Solana mainnet explorer URL for a transaction signature.
    
    Args:
        signature: Solana transaction signature
        
    Returns:
        Explorer URL for the transaction on mainnet
    """
    return f"https://explorer.solana.com/tx/{signature}?cluster=mainnet-beta"


if __name__ == "__main__":
    # Test proof hash utilities
    print("MEMBRA Proof Hash Utilities Test")
    print("=" * 50)
    
    # Test data
    test_proof = {
        "agent_id": "agent_123",
        "task_id": "task_456",
        "proof_type": "task_completion",
        "timestamp": "2024-01-01T00:00:00Z",
        "result": "success"
    }
    
    # Generate hash
    hash_value = proof_hash(test_proof)
    print(f"\nProof JSON: {test_proof}")
    print(f"Proof Hash: {hash_value}")
    
    # Generate memo payload
    entry_id = "proof_789"
    memo = memo_payload(entry_id, hash_value)
    print(f"\nMemo Payload: {memo}")
    
    # Generate explorer URL
    test_signature = "5K7dK5M5p5o5n5t5s5h5a5d5o5w5n5s5i5g5n5a5t5u5r5e5x5a5m5p5l5e"
    explorer = mainnet_explorer_url(test_signature)
    print(f"\nExplorer URL: {explorer}")
