"""
Tell me the total mBTC on active laon and those stuck in balance.
"""
import argparse
import pandas as pd

from modules.Poloniex import Poloniex, PoloniexApiError
import modules.Configuration as Config

# Fetch configuration for the API key & secret inside
parser = argparse.ArgumentParser()
parser.add_argument("-cfg", "--config", help="Custom config file")
args = parser.parse_args()
if args.config:
    config_location = args.config
else:
    config_location = 'default.cfg'
Config.init(config_location)

api = Poloniex(Config.get('API', 'apikey', None), Config.get('API', 'secret', None))
active_loans = api.return_active_loans()
active_loans_sum = pd.DataFrame.from_records(active_loans['provided']).query('currency == "BTC"')['amount'].map(lambda x: x.replace('.','')).astype('int').sum()
idle_loan_balance = api.return_available_account_balances("lending")["lending"]
# idle_loan_balance = int(idle_loan_balance.replace('.', ''))
if idle_loan_balance == []:
    idle_loan_balance = 0
else:
    idle_loan_balance = int(idle_loan_balance["BTC"].replace('.', ''))

print("Idle: {0}".format(idle_loan_balance))
print("Active: {0}".format(active_loans_sum))
print("Total satoshi: {0}".format(idle_loan_balance + active_loans_sum))
