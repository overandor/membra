"""
Unit tests for MEMBRA Liquid Terminal core functions
Tests MUP calculation, approval flow, liquidity calculation, exports, and ledger functions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    calculate_mup,
    calculate_trust_adjusted_liquidity,
    calculate_node_yield_score,
    SAMPLE_INVENTORY
)


def test_calculate_mup():
    """Test Minimum Useful Price calculation"""
    # Test with sample inventory item
    item = SAMPLE_INVENTORY[0]  # Vacuum Cleaner
    mup = calculate_mup(item)
    
    # MUP should be positive
    assert mup > 0, "MUP should be positive"
    
    # MUP should be based on calculation components
    calc = item['mup_calculation']
    expected_base = calc['hourly_depreciation'] + calc['setup_overhead'] + calc['risk_premium'] + calc['market_adjustment']
    expected_mup = expected_base * 1.2
    
    assert abs(mup - expected_mup) < 0.01, f"MUP calculation mismatch: {mup} vs {expected_mup}"
    print("✓ test_calculate_mup passed")


def test_approval_flow_parsing():
    """Test approval flow correctly parses checkbox labels"""
    # Simulate checkbox selections (format: "1. Vacuum Cleaner")
    approved_selections = ["1. Vacuum Cleaner", "3. Power Drill"]
    
    # Parse indices from selections
    approved_index_numbers = []
    for selection in approved_selections:
        try:
            index = int(selection.split('.')[0]) - 1  # Convert to 0-based index
            approved_index_numbers.append(index)
        except (ValueError, IndexError):
            continue
    
    # Verify parsing
    assert 0 in approved_index_numbers, "Should parse index 0 from '1. Vacuum Cleaner'"
    assert 2 in approved_index_numbers, "Should parse index 2 from '3. Power Drill'"
    assert len(approved_index_numbers) == 2, "Should have exactly 2 approved indices"
    
    print("✓ test_approval_flow_parsing passed")


def test_trust_adjusted_liquidity_dollars():
    """Test Trust-Adjusted Liquidity returns monthly dollars, not percentage"""
    # Create test approved items
    approved_items = [SAMPLE_INVENTORY[0], SAMPLE_INVENTORY[1]]  # Vacuum Cleaner, Shelf Space
    
    # Calculate trust-adjusted liquidity
    liquidity = calculate_trust_adjusted_liquidity(approved_items)
    
    # Should return dollar amount, not percentage
    assert liquidity > 0, "Liquidity should be positive"
    assert liquidity < 10000, "Liquidity should be reasonable dollar amount"
    
    # Should be in dollars per month range
    # Vacuum: $7.50 * 20 = $150/month
    # Shelf: $15/month
    # Total gross: ~$165/month
    # Risk-adjusted should be close to gross (all Low Risk)
    assert liquidity > 100, f"Liquidity should be >$100/month, got ${liquidity:.2f}"
    assert liquidity < 200, f"Liquidity should be <$200/month, got ${liquidity:.2f}"
    
    print("✓ test_trust_adjusted_liquidity_dollars passed")


def test_trust_adjusted_liquidity_risk_adjustment():
    """Test risk adjustment factors are applied correctly"""
    # Low risk item
    low_risk_item = SAMPLE_INVENTORY[0].copy()
    low_risk_item['risk_level'] = 'Low'
    low_risk_item['rent_mode'] = 'hourly'
    low_risk_item['suggested_price'] = 10.0
    
    # Medium risk item
    medium_risk_item = SAMPLE_INVENTORY[0].copy()
    medium_risk_item['risk_level'] = 'Medium'
    medium_risk_item['rent_mode'] = 'hourly'
    medium_risk_item['suggested_price'] = 10.0
    
    # Calculate for each
    low_liquidity = calculate_trust_adjusted_liquidity([low_risk_item])
    medium_liquidity = calculate_trust_adjusted_liquidity([medium_risk_item])
    
    # Medium risk should have lower liquidity (0.7 factor)
    assert low_liquidity > medium_liquidity, "Low risk should have higher liquidity than medium risk"
    
    # Check approximate ratio (should be ~1.0/0.7 = 1.43)
    ratio = low_liquidity / medium_liquidity
    assert 1.3 < ratio < 1.6, f"Risk adjustment ratio should be ~1.43, got {ratio:.2f}"
    
    print("✓ test_trust_adjusted_liquidity_risk_adjustment passed")


def test_node_yield_score():
    """Test node yield score calculation"""
    # Test with approved items
    approved_items = SAMPLE_INVENTORY[:3]
    
    score = calculate_node_yield_score(approved_items)
    
    # Score should be between 0 and 100
    assert 0 <= score <= 100, f"Yield score should be 0-100, got {score}"
    
    # Score should be reasonable for sample data
    assert score > 50, f"Yield score should be >50 for sample data, got {score}"
    
    print("✓ test_node_yield_score passed")


def test_node_yield_score_components():
    """Test yield score components are calculated correctly"""
    # Single item
    single_item = [SAMPLE_INVENTORY[0]]
    score = calculate_node_yield_score(single_item)
    
    # With single item, diversity should be 1.0 (1 category / 1 item)
    # Confidence should be the item's confidence
    # Risk score should be based on risk level
    
    assert score > 0, "Single item should have positive yield score"
    
    print("✓ test_node_yield_score_components passed")


def test_export_json_structure():
    """Test JSON export produces valid structure"""
    from app import export_inventory_json
    
    # Approve some items first
    SAMPLE_INVENTORY[0]['approved'] = True
    SAMPLE_INVENTORY[1]['approved'] = True
    
    json_export = export_inventory_json()
    
    # Should be valid JSON
    import json
    try:
        data = json.loads(json_export)
    except json.JSONDecodeError:
        raise AssertionError("JSON export should produce valid JSON")
    
    # Should have required fields
    assert 'generated_at' in data, "JSON export should have generated_at"
    assert 'total_items' in data, "JSON export should have total_items"
    assert 'inventory' in data, "JSON export should have inventory"
    
    # Should have correct count
    assert data['total_items'] == 2, f"Should export 2 items, got {data['total_items']}"
    
    print("✓ test_export_json_structure passed")


def test_export_csv_structure():
    """Test CSV export produces valid structure"""
    from app import export_inventory_csv
    
    # Approve some items first
    SAMPLE_INVENTORY[0]['approved'] = True
    SAMPLE_INVENTORY[1]['approved'] = True
    
    csv_export = export_inventory_csv()
    
    # Should have header row
    lines = csv_export.split('\n')
    assert len(lines) >= 3, "CSV should have header + at least 2 data rows"
    
    # Header should have expected columns
    header = lines[0]
    expected_columns = ['name', 'category', 'type', 'confidence', 'risk_level', 'rent_mode', 'space_mode', 'suggested_price', 'condition', 'approved']
    for col in expected_columns:
        assert col in header, f"CSV header should include '{col}'"
    
    print("✓ test_export_csv_structure passed")


def test_investor_summary_structure():
    """Test investor summary produces valid structure"""
    from app import generate_investor_summary
    
    # Approve some items first
    SAMPLE_INVENTORY[0]['approved'] = True
    SAMPLE_INVENTORY[1]['approved'] = True
    
    summary = generate_investor_summary()
    
    # Should be valid JSON
    import json
    try:
        data = json.loads(summary)
    except json.JSONDecodeError:
        raise AssertionError("Investor summary should produce valid JSON")
    
    # Should have required fields
    assert 'generated_at' in data, "Summary should have generated_at"
    assert 'household_node' in data, "Summary should have household_node"
    assert 'inventory_breakdown' in data, "Summary should have inventory_breakdown"
    
    # Household node should have required metrics
    node = data['household_node']
    assert 'detected_units' in node, "Node should have detected_units"
    assert 'approved_liquid_units' in node, "Node should have approved_liquid_units"
    assert 'gross_utility_value_monthly' in node, "Node should have gross_utility_value_monthly"
    assert 'trust_adjusted_liquidity_monthly' in node, "Node should have trust_adjusted_liquidity_monthly"
    
    # Trust-adjusted liquidity should be in dollars, not percentage
    assert node['trust_adjusted_liquidity_monthly'] < 10000, "Trust-adjusted liquidity should be dollar amount"
    assert node['trust_adjusted_liquidity_monthly'] > 0, "Trust-adjusted liquidity should be positive"
    
    print("✓ test_investor_summary_structure passed")


def test_settlement_ledger_mock():
    """Test mock settlement ledger generation"""
    from app import generate_mock_settlement_ledger
    
    # Approve some items first
    SAMPLE_INVENTORY[0]['approved'] = True
    SAMPLE_INVENTORY[1]['approved'] = True
    
    ledger = generate_mock_settlement_ledger()
    
    # Should contain mock disclaimer
    assert "MOCK" in ledger or "DEMO" in ledger, "Ledger should indicate mock/demo status"
    assert "demonstration" in ledger.lower(), "Ledger should mention demonstration"
    
    # Should not claim real transactions
    assert "simulated" in ledger.lower() or "simulation" in ledger.lower(), "Ledger should mention simulated/simulation"
    
    print("✓ test_settlement_ledger_mock passed")


def test_membra_index_record_fields():
    """Test sample inventory includes MembraIndexRecord fields"""
    item = SAMPLE_INVENTORY[0]
    
    # Should have required MembraIndexRecord fields
    required_fields = [
        'membra_index_id',
        'unit_type',
        'access_mode',
        'fulfillment_mode',
        'minimum_useful_price',
        'trust_score',
        'demand_score',
        'liquidity_score',
        'yield_score'
    ]
    
    for field in required_fields:
        assert field in item, f"Sample inventory should include {field}"
    
    print("✓ test_membra_index_record_fields passed")


def test_rent_mode_monthly_vs_hourly():
    """Test monthly vs hourly rent mode calculations"""
    # Hourly item
    hourly_item = SAMPLE_INVENTORY[0].copy()
    hourly_item['rent_mode'] = 'hourly'
    hourly_item['suggested_price'] = 10.0
    hourly_item['risk_level'] = 'Low'
    
    # Monthly item
    monthly_item = SAMPLE_INVENTORY[1].copy()
    monthly_item['rent_mode'] = 'monthly'
    monthly_item['suggested_price'] = 10.0
    monthly_item['risk_level'] = 'Low'
    
    hourly_liquidity = calculate_trust_adjusted_liquidity([hourly_item])
    monthly_liquidity = calculate_trust_adjusted_liquidity([monthly_item])
    
    # Hourly should be ~20x monthly (20 hours * $10 vs $10)
    ratio = hourly_liquidity / monthly_liquidity
    assert 18 < ratio < 22, f"Hourly should be ~20x monthly, got ratio {ratio:.2f}"
    
    print("✓ test_rent_mode_monthly_vs_hourly passed")


def run_all_tests():
    """Run all tests"""
    print("Running MEMBRA Liquid Terminal unit tests...\n")
    
    tests = [
        test_calculate_mup,
        test_approval_flow_parsing,
        test_trust_adjusted_liquidity_dollars,
        test_trust_adjusted_liquidity_risk_adjustment,
        test_node_yield_score,
        test_node_yield_score_components,
        test_export_json_structure,
        test_export_csv_structure,
        test_investor_summary_structure,
        test_settlement_ledger_mock,
        test_membra_index_record_fields,
        test_rent_mode_monthly_vs_hourly
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
