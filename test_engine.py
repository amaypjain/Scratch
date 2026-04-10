import unittest
from datetime import datetime
from src.models import UserProfile, TelemetryData
from src.context_engine import ContextEngine
from src.jitai_engine import JITAI_Engine
from src.config import Config

class TestNutritionalIntelligence(unittest.TestCase):

    def setUp(self):
        self.context_engine = ContextEngine()
        self.jitai_engine = JITAI_Engine()
        self.user_general = UserProfile("U-1", "general")
        self.user_routine = UserProfile("U-2", "routine_eater")
        self.user_emotional = UserProfile("U-3", "emotional_eater")

    def test_telemetry_validation(self):
        # Valid telemetry
        valid_data = {
            "hrv": 50, "sleep_score": 80, "blood_glucose": 90, 
            "lat": 10.0, "lon": 10.0
        }
        telemetry = TelemetryData.from_dict(valid_data)
        self.assertEqual(telemetry.hrv, 50)
        self.assertIsInstance(telemetry.timestamp, datetime)

        # Invalid telemetry
        invalid_data = {"hrv": 50} # Missing required fields
        with self.assertRaises(ValueError):
            TelemetryData.from_dict(invalid_data)

    def test_user_profile_validation(self):
        with self.assertRaises(ValueError):
            UserProfile("U-X", "invalid_profile")

    def test_context_evaluation_safe(self):
        telemetry = TelemetryData(
            timestamp=datetime.now(),
            hrv=60, # Good
            sleep_score=90, # Good
            blood_glucose=100, # Good
            lat=0.0, lon=0.0 # Safe zone
        )
        state = self.context_engine.evaluate_context(telemetry)
        self.assertEqual(state.vulnerability_score, 0)
        self.assertFalse(state.sleep_deprived)

    def test_context_evaluation_vulnerable(self):
        # Coordinates matching the danger zone in config.py
        danger_zone = Config.DANGER_ZONES[0]
        
        telemetry = TelemetryData(
            timestamp=datetime.now(),
            hrv=20, # Bad (<30)
            sleep_score=40, # Bad (<60)
            blood_glucose=60, # Bad (<70)
            lat=danger_zone["lat"], lon=danger_zone["lon"] # Danger zone!
        )
        state = self.context_engine.evaluate_context(telemetry)
        
        # 30 (glucose) + 20 (hrv) + 20 (sleep) + 30 (zone) = 100
        self.assertEqual(state.vulnerability_score, 100)
        self.assertTrue(state.in_danger_zone)
        self.assertTrue(state.sleep_deprived)
        self.assertEqual(state.stress_level, "high")
        self.assertEqual(state.biological_need, "high")

    def test_jitai_no_intervention(self):
        state = self.context_engine.evaluate_context(TelemetryData(
            timestamp=datetime.now(), hrv=60, sleep_score=90, blood_glucose=100, lat=0.0, lon=0.0
        ))
        # Vuln score is 0, threshold is 60. Should return None.
        nudge = self.jitai_engine.generate_intervention(self.user_routine, state)
        self.assertIsNone(nudge)

    def test_jitai_intervention_routine_eater(self):
        danger_zone = Config.DANGER_ZONES[0]
        state = self.context_engine.evaluate_context(TelemetryData(
            timestamp=datetime.now(), hrv=60, sleep_score=40, blood_glucose=100, lat=danger_zone["lat"], lon=danger_zone["lon"]
        ))
        
        nudge = self.jitai_engine.generate_intervention(self.user_routine, state)
        self.assertIsNotNone(nudge)
        self.assertIn("Sweetgreen", nudge)

if __name__ == '__main__':
    unittest.main()
