import json
from src import load_json, best_card_for_category, get_reward_rate_by_card_name

#BEGIN PUBLIC FUNCTIONS

def recommend_new_cards(wallet: dict) -> list[dict[str, object]]:
    """
    Suggests new credit cards to the user to open based on spending habits.
    
    Cards are recommended in order of estimated additional rewards earned.
    
    Args:
        wallet (dict): User's current wallet
    
    Returns:
        list of dictionaries:
            - "card_name" (str): Name of the recommended card
            - "category" (str): Spending category
            - "potential_rate" (int): Reward rate if using the recommended card
            - "current_rate" (int): Reward rate the user is currently earning
            - "additional_rewards" (int): Estimated additional rewards earned
        
        Example:
        [
            {
                "card_name": "Amex Gold Card",
                "category": "restaurants",
                "potential_rate": 4,
                "current_rate": 2,
                "additional_rewards": 500
            }
        ]
    """
    # convert wallet to dict of names for O(1) lookups
    user_cards = {}
    for card in wallet:
        name = card["name"]
        user_cards[name] = 1


    all_cards = load_json('data/static/creditcards.json')["creditcards"]
    user_spending = calc_spend_by_cat()
    best_current_cards = best_card_for_category()

    reward_gaps = []
    for category, spend in user_spending.items():
        current_rate = best_current_cards[category][1]
        
        for card in all_cards:
            # skip if user already has this card
            if card["name"] in user_cards:
                continue

            potential_rate = card['categories'].get(category, 0)
            reward_gap = ((potential_rate - current_rate) / 100) * spend
            if reward_gap > 0:
                reward_gaps.append({
                "card_name": card["name"],
                "category": category,
                "potential_rate": potential_rate,
                "current_rate": current_rate,
                "additional_rewards": reward_gap
            })
                
    # Sort by maximum reward gap and recommend the best card
    reward_gaps.sort(key=lambda x: x["additional_rewards"], reverse=True)
    return reward_gaps[:3]  # Top 3 recommendations



def analyze_spending() -> None:
    transactions = load_json('data/dynamic/transactions.json')["transactions"]
    wallet = load_json("data/dynamic/wallet.json")['wallet']
    categories = load_json('data/static/categories.json')['categories']
    best_cards = best_card_for_category() #user's best card for each category: dict

    results = {}
    correct_card_usage_counts = {}
    total_transactions_per_cat = {}
    total_transactions = len(transactions)


    # 1. Show the user the % of time they used the correct card for each category and total
    # 2. Show the associated amount of benefits that they missed
    missed_benefits = 0
    for transaction in transactions:
        card_used_name = transaction["card_name"]
        category = transaction["category"]
        total_transactions_per_cat[category] = 1 + total_transactions_per_cat.get(category, 0)


        if card_used_name == best_cards[category][0]:
            correct_card_usage_counts[category] = 1 + correct_card_usage_counts.get(category, 0)
        else:
            
            card_used_reward_rate = get_reward_rate_by_card_name(card_used_name, category)
            reward_earned = transaction["amount"] * (card_used_reward_rate / 100)
            potential_reward = transaction["amount"] * (best_cards[category][1] / 100)
            if potential_reward - reward_earned > 0:
                missed_benefits += (potential_reward - reward_earned)

    
    _display_usage_feedback(correct_card_usage_counts, total_transactions_per_cat, total_transactions, missed_benefits)


def calc_spend_by_cat() -> dict[str, int]:
    """
    Calculates the amount the user has spent per category
    
    Returns:
    dict [str, int] where \n
    key (str) = The spending category \n
    value (int) = Amount spent in the category
    """

    transactions = load_json('data/dynamic/transactions.json')["transactions"]
    spend_by_cat = {}
    for transaction in transactions:
        category = transaction["category"]
        spend_by_cat[category] = transaction['amount'] + spend_by_cat.get(category, 0)

    return spend_by_cat

# BEGIN PRIVATE FUNCTIONS

def _display_usage_feedback(correct_usages : dict[str, int], total_transactions_by_cat : dict[str, int], total_transactions: int, missed_benefits: int) -> None:
    total_correct_usage = sum(correct_usages.values())
    total_usage_pctage = (total_correct_usage / total_transactions) * 100

    print(f"You used the best card for {total_correct_usage} out of {total_transactions} transactions!")
    print(f"That's {total_usage_pctage:.2f}% optimized usage.\n")

    if total_usage_pctage == 100:
        print("🔥 Perfect! You're optimizing your rewards perfectly. Keep up the great work!")
    elif total_usage_pctage >= 75:
        print("👍 Great job! You're using the best card for most transactions. Keep refining!")
    elif total_usage_pctage >= 50:
        print("✨ You're halfway there! Consider revisiting your wallet to maximize your rewards.")
    else:
        print("😕 There's room for improvement. Use the tool to identify opportunities to optimize!")

    best_cat = _calc_best_category(correct_usages, total_transactions_by_cat)
    worst_cat = _calc_worst_category(correct_usages, total_transactions_by_cat)

    if missed_benefits > 0:
        print(f"\nIn total, you missed out on ${missed_benefits:.2f} of rewards!\n")

    print(f"⭐ {best_cat[0]} was your most optimized category at {best_cat[1]*100:.2f}%.\n")
    print(f"⚠️  {worst_cat[0]} was your least optimized category at {worst_cat[1]*100:.2f}%.\n\n")

    
def _calc_best_category(correct_usages: dict[str, int], totals: dict[str, int]) -> tuple[str, int]:
    best = None
    best_rate = 0
    for cat, count in correct_usages.items():
        rate = count / totals[cat]
        if rate > best_rate:
            best_rate = rate
            best = (cat.capitalize().replace('_', ' '), best_rate)
    
    return best


def _calc_worst_category(correct_usages: dict[str, int], totals: dict[str, int]) -> tuple[str, int]:
    worst = None
    worst_rate = 1.1
    for cat, count in correct_usages.items():
        rate = count / totals[cat]
        if rate < worst_rate:
            worst_rate = rate
            worst = (cat.capitalize().replace('_', ' '), worst_rate)
    
    return worst

