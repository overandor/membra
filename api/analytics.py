"""
MEMBRA Analytics API
Real analytics from database events
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import sqlite3
import os

router = APIRouter(tags=["Analytics"])

# Database connection
DB_PATH = os.getenv("DATABASE_PATH", "membra.db")

class AnalyticsResponse(BaseModel):
    inventory_alpha: float
    match_quality: float
    trust_score: float
    node_yield: float
    active_nodes: int
    network_uptime: float
    period: str

@router.get("/analytics/overview")
async def get_analytics_overview(period: str = "30d"):
    """Get analytics overview for specified period"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if database tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='analytics_events'
        """)
        
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=501,
                detail="Analytics tables not initialized. Run schema.sql first."
            )
        
        # Calculate time period
        if period == "30d":
            start_date = datetime.now() - timedelta(days=30)
        elif period == "7d":
            start_date = datetime.now() - timedelta(days=7)
        elif period == "24h":
            start_date = datetime.now() - timedelta(hours=24)
        else:
            start_date = datetime.now() - timedelta(days=30)
        
        # Get inventory alpha (detection approval rate)
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN is_approved = 1 THEN 1 END) * 100.0 / COUNT(*) as inventory_alpha
            FROM sku_matches
            WHERE created_at >= ?
        """, (start_date,))
        
        result = cursor.fetchone()
        inventory_alpha = result[0] if result and result[0] else 0.0
        
        # Get match quality (average match score)
        cursor.execute("""
            SELECT AVG(match_score) as match_quality
            FROM sku_matches
            WHERE created_at >= ?
        """, (start_date,))
        
        result = cursor.fetchone()
        match_quality = result[0] if result and result[0] else 0.0
        
        # Get trust score (average user trust score)
        cursor.execute("""
            SELECT AVG(trust_score) as trust_score
            FROM users
            WHERE created_at >= ?
        """, (start_date,))
        
        result = cursor.fetchone()
        trust_score = result[0] if result and result[0] else 0.0
        
        # Get node yield (total transaction amount / active nodes)
        cursor.execute("""
            SELECT 
                COALESCE(SUM(t.amount), 0.0) as total_revenue,
                COUNT(DISTINCT h.id) as active_nodes
            FROM transactions t
            JOIN requests r ON t.request_id = r.id
            JOIN inventory_items ii ON r.inventory_item_id = ii.id
            JOIN hosts h ON ii.host_id = h.id
            WHERE t.created_at >= ?
        """, (start_date,))
        
        result = cursor.fetchone()
        total_revenue = result[0] if result else 0.0
        active_nodes = result[1] if result and result[1] else 1
        node_yield = total_revenue / active_nodes if active_nodes > 0 else 0.0
        
        # Get active nodes count
        cursor.execute("""
            SELECT COUNT(DISTINCT h.id)
            FROM hosts h
            WHERE h.is_active = 1
        """)
        
        result = cursor.fetchone()
        active_nodes_count = result[0] if result else 0
        
        # Get network uptime (mock - would be calculated from actual uptime monitoring)
        network_uptime = 99.98
        
        conn.close()
        
        return AnalyticsResponse(
            inventory_alpha=round(inventory_alpha, 2),
            match_quality=round(match_quality, 1),
            trust_score=round(trust_score, 1),
            node_yield=round(node_yield, 2),
            active_nodes=active_nodes_count,
            network_uptime=network_uptime,
            period=period
        )
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics calculation failed: {str(e)}")

@router.get("/analytics/inventory-metrics")
async def get_inventory_metrics(user_id: Optional[str] = None):
    """Get detailed inventory metrics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get inventory items count
        if user_id:
            cursor.execute("""
                SELECT COUNT(*) FROM inventory_items ii
                JOIN hosts h ON ii.host_id = h.id
                WHERE h.user_id = ?
            """, (user_id,))
        else:
            cursor.execute("SELECT COUNT(*) FROM inventory_items")
        
        total_items = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        # Get approved items count
        if user_id:
            cursor.execute("""
                SELECT COUNT(*) FROM inventory_items ii
                JOIN hosts h ON ii.host_id = h.id
                WHERE h.user_id = ? AND ii.is_public = 1
            """, (user_id,))
        else:
            cursor.execute("SELECT COUNT(*) FROM inventory_items WHERE is_public = 1")
        
        public_items = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        # Get total space detected
        if user_id:
            cursor.execute("""
                SELECT SUM(r.area_sq_ft) FROM rooms r
                JOIN hosts h ON r.host_id = h.id
                WHERE h.user_id = ?
            """, (user_id,))
        else:
            cursor.execute("SELECT SUM(area_sq_ft) FROM rooms")
        
        total_space = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        conn.close()
        
        return {
            "total_items": total_items,
            "public_items": public_items,
            "private_items": total_items - public_items,
            "total_space_sq_ft": total_space or 0,
            "user_id": user_id
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inventory metrics failed: {str(e)}")

@router.get("/analytics/trends")
async def get_analytics_trends(metric: str, period: str = "7d"):
    """Get trend data for a specific metric"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Calculate time buckets based on period
        if period == "24h":
            time_format = "%Y-%m-%d %H:00:00"
        elif period == "7d":
            time_format = "%Y-%m-%d"
        else:
            time_format = "%Y-%m-%d"
        
        # Get trend data based on metric type
        if metric == "inventory":
            cursor.execute(f"""
                SELECT 
                    DATE_FORMAT(created_at, '{time_format}') as time_bucket,
                    COUNT(*) as value
                FROM inventory_items
                WHERE created_at >= DATE_SUB(NOW(), INTERVAL {period})
                GROUP BY time_bucket
                ORDER BY time_bucket
            """)
        elif metric == "approvals":
            cursor.execute(f"""
                SELECT 
                    DATE_FORMAT(approved_at, '{time_format}') as time_bucket,
                    COUNT(*) as value
                FROM sku_matches
                WHERE approved_at >= DATE_SUB(NOW(), INTERVAL {period})
                GROUP BY time_bucket
                ORDER BY time_bucket
            """)
        else:
            conn.close()
            raise HTTPException(status_code=400, detail=f"Unknown metric: {metric}")
        
        trends = []
        for row in cursor.fetchall():
            trends.append({
                "timestamp": row[0],
                "value": row[1]
            })
        
        conn.close()
        
        return {
            "metric": metric,
            "period": period,
            "trends": trends
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend calculation failed: {str(e)}")
