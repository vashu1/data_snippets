import os

BITCOIN_BLOCKCHAIN_PATH = os.path.expanduser('~/Downloads/BitcoinData/blocks/')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# see https://shtab.navalny.com/#donate
# 2016-12-09 03:44 skip files?  https://www.blockchain.com/btc/address/3QzYvaRFY6bakFBW4YBRrzmwzTnfZcaA6E?page=776
ADDRESS = '3QzYvaRFY6bakFBW4YBRrzmwzTnfZcaA6E'

PROCESSED_FILES_LIST = 'processed.txt'
TRANSACTIONS_JSON_LIST = 'transactions.txt'