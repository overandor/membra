"""
MEMBRA Inventory Node Simulator
AI-powered household inventory commerce OS
"""

import gradio as gr
import json
from datetime import datetime
import random

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
        "approved": False
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
        "approved": False
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
        "approved": False
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
        "approved": False
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
        "approved": False
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
        "approved": False
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
        "approved": False
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
        "approved": False
    }
]

def simulate_detection(image):
    """Simulate AI detection from uploaded image"""
    if image is None:
        return "Please upload a room image to begin."
    
    # In a real implementation, this would use computer vision
    # For now, we return sample inventory
    return f"Detected {len(SAMPLE_INVENTORY)} items in your space. Review and approve below."

def generate_sku_cards():
    """Generate SKU cards from detected inventory"""
    cards = []
    for item in SAMPLE_INVENTORY:
        card = f"""
**{item['name']}**
- Category: {item['category']}
- Type: {item['type']}
- Detection Confidence: {item['confidence']:.0%}
- Risk Level: {item['risk_level']}
- Rent Mode: {item['rent_mode']}
- Space Mode: {item['space_mode']}
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
    return generate_sku_cards()

def calculate_earnings():
    """Calculate estimated monthly earnings"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    monthly_earnings = 0
    breakdown = []
    
    for item in approved_items:
        if item['rent_mode'] == 'monthly':
            monthly_earnings += item['suggested_price']
            breakdown.append(f"{item['name']}: ${item['suggested_price']:.2f}/month")
        else:  # hourly
            # Assume 20 hours/month usage
            monthly_earnings += item['suggested_price'] * 20
            breakdown.append(f"{item['name']}: ${item['suggested_price']:.2f}/hr × 20hr = ${item['suggested_price'] * 20:.2f}/month")
    
    if not breakdown:
        return "No approved items. Approve items to see earnings estimate."
    
    breakdown_text = "\n".join(breakdown)
    return f"""**Estimated Monthly Earnings: ${monthly_earnings:.2f}**

Breakdown:
{breakdown_text}

*Estimates based on 20 hours/month usage for hourly items. Actual earnings may vary.*
"""

def generate_public_listing():
    """Generate public inventory listing"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to list."
    
    listing = f"# Public Inventory Listing\n"
    listing += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    listing += f"Total Items: {len(approved_items)}\n\n"
    
    for item in approved_items:
        listing += f"## {item['name']}\n"
        listing += f"- **Category**: {item['category']}\n"
        listing += f"- **Type**: {item['type']}\n"
        listing += f"- **Price**: ${item['suggested_price']:.2f}/{item['rent_mode']}\n"
        listing += f"- **Access**: {item['space_mode']}\n"
        listing += f"- **Condition**: {item['condition']}\n"
        listing += f"- **Risk Level**: {item['risk_level']}\n\n"
    
    return listing

def simulate_matching():
    """Simulate requester matching (dry-run only)"""
    approved_items = [item for item in SAMPLE_INVENTORY if item['approved']]
    
    if not approved_items:
        return "No approved items to match."
    
    # Simulate potential requests
    requests = [
        "Need a vacuum near me for 20 minutes",
        "Looking for shelf space for boxes",
        "Need a drill for home project",
        "Need folding chairs for event",
        "Need ring light for video shoot"
    ]
    
    matches = []
    for request in requests:
        matched_item = random.choice(approved_items)
        matches.append(f"Request: '{request}'\nMatched: {matched_item['name']} (${matched_item['suggested_price']:.2f}/{matched_item['rent_mode']})")
    
    return "**Requester Matching Simulation (Dry-Run)**\n\n" + "\n\n".join(matches)

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

# Gradio Interface
with gr.Blocks(title="MEMBRA Inventory Node Simulator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # MEMBRA Inventory Node Simulator
    ### AI-powered household inventory commerce OS
    """)
    
    with gr.Tab("Scan & Detect"):
        gr.Markdown("### Step 1: Upload Room Image")
        image_input = gr.Image(label="Upload room photo", type="filepath")
        detect_btn = gr.Button("Detect Inventory", variant="primary")
        detect_output = gr.Textbox(label="Detection Result")
        
        detect_btn.click(
            simulate_detection,
            inputs=[image_input],
            outputs=[detect_output]
        )
    
    with gr.Tab("Review & Approve"):
        gr.Markdown("### Step 2: Review Detected Items")
        gr.Markdown("Select items to approve for listing:")
        
        sku_cards = gr.Textbox(label="Detected SKU Cards", value=generate_sku_cards(), lines=20)
        
        gr.Markdown("### Approve Items")
        approve_checkboxes = gr.CheckboxGroup(
            choices=[f"{i+1}. {item['name']}" for i, item in enumerate(SAMPLE_INVENTORY)],
            label="Select items to approve",
            value=[]
        )
        
        approve_btn = gr.Button("Update Approval Status", variant="primary")
        
        approve_btn.click(
            update_inventory_status,
            inputs=[approve_checkboxes],
            outputs=[sku_cards]
        )
    
    with gr.Tab("Earnings Estimate"):
        gr.Markdown("### Step 3: View Earnings Estimate")
        earnings_btn = gr.Button("Calculate Earnings", variant="primary")
        earnings_output = gr.Markdown(label="Monthly Earnings Estimate")
        
        earnings_btn.click(
            calculate_earnings,
            outputs=[earnings_output]
        )
    
    with gr.Tab("Public Listing"):
        gr.Markdown("### Step 4: Generate Public Listing")
        listing_btn = gr.Button("Generate Listing", variant="primary")
        listing_output = gr.Markdown(label="Public Inventory Listing")
        
        listing_btn.click(
            generate_public_listing,
            outputs=[listing_output]
        )
    
    with gr.Tab("Matching Simulation"):
        gr.Markdown("### Step 5: Requester Matching (Dry-Run)")
        gr.Markdown("*This is a simulation only. No actual requests will be sent.*")
        match_btn = gr.Button("Simulate Matching", variant="primary")
        match_output = gr.Markdown(label="Matching Results")
        
        match_btn.click(
            simulate_matching,
            outputs=[match_output]
        )
    
    with gr.Tab("Export"):
        gr.Markdown("### Step 6: Export Inventory")
        
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
    **MEMBRA** turns private household utility into verified, fractional, permissioned local commerce.
    
    *This is a simulator. Real AI detection and matching would use computer vision and LLM intent matching.*
    """)

if __name__ == "__main__":
    demo.launch()
