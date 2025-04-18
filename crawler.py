import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import time

# Load API key from .env
load_dotenv()
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
print("Is API Key Loaded?:", ETHERSCAN_API_KEY is not None)


def get_transactions(wallet_address, start_block):
    print("get_transactions function called")
    print(f"Address: {wallet_address}, Start Block: {start_block}")

    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": int(start_block),
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=params)
    try:
        data = response.json()
    except Exception as e:
        print("Error parsing JSON:", e)
        return {"error": "JSON parsing failed"}

    if data.get("status") != "1":
        print("Error or no data:", data.get("message"))
        return {"error": data.get("message", "No data found")}

    transactions = []
    for tx in data["result"]:
        transactions.append({
            "hash": tx["hash"],
            "from": tx["from"],
            "to": tx["to"],
            "value_eth": int(tx["value"]) / 10 ** 18,
            "timestamp": tx["timeStamp"]
        })

    print(f"{len(transactions)} transactions found.")
    return transactions


def get_balance_by_date(wallet_address, date_str):
    print("ETH balance by date function called")

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    timestamp = int(time.mktime(dt.timetuple()))

    block_url = "https://api.etherscan.io/api"
    block_params = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": timestamp,
        "closest": "before",
        "apikey": ETHERSCAN_API_KEY
    }

    block_response = requests.get(block_url, params=block_params)
    block_data = block_response.json()

    if block_data["status"] != "1":
        return {"error": "Block not found"}

    transactions = get_transactions(wallet_address, 0)
    eth_balance = 0

    for tx in transactions:
        if int(tx["timestamp"]) <= timestamp:
            if tx["to"].lower() == wallet_address.lower():
                eth_balance += tx["value_eth"]
            elif tx["from"].lower() == wallet_address.lower():
                eth_balance -= tx["value_eth"]

    return round(eth_balance, 6)


def get_token_balances_by_date(wallet_address, date_str):
    print("Token balance by date function called")

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    timestamp = int(time.mktime(dt.timetuple()))

    url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "tokentx",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "1":
        print("Error fetching token data.")
        return {}

    token_balances = {}

    for tx in data["result"]:
        if int(tx["timeStamp"]) <= timestamp:
            symbol = tx["tokenSymbol"]
            decimals = int(tx["tokenDecimal"])
            value = int(tx["value"]) / (10 ** decimals)

            if symbol not in token_balances:
                token_balances[symbol] = 0

            if tx["to"].lower() == wallet_address.lower():
                token_balances[symbol] += value
            elif tx["from"].lower() == wallet_address.lower():
                token_balances[symbol] -= value

    filtered_balances = {
        token: round(amount, 6)
        for token, amount in token_balances.items()
        if abs(amount) >= 0.001
    }

    print("Filtered token balances:", filtered_balances)
    return filtered_balances
