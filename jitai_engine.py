from typing import Optional
from .models import UserProfile, ContextState
from .config import Config
from .utils import setup_logger

logger = setup_logger(__name__)

class JITAI_Engine:
    """
    Just-In-Time Adaptive Intervention Engine.
    Uses the BJ Fogg Model (Behavior = Motivation + Ability + Prompt).
    """
    def __init__(self, config=Config):
        self.config = config

    def generate_intervention(self, user: UserProfile, context_state: ContextState) -> Optional[str]:
        """
        Trigger an intervention only if the user is vulnerable to a poor habit loop.
        """
        if context_state.vulnerability_score < self.config.VULNERABILITY_THRESHOLD_CRITICAL:
            logger.debug(f"User {user.user_id} vulnerability score ({context_state.vulnerability_score}) below threshold. Skipping intervention.")
            return None 
            
        # Route intervention logic based on psychology profile
        try:
            handler = getattr(self, f"_handle_{user.psychology_profile}")
            return handler(context_state)
        except AttributeError:
            logger.warning(f"No specific handler for profile '{user.psychology_profile}'. Falling back to general.")
            return self._handle_general(context_state)

    def _handle_emotional_eater(self, state: ContextState) -> Optional[str]:
        if state.stress_level == "high":
            return ("NUDGE (Emotional Eater):\n"
                    "💡 The data shows your HRV just dropped, indicating a stress spike. "
                    "Before turning to food for comfort, let's try a 2-minute somatic breathing exercise to reset your nervous system.")
        return self._handle_general(state)

    def _handle_routine_eater(self, state: ContextState) -> Optional[str]:
        if state.in_danger_zone and state.sleep_deprived:
             return ("NUDGE (Routine Eater):\n"
                     "🍔 We noticed you had a rough night of sleep, making cravings harder to fight, and you're near a high-friction food zone.\n"
                     "✅ Let's make it easy: I found a Sweetgreen 2 blocks ahead. Tap here to 1-click order your usual wholesome grain bowl for curbside pickup.")
        return self._handle_general(state)
        
    def _handle_general(self, state: ContextState) -> Optional[str]:
        if state.biological_need == "high":
            return ("NUDGE (General Profile):\n"
                    "📉 Your energy is dropping. Grab a handful of almonds to stabilize your glucose levels.")
        elif state.vulnerability_score >= self.config.VULNERABILITY_THRESHOLD_CRITICAL:
            return ("NUDGE (General Profile):\n"
                    "🛑 Your vulnerability indicators are high right now. Take a moment to drink water and assess your cravings intentionally.")
        return None
