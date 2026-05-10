"""
MEMBRA Devnet Guardrails
Enforces the MEMBRA Devnet Doctrine across all applications.
"""

import os


def assert_devnet_only() -> None:
    """Ensure the application is running on Solana Devnet only."""
    allow_mainnet = os.getenv("ALLOW_MAINNET", "false").lower() == "true"
    rpc_url = os.getenv("SOLANA_RPC_URL", "")
    cluster = os.getenv("SOLANA_CLUSTER", "devnet").lower()
    
    if not allow_mainnet:
        if "mainnet" in rpc_url.lower() or cluster == "mainnet":
            raise RuntimeError(
                "Mainnet disabled. MEMBRA default mode requires Solana Devnet."
            )


def assert_no_real_funds() -> None:
    """Ensure real funds are not being used by default."""
    allow_real_funds = os.getenv("ALLOW_REAL_FUNDS", "false").lower() == "true"
    
    if allow_real_funds:
        raise RuntimeError(
            "Real funds are disabled by default. Use LaunchPad promotion with human approval."
        )


def assert_no_live_trading() -> None:
    """Ensure live trading is disabled by default."""
    allow_live_trading = os.getenv("ALLOW_LIVE_TRADING", "false").lower() == "true"
    
    if allow_live_trading:
        raise RuntimeError(
            "Live trading is disabled by default. Use Devnet, dry-run, backtest, or paper mode."
        )


def enforce_membra_devnet_doctrine() -> None:
    """
    Enforce all MEMBRA Devnet Doctrine guardrails.
    This should be called at application startup in every app.py.
    """
    assert_devnet_only()
    assert_no_real_funds()
    assert_no_live_trading()


def is_devnet_mode() -> bool:
    """Check if the system is in Devnet mode."""
    return os.getenv("MEMBRA_ENV", "devnet").lower() == "devnet"


def is_dry_run() -> bool:
    """Check if the system is in dry-run mode."""
    return os.getenv("DRY_RUN", "true").lower() == "true"


def is_platform_fee_payer() -> bool:
    """Check if platform is sponsoring Devnet transaction fees."""
    return os.getenv("AGENT_FEE_PAYER_MODE", "platform").lower() == "platform"


def get_solana_cluster() -> str:
    """Get the configured Solana cluster."""
    return os.getenv("SOLANA_CLUSTER", "devnet")


def get_solana_rpc_url() -> str:
    """Get the configured Solana RPC URL."""
    return os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
