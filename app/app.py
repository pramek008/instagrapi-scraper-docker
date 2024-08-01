from flask import Flask
import logging
from .account_manager import initialize_accounts, get_next_account

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Inisialisasi akun Instagram
try:
    initialize_accounts()
    logger.info("Instagram accounts initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Instagram accounts: {e}")

# Import routes
from .routes import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)