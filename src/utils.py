import json
import random
import uuid
import re
from datetime import datetime, timedelta

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
    
def format_currency(number):
    number_str = f"{number:.2f}"
    number_str = re.sub(r"(?<=\d)(?=(\d{3})+(?!\d))", ",", number_str)
    number_str = "$" + number_str
    return number_str

def generate_random_data() -> bool:
    if not _generate_random_wallet():
        return False
    if not _generate_random_transactions():
        return False

    return True
    

def _generate_random_wallet(num_cards=5) -> bool:
    try:
        all_cards = load_json("data/static/creditcards.json")["creditcards"]
        random.shuffle(all_cards)

        # Select the first num_cards cards
        wallet = all_cards[:num_cards]


        with open("data/dynamic/wallet.json", "w") as f:
            json.dump({"wallet": wallet}, f, indent=4)

        return True  # Return True if successful
    except Exception as e:
        print(f"Error generating wallet: {e}")
        return False  # Return False if an error occurred
    
    
def _generate_random_transactions(num_transactions=100) -> None:
    try:
        wallet = load_json("data/dynamic/wallet.json")["wallet"]
        categories = load_json("data/static/categories.json")["categories"]
        transactions = []
        
        for _ in range(num_transactions):
            card = random.choice(wallet)
            category = random.choice(categories)
            amount = round(random.uniform(1, 100), 2)  # Random spending amount between $1 and $100
            date = datetime.now() - timedelta(days=random.randint(0, 30))  # Random date in the last month
            transaction_id = str(uuid.uuid4())  # Generate a unique ID as a string

            transaction = {
                "id": transaction_id,
                "date": date.strftime("%Y-%m-%d"),
                "category": category,
                "amount": amount,
                "card_name": card["name"],  # Assign the card to the transaction
            }
            transactions.append(transaction)
        
        with open("data/dynamic/transactions.json", "w") as f:
            json.dump({"transactions": transactions}, f, indent=4)

        return True
    
    except Exception as e:
        print(f"Error generating transactions: {e}")
        return False  # Return False if an error occurred
