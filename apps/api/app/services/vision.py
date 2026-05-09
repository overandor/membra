from typing import List, Dict

class VisionService:
    async def detect_objects(self, image_data: str) -> List[Dict]:
        mock_detections = [
            {"object": "power_drill", "confidence": 0.92, "suggested_price": "$7/hour", "risk": "low"},
            {"object": "tripod", "confidence": 0.88, "suggested_price": "$5/hour", "risk": "low"},
            {"object": "ring_light", "confidence": 0.95, "suggested_price": "$6/hour", "risk": "low"},
        ]
        return mock_detections
