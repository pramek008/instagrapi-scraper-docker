import os
import csv
import random
from .instagram_client import login_user, get_liker_data, get_post, get_comments
import logging
import threading

logger = logging.getLogger(__name__)

accounts = []
account_lock = threading.Lock()
current_account_index = 0

def load_accounts_from_csv(file_path):
    global accounts
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Lewati baris header
            for row in reader:
                if len(row) >= 2:
                    accounts.append({
                        'username': row[0],
                        'password': row[1]
                    })
                else:
                    logger.warning(f"Ignoring invalid row: {row}")
        logger.info(f"Loaded {len(accounts)} accounts from CSV")
    except Exception as e:
        logger.error(f"Error loading accounts from CSV: {e}")

def initialize_accounts():
    global accounts
    if os.path.exists('accounts.csv'):
        load_accounts_from_csv('accounts.csv')
    else:
        raise Exception("accounts.csv file not found")

    if not accounts:
        raise Exception("No accounts found in CSV file")
    
    for account in accounts[:]:  # Iterate over a copy of the list
        try:
            cl = login_user(account['username'], account['password'])
            account['client'] = cl
            logger.info(f"Successfully logged in with account: {account['username']}")
        except Exception as e:
            logger.warning(f"Failed to login with account {account['username']}: {e}")
            accounts.remove(account)

def get_next_account():
    global current_account_index
    with account_lock:
        if not accounts:
            raise Exception("No working accounts available")
        account = accounts[current_account_index]
        current_account_index = (current_account_index + 1) % len(accounts)
    return account['client']

# Fungsi-fungsi baru yang menggunakan client
def get_likers(url):
    client = get_next_account()
    return get_liker_data(client, url)

def get_post_data(url):
    client = get_next_account()
    return get_post(client, url)

def get_post_comments(url):
    client = get_next_account()
    return get_comments(client, url)