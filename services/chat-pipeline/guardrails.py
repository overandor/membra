"""
MEMBRA Guardrails

Enforces the MEMBRA operating rules:
- Real SOL by default
- Real transactions by default
- Real profit by default
- All agent prompts, tests, tasks, proof logs, skill tests, and transactions run on Solana mainnet
- Database preserves canonical state
- Blockchain provides cryptographic proof
"""

import os


def assert_mainnet_ready():
    """
    Ensure the system is configured for mainnet operation.
    
    Raises:
        RuntimeError: If mainnet is not enabled when required.
    """
    if os.getenv("ALLOW_MAINNET", "true").lower() != "true":
        raise RuntimeError("Mainnet must be enabled for real funds operation.")


def assert_real_funds_enabled():
    """
    Ensure real funds are enabled.
    
    Returns:
        True if real funds are enabled.
    
    Raises:
        RuntimeError: If real funds are disabled.
    """
    if os.getenv("ALLOW_REAL_FUNDS", "true").lower() != "true":
        raise RuntimeError("Real funds must be enabled for mainnet operation.")
    return True


def enforce_membra_doctrine():
    """
    Enforce MEMBRA doctrine for mainnet operation.
    
    This function should be called at the start of any app.py or critical execution path
    to ensure the system is configured for mainnet with real funds.
    
    Raises:
        RuntimeError: If any guardrail check fails.
    """
    assert_mainnet_ready()
    assert_real_funds_enabled()


if __name__ == "__main__":
    # Test guardrails when run directly
    print("MEMBRA Guardrails")
    print("=" * 50)
    
    # Try to enforce doctrine
    print("\nEnforcing MEMBRA Doctrine...")
    try:
        enforce_membra_doctrine()
        print("✓ All guardrails passed. System is configured for mainnet operation with real funds.")
    except RuntimeError as e:
        print(f"✗ Guardrail violation: {e}")
