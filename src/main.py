import sys
from tabulate import tabulate
import src
import matplotlib.pyplot as plt


    
def main():

    print("**** Generating random data ****")
    if not src.generate_random_data():
        print("ERROR: Generating random data, exiting program")
        sys.exit()
    print("**** Done generating random data ****")
    print("**** Retrieving user info ****")
    wallet = src.load_json("data/dynamic/wallet.json")["wallet"]
    print("**** Done retrieving user data ****")

    while True:
        display_menu()
        choice = input("\nEnter your choice (q to quit): ").strip()

        if choice == '1':
            _show_wallet()
        elif choice == '2':
            _best_card_for_category()
        elif choice == '3':
            _analyze_spending()
        elif choice == '4':
            _visualize_spending()
        elif choice == '5':
            _suggest_new_cards(wallet)
        elif choice == '6':
            _new_data()
        elif choice == 'q':
            print("\nExiting the program.")
            sys.exit()  # Exit the program
        else:
            print("\nInvalid option! Please choose a number between 1 and 7.")



def display_menu():
    print("\n*** Credit Card Optimizer Menu ***")
    print("1. Show Wallet")
    print("2. Best Card for Each Category")
    print("3. Analyze Spending and Card Utilization")
    print("4. Visualize Spending Trends")
    print("5. Suggest New Cards Based on Spending")
    print("6. Generate New Mock Data")
    print("7. Exit")

def _show_wallet():
    wallet = src.load_json('data/dynamic/wallet.json')['wallet']
    formatted_wallet = src.format_card_benefits(wallet)
    print(tabulate(formatted_wallet, headers="keys", tablefmt="fancy_grid"))
    

def _best_card_for_category():
    best_card_data = src.best_card_for_category()
    headers = ["Category", "Best Card", "Reward (%)"]
    table_data = []
    
    for category, card in best_card_data.items():
        table_data.append([category.capitalize().replace('_', ' '), card[0], card[1]])

    print(tabulate(table_data, headers, tablefmt="fancy_grid"))

def _analyze_spending():
    src.analyze_spending()

def _visualize_spending():
    data = src.calc_spend_by_cat()
    _display_spending_trends(data)

def _suggest_new_cards(wallet: dict[str, object]):
    suggestions = src.recommend_new_cards(wallet)
    _display_card_recommendations(suggestions)

def _new_data():
    print("\n****Crunching numbers...****")
    print("**** Generating random data ****")
    if not src.generate_random_data():
        print("ERROR: Generating random data, exiting program")
        sys.exit()
    print("**** Done generating random data ****")

def _display_card_recommendations(suggetions):
    headers = headers=["Card Name", "Category", "Potential Reward", "Current Best", "Improvement", "Additional Rewards"]
    table_data = []
    for suggestion in suggetions:
        improvement = suggestion["potential_rate"] - suggestion["current_rate"]
        table_data.append([
            suggestion["card_name"],
            suggestion["category"].capitalize(),
            f"{suggestion['potential_rate']:.1f}%",
            f"{suggestion['current_rate']:.1f}%",
            f"+{improvement:.1f}%",
            src.format_currency(suggestion["additional_rewards"]),
        ])
    
    print(f"\n*** Top {len(suggetions)} Recommended Cards For You***")
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))

def _display_spending_trends(spending_data):
    categories = spending_data.keys()
    amounts = spending_data.values()

    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color="skyblue")
    plt.title("Spending Trends by Category", fontsize=14)
    plt.ylabel("Spending Amount ($)", fontsize=12)
    plt.xlabel("Category", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
