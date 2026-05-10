"""
MEMBRA Liquid Terminal
The liquidity layer for real-world household utility
"""

import gradio as gr
import json
from datetime import datetime

# Sample inventory data for simulation
SAMPLE_INVENTORY = [
    {
        "name": "Vacuum Cleaner",
        "category": "Appliance",
        "type": "Cleaning",
        "confidence": 0.92,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 7.50,
        "condition": "Good",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.14,
            "setup_overhead": 4.00,
            "risk_premium": 0.08,
            "market_adjustment": 1.50,
            "platform_margin": 1.78
        }
    },
    {
        "name": "Shelf Space (3ft)",
        "category": "Storage",
        "type": "Shelf",
        "confidence": 0.88,
        "risk_level": "Low",
        "rent_mode": "monthly",
        "space_mode": "onsite",
        "suggested_price": 15.00,
        "condition": "Excellent",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.00,
            "setup_overhead": 2.50,
            "risk_premium": 0.00,
            "market_adjustment": 0.50,
            "platform_margin": 3.00
        }
    },
    {
        "name": "Power Drill",
        "category": "Tool",
        "type": "Power Tool",
        "confidence": 0.85,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 8.00,
        "condition": "Good",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.15,
            "setup_overhead": 5.00,
            "risk_premium": 0.09,
            "market_adjustment": 2.00,
            "platform_margin": 0.76
        }
    },
    {
        "name": "Folding Chair",
        "category": "Furniture",
        "type": "Chair",
        "confidence": 0.95,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 3.00,
        "condition": "Excellent",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.03,
            "setup_overhead": 2.00,
            "risk_premium": 0.00,
            "market_adjustment": 0.50,
            "platform_margin": 0.47
        }
    },
    {
        "name": "Ring Light",
        "category": "Appliance",
        "type": "Lighting",
        "confidence": 0.90,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 5.00,
        "condition": "Good",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.08,
            "setup_overhead": 3.00,
            "risk_premium": 0.05,
            "market_adjustment": 1.00,
            "platform_margin": 0.87
        }
    },
    {
        "name": "Closet Space (5ft)",
        "category": "Storage",
        "type": "Closet",
        "confidence": 0.87,
        "risk_level": "Low",
        "rent_mode": "monthly",
        "space_mode": "onsite",
        "suggested_price": 25.00,
        "condition": "Excellent",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.00,
            "setup_overhead": 3.00,
            "risk_premium": 0.00,
            "market_adjustment": 1.00,
            "platform_margin": 5.00
        }
    },
    {
        "name": "Extension Cord (25ft)",
        "category": "Tool",
        "type": "Accessory",
        "confidence": 0.93,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 2.00,
        "condition": "Excellent",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.01,
            "setup_overhead": 1.50,
            "risk_premium": 0.00,
            "market_adjustment": 0.25,
            "platform_margin": 0.24
        }
    },
    {
        "name": "Phone Charger",
        "category": "Appliance",
        "type": "Charger",
        "confidence": 0.91,
        "risk_level": "Low",
        "rent_mode": "hourly",
        "space_mode": "pickup",
        "suggested_price": 1.50,
        "condition": "Good",
        "approved": False,
        "mup_calculation": {
            "hourly_depreciation": 0.01,
            "setup_overhead": 1.00,
            "risk_premium": 0.00,
            "market_adjustment": 0.25,
            "platform_margin": 0.24
        }
    }
]

def simulate_detection(image):
    """Simulate AI detection from uploaded image"""
    if image is None:
        return "Please upload a room image to begin."
    
    return f"Detected {len(SAMPLE_INVENTORY)} utility units in your space. Review and approve to generate household balance sheet."

def calculate_mup(item):
    """Calculate Minimum Useful Price for an item"""
    calc = item.get('mup_calculation', {})
    base = calc.get('hourly_depreciation', 0) + calc.get('setup_overhead', 0) + calc.get('risk_premium', 0) + calc.get('market_adjustment', 0)
    mup = base * 1.2  # Platform margin
    return mup

def calculate_trust_adjusted_liquidity(approved_items):
    """Calculate trust-adjusted liquidity score"""
    if not approved_items:
        return 0.0
    
    gross_value = 0
    risk_adjusted = 0
    
    for item in approved_items:
        monthly_value = item['suggested_price'] * 20 if item['rent_mode'] == 'hourly' else item['suggested_price']
        gross_value += monthly_value
        
        # Risk adjustment factor
        risk_factor = 1.0 if item['risk_level'] == 'Low' else 0.7 if item['risk_level'] == 'Medium' else 0.4
        risk_adjusted += monthly_value * risk_factor
    
    return risk_adjusted if gross_value == 0 else (risk_adjusted / gross_value) * 100

def calculate_node_yield_score(approved_items):
    """Calculate node yield score"""
    if not approved_items:
        return 0.0
    
    # Factors: inventory diversity, confidence avg, risk profile, pricing quality
    diversity = len(set(item['category'] for item in approved_items)) / len(approved_items)
    avg_confidence = sum(item['confidence'] for item in approved_items) / len(approved_items)
    risk_score = sum(1 if item['risk_level'] == 'Low' else 0.5 for item in approved_items) / len(approved_items)
    
    score = (diversity * 30) + (avg_confidence * 40) + (risk_score * 30)
    return score

def generate_liquid_cards():
    """Generate liquid asset cards from detected inventory"""
    cards = []
    for item in SAMPLE_INVENTORY:
        mup = calculate_mup(item)
        card = f"""
**{item['name']}**
- Category: {item['category']}
- Type: {item['type']}
- Detection Confidence: {item['confidence']:.0%}
- Risk Level: {item['risk_level']}
- Access Mode: {item['space_mode']}
- MUP: ${mup:.2f}/{item['rent_mode']}
- Suggested Price: ${item['suggested_price']:.2f}/{item['rent_mode']}
- Condition: {item['condition']}
- Status: {'✓ Approved' if item['approved'] else '○ Pending'}
"""
        cards.append(card)
    return "\n\n---\n\n".join(cards)

def update_inventory_status(approved_indices):
    """Update approval status for selected items"""
    for i, item in enumerate(SAMPLE_INVENTORY):
        SAMPLE_INVENTORY[i]['approved'] = i in approved_indices
    return generate_liquid_cards()

def generate_household_balance_sheet():
    """Generate household balance sheet from approved inventory"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to generate balance sheet."
    
    gross_value = 0
    for item in approved_items:
        monthly_value = item['suggested_price'] * 20 if item['rent_mode'] == 'hourly' else item['suggested_price']
        gross_value += monthly_value
    
    trust_adjusted = calculate_trust_adjusted_liquidity(approved_items)
    node_yield = calculate_node_yield_score(approved_items)
    risk_grade = "Low" if all(item['risk_level'] == 'Low' for item in approved_items) else "Low-Medium"
    
    top_units = ", ".join([item['name'] for item in approved_items[:5]])
    
    return f"""**Household Node Balance Sheet**

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Node Metrics:**
- Detected Utility Units: {len(SAMPLE_INVENTORY)}
- Approved Liquid Units: {len(approved_items)}
- Gross Utility Value: ${gross_value:.2f}/month
- Trust-Adjusted Liquidity: ${trust_adjusted:.2f}/month
- Node Yield Score: {node_yield:.1f}
- Risk Grade: {risk_grade}

**Top Liquid Units:**
{top_units}

**Risk Ladder:**
{len([item for item in approved_items if item['risk_level'] == 'Low'])} Low Risk
{len([item for item in approved_items if item['risk_level'] == 'Medium'])} Medium Risk
{len([item for item in approved_items if item['risk_level'] == 'High'])} High Risk

*This is a simulation. Real deployment requires AI vision detection and live market data.*
"""

def generate_mock_settlement_ledger():
    """Generate mock settlement ledger (demo/dry-run only)"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to generate settlement ledger."
    
    ledger = "**MOCK SETTLEMENT LEDGER (DEMO/DRY-RUN ONLY)**\n\n"
    ledger += "This ledger is for demonstration purposes only. No actual transactions will occur.\n\n"
    
    # Generate mock transactions
    ledger += "**Recent Transactions (Simulated)**\n\n"
    
    for i, item in enumerate(approved_items[:3]):
        ledger += f"TX-{1000+i}: {item['name']}\n"
        ledger += f"- SKU ID: SKU-{i+1:04d}\n"
        ledger += f"- Price: ${item['suggested_price']:.2f}\n"
        ledger += "- Status: COMPLETED\n"
        ledger += "- Proof: PHOTO_VERIFIED\n"
        ledger += "- Settlement: PAYOUT_COMPLETE\n\n"
    
    ledger += "*All data shown is simulated. Real deployment requires live transaction processing.*"
    return ledger

def generate_investor_summary():
    """Generate exportable investor summary"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to generate investor summary."
    
    gross_value = sum(item['suggested_price'] * 20 if item['rent_mode'] == 'hourly' else item['suggested_price'] for item in approved_items)
    trust_adjusted = calculate_trust_adjusted_liquidity(approved_items)
    node_yield = calculate_node_yield_score(approved_items)
    
    summary = {
        "generated_at": datetime.now().isoformat(),
        "household_node": {
            "detected_units": len(SAMPLE_INVENTORY),
            "approved_liquid_units": len(approved_items),
            "gross_utility_value_monthly": gross_value,
            "trust_adjusted_liquidity_monthly": trust_adjusted,
            "node_yield_score": node_yield,
            "risk_grade": "Low" if all(item['risk_level'] == 'Low' for item in approved_items) else "Low-Medium"
        },
        "inventory_breakdown": [
            {
                "name": item['name'],
                "category": item['category'],
                "mup": calculate_mup(item),
                "suggested_price": item['suggested_price'],
                "rent_mode": item['rent_mode'],
                "risk_level": item['risk_level'],
                "confidence": item['confidence']
            }
            for item in approved_items
        ],
        "disclaimer": "This is a simulation. Real deployment requires AI vision detection and live market data."
    }
    
    return json.dumps(summary, indent=2)

def export_inventory_json():
    """Export inventory as JSON"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "total_items": len(approved_items),
        "inventory": approved_items
    }
    return json.dumps(export_data, indent=2)

def export_inventory_csv():
    """Export inventory as CSV"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to export."
    
    output = ["name,category,type,confidence,risk_level,rent_mode,space_mode,suggested_price,condition,approved"]
    for item in approved_items:
        output.append(f"{item['name']},{item['category']},{item['type']},{item['confidence']},{item['risk_level']},{item['rent_mode']},{item['space_mode']},{item['suggested_price']},{item['condition']},{item['approved']}")
    
    return "\n".join(output)

# Gradio Interface - MEMBRA Liquid Terminal
with gr.Blocks(title="MEMBRA Liquid Terminal", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # MEMBRA Liquid Terminal
    ### The liquidity layer for real-world household utility
    """)
    
    with gr.Tab("Scan & Detect"):
        gr.Markdown("### Step 1: Upload Room Image")
        image_input = gr.Image(label="Upload room photo", type="filepath")
        detect_btn = gr.Button("Detect Utility Units", variant="primary")
        detect_output = gr.Textbox(label="Detection Result")
        
        detect_btn.click(
            simulate_detection,
            inputs=[image_input],
            outputs=[detect_output]
        )
    
    with gr.Tab("Review & Approve"):
        gr.Markdown("### Step 2: Review Detected Utility Units")
        gr.Markdown("Select utility units to approve for liquidity:")
        
        liquid_cards = gr.Textbox(label="Detected Liquid Asset Cards", value=generate_liquid_cards(), lines=20)
        
        gr.Markdown("### Approve Utility Units")
        approve_checkboxes = gr.CheckboxGroup(
            choices=[f"{i+1}. {item['name']}" for i, item in enumerate(SAMPLE_INVENTORY)],
            label="Select utility units to approve",
            value=[]
        )
        
        approve_btn = gr.Button("Update Approval Status", variant="primary")
        
        approve_btn.click(
            update_inventory_status,
            inputs=[approve_checkboxes],
            outputs=[liquid_cards]
        )
    
    with gr.Tab("Household Balance Sheet"):
        gr.Markdown("### Step 3: Generate Household Balance Sheet")
        gr.Markdown("View your household as a liquidity node:")
        
        balance_btn = gr.Button("Generate Balance Sheet", variant="primary")
        balance_output = gr.Markdown(label="Household Node Balance Sheet")
        
        balance_btn.click(
            generate_household_balance_sheet,
            outputs=[balance_output]
        )
    
    with gr.Tab("Risk Ladder"):
        gr.Markdown("### Step 4: Risk Assessment")
        gr.Markdown("View risk ladder for approved utility units:")
        
        risk_btn = gr.Button("Generate Risk Assessment", variant="primary")
        risk_output = gr.Markdown(label="Risk Ladder Assessment")
        
        def generate_risk_assessment():
            approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
            if not approved_items:
                return "No approved items to assess."
            
            low_risk = [item for item in approved_items if item['risk_level'] == 'Low']
            medium_risk = [item for item in approved_items if item['risk_level'] == 'Medium']
            high_risk = [item for item in approved_items if item['risk_level'] == 'High']
            
            assessment = f"""**Risk Ladder Assessment**

**Low Risk Units ({len(low_risk)}):**
{', '.join([item['name'] for item in low_risk]) if low_risk else 'None'}

**Medium Risk Units ({len(medium_risk)}):**
{', '.join([item['name'] for item in medium_risk]) if medium_risk else 'None'}

**High Risk Units ({len(high_risk)}):**
{', '.join([item['name'] for item in high_risk]) if high_risk else 'None'}

**Overall Risk Grade:**
{'LOW' if len(high_risk) == 0 and len(medium_risk) == 0 else 'LOW-MEDIUM' if len(high_risk) == 0 else 'MEDIUM'}

*Risk assessment based on asset type, condition, and access mode.*
"""
            return assessment
        
        risk_btn.click(
            generate_risk_assessment,
            outputs=[risk_output]
        )
    
    with gr.Tab("Settlement Ledger"):
        gr.Markdown("### Step 5: Mock Settlement Ledger")
        gr.Markdown("*This is a demonstration. No actual transactions will occur.*")
        
        ledger_btn = gr.Button("Generate Mock Ledger", variant="primary")
        ledger_output = gr.Markdown(label="Mock Settlement Ledger")
        
        ledger_btn.click(
            generate_mock_settlement_ledger,
            outputs=[ledger_output]
        )
    
    with gr.Tab("Investor Summary"):
        gr.Markdown("### Step 6: Export Investor Summary")
        gr.Markdown("Generate finance-ready inventory summary for investors:")
        
        investor_btn = gr.Button("Generate Investor Summary", variant="primary")
        investor_output = gr.Textbox(label="Investor Summary (JSON)")
        
        investor_btn.click(
            generate_investor_summary,
            outputs=[investor_output]
        )
    
    with gr.Tab("Export"):
        gr.Markdown("### Step 7: Export Data")
        
        with gr.Row():
            json_btn = gr.Button("Export JSON", variant="secondary")
            csv_btn = gr.Button("Export CSV", variant="secondary")
        
        with gr.Row():
            json_output = gr.Textbox(label="JSON Export")
            csv_output = gr.Textbox(label="CSV Export")
        
        json_btn.click(
            export_inventory_json,
            outputs=[json_output]
        )
        
        csv_btn.click(
            export_inventory_csv,
            outputs=[csv_output]
        )
    
    gr.Markdown("""
    ---
    **MEMBRA Liquid** converts idle household utility into verified, fractional, finance-ready local liquidity.
    
    *This is a simulator. Real deployment requires AI vision detection and live market data.*
    
    **Pre-user. Post-thesis. Artifact-complete.**
    """)

if __name__ == "__main__":
    demo.launch()
