import datetime
from typing import Dict, Any, Optional

class UserProfile:
    """Represents a platform user and their specific behavioral patterns."""
    def __init__(self, user_id: str, psychology_profile: str):
        self.user_id = user_id
        # psychology_profile examples: 'emotional_eater', 'social_eater', 'routine_eater'
        self.psychology_profile = psychology_profile

class ContextEngine:
    """
    The Data Integration Layer (Simulated).
    Ingests continuous telemetry and calculates a 'Vulnerability Score'.
    """
    def __init__(self):
        # Coordinates representing geographic 'vulnerability zones' (e.g. fast-food corridors)
        self.fast_food_zones = [
            {"lat": 34.0522, "lon": -118.2437, "radius_km": 1.5}
        ]

    def _is_in_vulnerability_zone(self, lat: float, lon: float) -> bool:
        # A simplified geospatial bounding-box check
        for zone in self.fast_food_zones:
            if abs(zone["lat"] - lat) < 0.05 and abs(zone["lon"] - lon) < 0.05:
                return True
        return False

    def evaluate_context(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes raw telemetry into an actionable contextual state.
        """
        state = {
            "vulnerability_score": 0,
            "biological_need": "high" if telemetry.get("blood_glucose", 100) < 70 else "normal",
            "stress_level": "high" if telemetry.get("hrv", 50) < 30 else "normal",
            "sleep_deprived": telemetry.get("sleep_score", 100) < 60,
            "in_danger_zone": self._is_in_vulnerability_zone(telemetry.get("lat", 0), telemetry.get("lon", 0)),
            "time_of_day": telemetry.get("timestamp").hour
        }
        
        # Calculate a vulnerability score based on compounded risk factors
        score = 0
        if state["biological_need"] == "high": score += 30
        if state["stress_level"] == "high": score += 20
        if state["sleep_deprived"]: score += 20
        if state["in_danger_zone"]: score += 30
        
        state["vulnerability_score"] = score
        return state

class JITAI_Engine:
    """
    Just-In-Time Adaptive Intervention Engine.
    Uses the BJ Fogg Model (Behavior = Motivation + Ability + Prompt).
    """
    def __init__(self):
        pass

    def generate_intervention(self, user: UserProfile, context_state: Dict[str, Any]) -> Optional[str]:
        """
        Trigger an intervention only if the context suggests the user is vulnerable to a poor habit loop.
        """
        # Threshold to trigger an intervention
        if context_state["vulnerability_score"] < 60:
            return None 
            
        print(f"[SYSTEM] High Vulnerability Detected (Score: {context_state['vulnerability_score']}/100) for User: {user.user_id}")
        
        # Determine the Prompt based on the User's Psychology Profile
        if user.psychology_profile == "emotional_eater":
            if context_state["stress_level"] == "high":
                return ("NUDGE (Emotional Eater Profile):\n"
                        "💡 The data shows your HRV just dropped, indicating a stress spike. "
                        "Before turning to food for comfort, let's try a 2-minute somatic breathing exercise to reset your nervous system.")
                
        elif user.psychology_profile == "routine_eater":
            if context_state["in_danger_zone"] and context_state["sleep_deprived"]:
                 return ("NUDGE (Routine Eater Profile):\n"
                         "🍔 We noticed you had a rough night of sleep, making cravings harder to fight, and you're near a high-friction food zone.\n"
                         "✅ Let's make it easy: I found a Sweetgreen 2 blocks ahead. Tap here to 1-click order your usual wholesome grain bowl for curbside pickup.")

        return ("NUDGE (General Profile):\n"
                "📉 Your energy is dropping. Grab a handful of almonds to stabilize your glucose levels.")

def simulate_platform():
    context_engine = ContextEngine()
    intervention_engine = JITAI_Engine()
    
    # Simulate a user with a specific profile
    user1 = UserProfile(user_id="U-775", psychology_profile="routine_eater")
    
    # Mock telemetry stream: User is sleep deprived (55), normal HRV and glucose, driving near fast food at 6 PM (18:00)
    mock_telemetry_event = {
        "timestamp": datetime.datetime.now().replace(hour=18),
        "hrv": 45, 
        "sleep_score": 55, 
        "blood_glucose": 85, 
        "lat": 34.0520, 
        "lon": -118.2430
    }
    
    print("--- 1. Ingesting & Analyzing Telemetry ---")
    current_context = context_engine.evaluate_context(mock_telemetry_event)
    for key, val in current_context.items():
        print(f"  > {key}: {val}")
    
    print("\n--- 2. Running Behavioral Engine (JITAI) ---")
    nudge = intervention_engine.generate_intervention(user1, current_context)
    
    if nudge:
        print(f"\n🔔 DELIVERED NOTIFICATION:\n{nudge}")
    else:
        print("\n✅ No intervention required. System monitoring silently.")

if __name__ == '__main__':
    simulate_platform()
