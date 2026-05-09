"""
MEMBRA SKU Approval API
Real SKU approval workflow
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
import sqlite3
import os

router = APIRouter(tags=["SKU Approval"])

# Database connection
DB_PATH = os.getenv("DATABASE_PATH", "membra.db")

class SKUApprovalRequest(BaseModel):
    user_id: str
    detected_object_id: str
    is_approved: bool
    notes: Optional[str] = None

class SKUApprovalResponse(BaseModel):
    approval_id: str
    detected_object_id: str
    user_id: str
    is_approved: bool
    approved_at: datetime
    notes: Optional[str]

class SKUApprovalBatchRequest(BaseModel):
    user_id: str
    approvals: List[dict]

@router.post("/sku-approval/approve")
async def approve_sku(request: SKUApprovalRequest):
    """Approve or reject a SKU match"""
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if database tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='sku_matches'
        """)
        
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=501,
                detail="Database tables not initialized. Run schema.sql first."
            )
        
        # Create approval record
        approval_id = str(uuid4())
        cursor.execute("""
            INSERT INTO approvals (id, inventory_item_id, user_id, approval_type, status, notes, approved_at)
            VALUES (?, ?, ?, 'sku_approval', ?, ?, ?)
        """, (approval_id, request.detected_object_id, request.user_id, 
              'approved' if request.is_approved else 'rejected', 
              request.notes, datetime.now()))
        
        # Update SKU match approval status
        cursor.execute("""
            UPDATE sku_matches 
            SET is_approved = ?, approved_by = ?, approved_at = ?
            WHERE id = ?
        """, (request.is_approved, request.user_id, datetime.now(), request.detected_object_id))
        
        conn.commit()
        conn.close()
        
        return SKUApprovalResponse(
            approval_id=approval_id,
            detected_object_id=request.detected_object_id,
            user_id=request.user_id,
            is_approved=request.is_approved,
            approved_at=datetime.now(),
            notes=request.notes
        )
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SKU approval failed: {str(e)}")

@router.post("/sku-approval/batch")
async def batch_approve_skus(request: SKUApprovalBatchRequest):
    """Batch approve multiple SKUs"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        approved_count = 0
        rejected_count = 0
        
        for approval in request.approvals:
            approval_id = str(uuid4())
            is_approved = approval.get('is_approved', False)
            detected_object_id = approval.get('detected_object_id')
            
            cursor.execute("""
                INSERT INTO approvals (id, inventory_item_id, user_id, approval_type, status, notes, approved_at)
                VALUES (?, ?, ?, 'sku_approval', ?, ?, ?)
            """, (approval_id, detected_object_id, request.user_id,
                  'approved' if is_approved else 'rejected',
                  approval.get('notes'), datetime.now()))
            
            cursor.execute("""
                UPDATE sku_matches 
                SET is_approved = ?, approved_by = ?, approved_at = ?
                WHERE id = ?
            """, (is_approved, request.user_id, datetime.now(), detected_object_id))
            
            if is_approved:
                approved_count += 1
            else:
                rejected_count += 1
        
        conn.commit()
        conn.close()
        
        return {
            "total_processed": len(request.approvals),
            "approved_count": approved_count,
            "rejected_count": rejected_count
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch approval failed: {str(e)}")

@router.get("/sku-approval/pending/{user_id}")
async def get_pending_approvals(user_id: str):
    """Get pending SKU approvals for a user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sm.id, sm.object_id, sm.match_score, sm.suggested_rent_price,
                   sm.suggested_sale_price, sm.rent_mode, sm.space_mode,
                   do.object_name, do.category, do.confidence
            FROM sku_matches sm
            JOIN detected_objects do ON sm.object_id = do.id
            JOIN uploaded_images ui ON do.image_id = ui.id
            WHERE sm.is_approved = FALSE
            AND ui.user_id = ?
            ORDER BY sm.match_score DESC
        """, (user_id,))
        
        pending_approvals = []
        for row in cursor.fetchall():
            pending_approvals.append({
                "sku_match_id": row[0],
                "object_id": row[1],
                "match_score": row[2],
                "suggested_rent_price": row[3],
                "suggested_sale_price": row[4],
                "rent_mode": row[5],
                "space_mode": row[6],
                "object_name": row[7],
                "category": row[8],
                "confidence": row[9]
            })
        
        conn.close()
        
        return {
            "user_id": user_id,
            "pending_count": len(pending_approvals),
            "pending_approvals": pending_approvals
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get pending approvals: {str(e)}")
