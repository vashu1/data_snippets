from blockchain_parser.blockchain import Blockchain
import os
import multiprocessing
import json

from constants import *

CPU_CORES = int(multiprocessing.cpu_count() / 2 + 1) # for overnight processing set something like multiprocessing.cpu_count()

def satoshi2btc(value):
    # A satoshi is the smallest unit of a bitcoin, equivalent to 100 millionth of a bitcoin.
    return value / 1e8

def output_record(output):
    assert len(output.addresses) < 2
    if len(output.addresses) == 0:
        return {}
    return {
        'address': output.addresses[0].address,
        'btc': satoshi2btc(output.value),
        'type': output.type,
    }

def transaction_record(header, transaction):
    return {
        'timestamp': header.timestamp.strftime(DATETIME_FORMAT),
        'hash': transaction.hash,
        'outputs': [output_record(output) for output in transaction.outputs]
    }

def transaction_with_address(filename, address):
    blockchain = Blockchain(filename)
    total_transaction_count = 0
    transactions = []
    for block in blockchain.get_unordered_blocks(): # blockchain.get_ordered_blocks(path, end=1000))
        for transaction in block.transactions:
            total_transaction_count += 1
            if address in [addr.address for output in transaction.outputs for addr in output.addresses]:
                transaction = transaction_record(block.header, transaction)
                transactions.append(transaction)
    return filename, total_transaction_count, transactions

# wrap for get_transactions(), can't use lambda since pool requires pickable callable
def get_transactions(filename):
    return transaction_with_address(filename, ADDRESS)


if __name__ == '__main__':
    # get list of files
    files = os.listdir(BITCOIN_BLOCKCHAIN_PATH)
    files = filter(lambda fn: fn.startswith('blk') and fn.endswith('.dat'), files)
    files = list(sorted(files))[:-1]  # skip last partial file
    files = [os.path.join(BITCOIN_BLOCKCHAIN_PATH, fn) for fn in files]
    files = list(reversed(files))
    print(f'=== {len(files)} files found')
    # substract processed
    if (os.path.isfile(PROCESSED_FILES_LIST)):
        with open(PROCESSED_FILES_LIST, 'rt') as f:
            processed = [os.path.join(BITCOIN_BLOCKCHAIN_PATH, line.split(' ')[0]) for line in f.readlines()]
            print(f'=== processed count {len(processed)}')
            print(processed[0], files[0])
            files = list(set(files) - set(processed))

    print(f'=== {len(files)} files to process...')
    #for fn in reversed(files):
    with multiprocessing.Pool(processes=CPU_CORES) as pool:
        for result in pool.imap_unordered(get_transactions, files):
            filename, total_transaction_count, transactions = result
            filename = filename.replace(BITCOIN_BLOCKCHAIN_PATH, '')
            print(f'===  {filename=} {total_transaction_count=} found={len(transactions)}')
            with open(PROCESSED_FILES_LIST, 'at') as f:
                f.write(f'{filename} {total_transaction_count} {len(transactions)}\n')
            for transaction in transactions:
                transaction['filename'] = filename
                print(str(transaction))
                with open(TRANSACTIONS_JSON_LIST, 'at') as f:
                    f.write(f'{json.dumps(transaction)}\n')