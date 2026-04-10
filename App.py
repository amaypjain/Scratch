import datetime
import traceback
from src.models import UserProfile, TelemetryData
from src.context_engine import ContextEngine
from src.jitai_engine import JITAI_Engine
from src.config import Config
from src.utils import setup_logger

logger = setup_logger("main")

def get_user_input():
    print("\n--- Enter Telemetry Data ---")
    try:
        hrv = float(input("Enter HRV (Heart Rate Variability, e.g., 20-100): "))
        sleep_score = float(input("Enter Sleep Score (0-100): "))
        blood_glucose = float(input("Enter Blood Glucose (mg/dL, e.g., 60-150): "))
        
        in_danger = input("Are you currently near a fast-food zone? (y/n): ").strip().lower()
        if in_danger == 'y':
            lat = Config.DANGER_ZONES[0]["lat"]
            lon = Config.DANGER_ZONES[0]["lon"]
        else:
            lat = 0.0 # Safe coordinate
            lon = 0.0
            
        time_hour = input("Enter current hour (0-23, or press enter for now): ").strip()
        timestamp = datetime.datetime.now()
        if time_hour.isdigit() and 0 <= int(time_hour) <= 23:
            timestamp = timestamp.replace(hour=int(time_hour))
            
        return {
            "timestamp": timestamp,
            "hrv": hrv,
            "sleep_score": sleep_score,
            "blood_glucose": blood_glucose,
            "lat": lat,
            "lon": lon
        }
    except ValueError:
        print("Invalid input! Please enter numbers where requested.")
        return None

def simulate_platform():
    logger.info("Initializing Context-Aware Nutritional Intelligence Platform...\n")
    
    context_engine = ContextEngine()
    intervention_engine = JITAI_Engine()
    
    # Let user select profile
    print("Available Psychology Profiles:")
    print("1. general")
    print("2. routine_eater")
    print("3. emotional_eater")
    
    profile_choice = input("Select your profile (1-3) [Default: 2]: ").strip()
    profile_map = {"1": "general", "2": "routine_eater", "3": "emotional_eater"}
    selected_profile = profile_map.get(profile_choice, "routine_eater")
    
    try:
        user = UserProfile(user_id="U-775", psychology_profile=selected_profile)
        logger.info(f"Loaded Profile: {user.user_id} ({user.psychology_profile})")
    except ValueError as e:
        logger.error(f"Failed to load user profile. {e}")
        return

    # Let user select data source
    print("\nSelect Data Source:")
    print("1. Run Default Highly-Vulnerable Scenario")
    print("2. Enter Manual Telemetry Input")
    data_source = input("Choice (1-2) [Default: 1]: ").strip()
    
    if data_source == "2":
        mock_telemetry_dict = get_user_input()
        if not mock_telemetry_dict: return
    else:
        mock_telemetry_dict = {
            "timestamp": datetime.datetime.now().replace(hour=18),
            "hrv": 20,                  # High stress
            "sleep_score": 40,          # Sleep deprived (< 60)
            "blood_glucose": 65,        # Low glucose
            "lat": Config.DANGER_ZONES[0]["lat"], # Danger Zone
            "lon": Config.DANGER_ZONES[0]["lon"]
        }
    
    print("\n" + "="*50)
    logger.info("--- 1. Ingesting & Validating Telemetry ---")
    try:
        telemetry = TelemetryData.from_dict(mock_telemetry_dict)
    except Exception as e:
        logger.error(f"Invalid Telemetry Data dropped: {e}")
        return
        
    logger.info("--- 2. Evaluating Context ---")
    current_context = context_engine.evaluate_context(telemetry)
    
    logger.info(f"Context State Discovered:")
    logger.info(f" > Vulnerability Score: {current_context.vulnerability_score}/100")
    logger.info(f" > Biological Need: {current_context.biological_need}")
    logger.info(f" > Stress Level: {current_context.stress_level}")
    logger.info(f" > Sleep Deprived: {current_context.sleep_deprived}")
    logger.info(f" > In Danger Zone: {current_context.in_danger_zone}")
    
    logger.info("\n--- 3. Running Behavioral Engine (JITAI) ---")
    nudge = intervention_engine.generate_intervention(user, current_context)
    
    print("=" * 50)
    if nudge:
        print(f"🔔 DELIVERED NOTIFICATION to {user.user_id}:\n\n{nudge}")
    else:
        print(f"✅ No intervention required for {user.user_id}. System monitoring silently.")
    print("=" * 50)

if __name__ == '__main__':
    try:
        simulate_platform()
    except KeyboardInterrupt:
        print("\nExiting simulation.")
    except Exception as e:
        logger.fatal(f"System crashed unexpectedly: {e}")
        traceback.print_exc()
