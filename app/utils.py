from functools import wraps
from flask import request, Response, jsonify
import logging
import time
import random

logger = logging.getLogger(__name__)

def make_response(data=None, message='', success=True, status_code=200):
    response = {
        "status_code": status_code,
        "is_success": success,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def log_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, tuple):
            body, status_code = response
        elif isinstance(response, Response):
            body = response.get_json() if response.is_json else response.get_data(as_text=True)
            status_code = response.status_code
        else:
            body = response
            status_code = 200
        
        logger.info(f"Response for {request.path}: Status {status_code}, Body: {body}")
        return response
    return decorated_function

def random_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))