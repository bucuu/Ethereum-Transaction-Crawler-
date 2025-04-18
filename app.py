from flask import Flask, render_template, request, send_file, session
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
from io import StringIO
from flask_session import Session
from crawler import (
    get_transactions,
    get_balance_by_date,
    get_token_balances_by_date
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'  # store session on disk
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wallet_address = request.form.get('wallet')
        start_block = request.form.get('block')
        balance_date = request.form.get('date')

        transactions = []
        eth_balance = None
        token_balances = {}
        balance_datetime_str = None

        # Get ETH transactions
        if wallet_address and start_block:
            transactions = get_transactions(wallet_address, int(start_block))
            session['transactions'] = transactions  # Store in session for export

        # Get ETH and token balances at a specific date
        if wallet_address and balance_date:
            eth_balance = get_balance_by_date(wallet_address, balance_date)
            token_balances = get_token_balances_by_date(wallet_address, balance_date)

            dt = datetime.strptime(balance_date, "%Y-%m-%d")
            balance_datetime_str = dt.strftime("%B %d, %Y at %H:%M UTC")

        return render_template(
            'index.html',
            transactions=transactions,
            wallet=wallet_address,
            balance=eth_balance,
            balance_date=balance_date,
            balance_datetime=balance_datetime_str,
            token_balances=token_balances
        )

    return render_template('index.html')


@app.route('/export_csv', methods=['GET'])
def export_csv():
    tx_list = session.get('transactions', [])

    if not tx_list:
        return "No transaction data to export", 400

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Hash', 'From', 'To', 'Value (ETH)', 'Timestamp'])

    for tx in tx_list:
        writer.writerow([
            tx.get('hash'),
            tx.get('from'),
            tx.get('to'),
            tx.get('value_eth'),
            tx.get('timestamp')
        ])

    output = StringIO(si.getvalue())
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='transactions.csv'
    )


if __name__ == '__main__':
    app.run(debug=True)
