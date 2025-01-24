from src.utils import load_json

def _calc_best_other_card(wallet):
    max_reward = 0
    best_card = None
    for card in wallet:
        reward = card['categories']['other']
        if reward > max_reward:
            max_reward = reward
            best_card = (card['name'], reward)
    return best_card


def best_card_for_category() -> dict:
    """
    Calculates the best card in the user's wallet for each spending category
    
    Returns:
    dict: [str, (str, int)] \n\n
    example: ["groceries", ("Amex Gold", 4)]
    """
    wallet = load_json('data/dynamic/wallet.json')['wallet']
    categories = load_json('data/static/categories.json')['categories']
    output = {}
    sum_percentages = 0
    for category in categories:
        if category == 'other':
            continue

        best_card = None
        best_reward = 0
        best_other_card = _calc_best_other_card(wallet)

        for card in wallet:
            if category not in card['categories']:
                continue
            reward = card['categories'][category]
            if reward > best_reward:
                best_reward = reward
                best_card = (card['name'], reward)
        
        if best_card is None:
            best_card = best_other_card

        output[category] = best_card
        sum_percentages += best_card[1]
    

    output["other"] = best_other_card
    average_cashback = sum_percentages / len(categories)
    output["Total Average Cashback"] = ("", round(average_cashback, 1))
    
    return output


def get_reward_rate_by_card_name(card_name: str, category: str) -> int | None:
    """
    Retrieve the reward rate for the specified category on the specified card

    Args:
        card_name (str): The name of the card to search for.

        category (str): The name of the category to look at

    Returns:
        int: reward rate | None if card not found
    """
    card = get_card_by_name(card_name)

    if not card:
        return None

    if category in card:
        return card["categories"][category]
    else:
        return card["categories"]["other"]
            


def get_card_by_name(card_name: str) -> dict | None:
    """
    Retrieve the a card object by the given card name

    Args:
        card_name (str): The name of the card to search for.

    Returns:
        card object (dict) | None
    """
    wallet = load_json("data/dynamic/wallet.json")["wallet"]
    for card in wallet:
        if card["name"].lower() == card_name.lower():
            return card
    return None

