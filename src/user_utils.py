def format_card_benefits(wallet):
    formatted_cards = []
    for card in wallet:
        benefits = "\n".join([f"{category.capitalize().replace('_', ' ')}: {reward}%" 
                              for category, reward in card['categories'].items()])
        formatted_cards.append({
            "Card Name": card["name"],
            "Company": card["company"],
            "Annual Fee ($)": card["annual_fee"],
            "Benefits": benefits
        })
    return formatted_cards

