from core.auth import build_context, has_permissions



def test_platform_admin_permissions():
    ctx = build_context(
        user_id="u1",
        tenant_id="t1",
        role="platform_admin",
    )

    assert has_permissions(ctx, ["assets.read"])
    assert has_permissions(ctx, ["proofbook.verify"])



def test_asset_owner_restrictions():
    ctx = build_context(
        user_id="u2",
        tenant_id="t1",
        role="asset_owner",
    )

    assert has_permissions(ctx, ["assets.write"])
    assert not has_permissions(ctx, ["billing.reconcile"])
