from .config import Config
from .models import TelemetryData, ContextState
from .utils import setup_logger, haversine_distance

logger = setup_logger(__name__)

class ContextEngine:
    """
    The Data Integration Layer.
    Ingests continuous telemetry and calculates a 'Vulnerability Score'.
    """
    def __init__(self, config=Config):
        self.config = config
        self.danger_zones = self.config.DANGER_ZONES

    def _is_in_vulnerability_zone(self, lat: float, lon: float) -> bool:
        """
        Uses Haversine distance to check if user is near any known danger zone.
        In production, this could query a map API or a geo-spatial DB.
        """
        for zone in self.danger_zones:
            dist = haversine_distance(lat, lon, zone["lat"], zone["lon"])
            if dist <= zone.get("radius_km", self.config.ZONE_RADIUS_KM):
                return True
        return False

    def evaluate_context(self, telemetry: TelemetryData) -> ContextState:
        """
        Synthesizes raw telemetry into an actionable contextual state
        and calculates an aggregate vulnerability score.
        """
        state = ContextState()
        state.time_of_day = telemetry.timestamp.hour

        # Evaluate Biological need
        if telemetry.blood_glucose < self.config.LOW_BLOOD_GLUCOSE_THRESHOLD:
            state.biological_need = "high"
        
        # Evaluate Stress
        if telemetry.hrv < self.config.HIGH_STRESS_HRV_THRESHOLD:
            state.stress_level = "high"

        # Evaluate Sleep Quality
        if telemetry.sleep_score < self.config.LOW_SLEEP_SCORE_THRESHOLD:
            state.sleep_deprived = True
            
        # Evaluate Environmental Friction
        if self._is_in_vulnerability_zone(telemetry.lat, telemetry.lon):
            state.in_danger_zone = True

        # Calculate Vulnerability Score Weighting
        score = 0
        if state.biological_need == "high": score += 30
        if state.stress_level == "high": score += 20
        if state.sleep_deprived: score += 20
        if state.in_danger_zone: score += 30
        
        state.vulnerability_score = min(score, 100) # Cap at 100
        
        logger.info(f"Context Evaluated. Vulnerability Score: {state.vulnerability_score}")
        return state
