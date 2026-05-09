"""
MEMBRA Smart Actions API
Real smart actions for inventory management
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import uuid4
import sqlite3
import os

router = APIRouter(tags=["Smart Actions"])

# Database connection
DB_PATH = os.getenv("DATABASE_PATH", "membra.db")

class SmartActionRequest(BaseModel):
    inventory_item_id: str
    action_type: str  # rent, split, deliver, meet_halfway, store
    action_config: Optional[dict] = None

class SmartActionResponse(BaseModel):
    action_id: str
    inventory_item_id: str
    action_type: str
    action_config: dict
    is_active: bool
    created_at: datetime

@router.post("/smart-actions/create")
async def create_smart_action(request: SmartActionRequest):
    """Create a smart action for an inventory item"""
    try:
        # Validate action type
        valid_actions = ["rent", "split", "deliver", "meet_halfway", "store"]
        if request.action_type not in valid_actions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid action type. Must be one of: {valid_actions}"
            )
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if database tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='smart_actions'
        """)
        
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=501,
                detail="Database tables not initialized. Run schema.sql first."
            )
        
        # Create smart action
        action_id = str(uuid4())
        cursor.execute("""
            INSERT INTO smart_actions (id, inventory_item_id, action_type, action_config, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (action_id, request.inventory_item_id, request.action_type,
              request.action_config or {}, True, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
        
        return SmartActionResponse(
            action_id=action_id,
            inventory_item_id=request.inventory_item_id,
            action_type=request.action_type,
            action_config=request.action_config or {},
            is_active=True,
            created_at=datetime.now()
        )
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Smart action creation failed: {str(e)}")

@router.get("/smart-actions/{inventory_item_id}")
async def get_smart_actions(inventory_item_id: str):
    """Get all smart actions for an inventory item"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, action_type, action_config, is_active, created_at
            FROM smart_actions
            WHERE inventory_item_id = ?
            ORDER BY created_at DESC
        """, (inventory_item_id,))
        
        actions = []
        for row in cursor.fetchall():
            actions.append({
                "action_id": row[0],
                "action_type": row[1],
                "action_config": row[2],
                "is_active": row[3],
                "created_at": row[4]
            })
        
        conn.close()
        
        return {
            "inventory_item_id": inventory_item_id,
            "actions": actions,
            "total_actions": len(actions)
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get smart actions: {str(e)}")

@router.put("/smart-actions/{action_id}/toggle")
async def toggle_smart_action(action_id: str):
    """Toggle smart action active status"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE smart_actions
            SET is_active = NOT is_active, updated_at = ?
            WHERE id = ?
        """, (datetime.now(), action_id))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Smart action not found")
        
        conn.commit()
        conn.close()
        
        return {
            "action_id": action_id,
            "status": "toggled",
            "updated_at": datetime.now()
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle smart action: {str(e)}")
