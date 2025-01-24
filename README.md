# Credit Card Analysis

## Overview
The Credit Card Analysis tool helps users identify the most effective credit card for their spending habits. By analyzing various categories of expenditures and cross-referencing them with the rewards and benefits provided by different credit cards, the tool provides data-driven suggestions to maximize cashback or rewards points.

## Features
### Current Functionalities:
1. **Best Card for Each Category**
    - Identifies the top credit card for each spending category (e.g., groceries, dining, travel, etc.) based on reward multipliers.

2. **Top N Recommendations**
    - Provides a ranked list of the top N (default of 3) credit cards overall based on user-specified spending across all categories.

3. **Analyze Spending**
    - Gives the user data on how optimized their spending is based on if they are using the best card they have in their wallet for the
     spending category.
        - Shows overall spend-optimization score and amount of missed rewards
        - Shows most optimized spend category
        - Shows lease optimized spend category

4. **Visualize Spending**
    - Opens a chart showing the users the amount spent per category

5. **Show Wallet**
    - Shows user's current wallet information
        -  card name
        - company
        - annual fee
        - reward multipliers

### Potential Enhancements:
While not yet implemented, future ideas include:
- Storing data in a database
- Frontend React-based UI
- User management/auth
- Integrate with a service like Plaid for real user data

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/chrisyecora/credit-card-analysis.git
   ```

2. Navigate to the project directory:
   ```bash
   cd credit-card-analysis
   ```

## Usage

1. Run the analysis tool:
   ```bash
   python -m src.main
   ```

## Project Structure
```
credit-card-analysis/
│
├── data/
    ├── static/           # static datasets
    ├── dynamic/          # dynamically generated datasets    
├── src/                  # Source code for the analysis logic.
├── .gitignore            # Git ignore file.
├── README.md             # Project documentation (this file).
└── requirements.txt      # Python dependencies.
```

## Dataset
The project includes a JSON file with data on 30 credit cards, stored in `data/creditcards.json`. Each entry contains:
- Card name
- Annual fee
- Reward multipliers for categories like groceries, dining, travel, gas, online shopping, entertainment, and others.
