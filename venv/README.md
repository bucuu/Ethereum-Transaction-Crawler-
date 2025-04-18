# 🕸 Ethereum Transaction Crawler —

Hi there! I'm Burcu Orhan, a senior-year Computer Engineering student, and this is my hands-on project built to interact with the Ethereum blockchain in the most practical way.  
If you’re curious about how to **analyze Ethereum transactions** for any wallet address, this project is for you. 🚀

---

## ✨ What This App Does

🔍 You input an Ethereum wallet address and a starting block.  
📊 The app fetches all ETH transactions related to that wallet (in & out).  
💰 You can also pick a specific date and check how much ETH and which tokens that wallet held at **00:00 UTC** on that day.  
📥 Bonus? You can **download all the transaction data as a CSV file.**

---

## 📁 Project Structure

```
├── app.py               # Flask application
├── crawler.py           # Handles API calls and data processing
├── templates/
│   └── index.html       # Web UI
├── .env                 # Your Etherscan API key (not committed)
├── requirements.txt     # Project dependencies
└── README.md            # You're reading it now ✨
```

---

## 🛠 Tech Stack

- Python 3.12
- Flask
- Flask-Session
- Etherscan API
- HTML/CSS (with Web3-style dark theme 😎)

---

## 🚀 Getting Started

Here’s how you can run this project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ethereum-crawler.git
cd ethereum-crawler
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Etherscan API Key

Create a `.env` file in the project root and add:

```
ETHERSCAN_API_KEY=your_api_key_here
```

> 🧠 You can get an API key for free at: https://etherscan.io/apis

---

## ▶️ Run the App

```bash
python app.py
```

Then go to your browser and open:

```
http://127.0.0.1:5000
```

✅ You’ll see a simple UI where you can input a wallet address, block, and optionally a date.

---

## 📦 CSV Export

Once the transaction list is shown, you’ll also see an **Export to CSV** button.  
Click it to download all transactions in a nice `.csv` file you can open in Excel or Google Sheets.

---

## 👩‍💻 Who Am I?

I'm a passionate Computer Engineering student with a love for clean UI, smart data, and real-world blockchain applications.  
This project was a part of my journey to learn more about Web3 and backend integration.

If you find it useful — star the repo 🌟, fork it, or reach out on [LinkedIn](https://linkedin.com/in/burcu-orhan)!

---

## 📜 License

This project is licensed under the MIT License — feel free to build on top of it!

---

> Thanks for reading all the way down here — you're awesome. 💙
