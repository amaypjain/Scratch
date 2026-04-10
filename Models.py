"""
Data models representing User Profiles, Telemetry, and Context.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class UserProfile:
    """Represents a platform user and their specific behavioral patterns."""
    user_id: str
    psychology_profile: str  # Options: 'emotional_eater', 'routine_eater', 'general'
    
    def __post_init__(self):
        valid_profiles = {'emotional_eater', 'routine_eater', 'general'}
        if self.psychology_profile not in valid_profiles:
            raise ValueError(f"Invalid psychology profile: {self.psychology_profile}. Must be one of {valid_profiles}")

@dataclass
class TelemetryData:
    """Incoming continuous raw data stream."""
    timestamp: datetime
    hrv: float
    sleep_score: float
    blood_glucose: float
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: dict) -> 'TelemetryData':
        """Safely extract from dict and validate."""
        # Check required fields
        required_keys = ['hrv', 'sleep_score', 'blood_glucose', 'lat', 'lon']
        missing_keys = [k for k in required_keys if k not in data]
        if missing_keys:
            raise ValueError(f"Missing telemetry telemetry fields: {missing_keys}")
            
        timestamp = data.get('timestamp')
        if not isinstance(timestamp, datetime):
            timestamp = datetime.now()  # Fallback gracefully
            
        return cls(
            timestamp=timestamp,
            hrv=float(data['hrv']),
            sleep_score=float(data['sleep_score']),
            blood_glucose=float(data['blood_glucose']),
            lat=float(data['lat']),
            lon=float(data['lon'])
        )

@dataclass
class ContextState:
    """Synthesized state evaluating the user's vulnerability."""
    vulnerability_score: int = 0
    biological_need: str = "normal"
    stress_level: str = "normal"
    sleep_deprived: bool = False
    in_danger_zone: bool = False
    time_of_day: int = field(default_factory=lambda: datetime.now().hour)
