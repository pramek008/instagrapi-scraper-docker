import random
from .instagram_client import login_user
import logging

logger = logging.getLogger(__name__)

class InstagramClientPool:
    def __init__(self, accounts):
        self.clients = []
        for account in accounts:
            try:
                cl = login_user(account['username'], account['password'])
                self.clients.append(cl)
                logger.info(f"Successfully logged in with account: {account['username']}")
            except Exception as e:
                logger.warning(f"Failed to login with account {account['username']}: {e}")

    def get_client(self):
        if not self.clients:
            raise Exception("No working clients available")
        return random.choice(self.clients)

    def execute_method(self, method_name, *args, **kwargs):
        attempts = len(self.clients)
        for _ in range(attempts):
            client = self.get_client()
            try:
                method = getattr(client, method_name)
                return method(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Error with client: {e}. Trying another client.")
        raise Exception("All clients failed to execute the method")