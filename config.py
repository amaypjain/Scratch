"""
Configuration thresholds and system settings.
"""

class Config:
    # Vulnerability Thresholds
    VULNERABILITY_THRESHOLD_CRITICAL = 60
    
    # Biological Markers
    LOW_BLOOD_GLUCOSE_THRESHOLD = 70  # mg/dL
    HIGH_STRESS_HRV_THRESHOLD = 30    # ms
    LOW_SLEEP_SCORE_THRESHOLD = 60    # /100 score
    
    # Geolocation math configurations
    ZONE_RADIUS_KM = 1.5              # Default vulnerability zone radius

    # Mock Database of 'Danger Zones' Fast Food Corridors
    # In a full app, this would query Google Maps Places API for nearby fast food.
    DANGER_ZONES = [
        {"name": "Downtown Fast Food Alley", "lat": 34.0522, "lon": -118.2437, "radius_km": 1.5}
    ]
