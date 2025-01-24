# card_optimizer/__init__.py

# Directly expose best_card_for_category for convenience
from .card_utils import best_card_for_category
from .card_utils import get_reward_rate_by_card_name
from .utils import load_json
from .utils import generate_random_data
from .utils import format_currency
from .user_utils import format_card_benefits
from .spending_analysis import analyze_spending
from .spending_analysis import recommend_new_cards
from .spending_analysis import calc_spend_by_cat
# from .recommendations import suggest_new_cards
# from .reward_simulation import simulate_rewards

# You can also define any necessary constants or setup here
__all__ = ['best_card_for_category']
