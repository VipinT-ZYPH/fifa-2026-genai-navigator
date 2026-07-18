# Stadium data and utilities
import json
from typing import List, Dict

STADIUM_DATA = {
    "name": "FIFA 2026 Stadium",
    "capacity": 80000,
    "zones": {
        "A": {"name": "North Stand", "gates": ["A1", "A2", "A3"]},
        "B": {"name": "South Stand", "gates": ["B1", "B2", "B3"]},
        "C": {"name": "East Stand", "gates": ["C1", "C2"]},
        "D": {"name": "West Stand", "gates": ["D1", "D2"]},
    },
    "facilities": {
        "bathrooms": [
            {"id": "B1", "location": "Zone A", "accessible": True, "wait_time": 5},
            {"id": "B2", "location": "Zone B", "accessible": True, "wait_time": 12},
            {"id": "B3", "location": "Zone C", "accessible": False, "wait_time": 8},
            {"id": "B4", "location": "Zone D", "accessible": True, "wait_time": 3},
        ],
        "food_courts": [
            {"id": "F1", "location": "Zone A", "cuisine": "Local", "wait_time": 15},
            {"id": "F2", "location": "Zone B", "cuisine": "International", "wait_time": 20},
            {"id": "F3", "location": "Zone C", "cuisine": "Vegetarian", "wait_time": 10},
        ],
        "medical": [
            {"id": "M1", "location": "Zone A", "type": "First Aid", "distance_m": 150},
            {"id": "M2", "location": "Zone D", "type": "Emergency", "distance_m": 200},
        ],
        "accessibility": {
            "wheelchair_ramps": [
                {"location": "Gate A1", "accessible": True},
                {"location": "Gate B2", "accessible": True},
                {"location": "Gate C1", "accessible": False},
                {"location": "Gate D1", "accessible": True},
            ],
            "accessible_seating": [
                {"zone": "A", "count": 50, "available": 12},
                {"zone": "B", "count": 50, "available": 8},
                {"zone": "C", "count": 30, "available": 5},
                {"zone": "D", "count": 40, "available": 20},
            ]
        }
    },
    "crowd_density": {
        "A": 85,
        "B": 72,
        "C": 60,
        "D": 90,
    }
}

def get_closest_facility(zone: str, facility_type: str) -> Dict:
    """Get closest facility of given type to user's zone"""
    facilities = STADIUM_DATA["facilities"].get(facility_type, [])

    if not facilities:
        return None

    # Prefer accessible facilities for bathrooms
    if facility_type == "bathrooms":
        accessible = [f for f in facilities if f.get("accessible", False)]
        return accessible[0] if accessible else facilities[0]

    return facilities[0]


def get_crowd_status() -> Dict:
    """Get current crowd density in each zone"""
    return STADIUM_DATA["crowd_density"]

def get_accessible_routes(from_zone: str, to_facility: str) -> List[str]:
    """Generate accessible route description"""
    return [
        f"From {from_zone}: Take main corridor (ramp available)",
        "Follow blue accessibility signs",
        f"Estimated walking time: 5-8 minutes",
        "Elevators available at junction points"
    ]