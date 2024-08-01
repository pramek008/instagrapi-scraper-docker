from flask import jsonify, request
from app import app
from .account_manager import get_likers, get_post_data, get_post_comments
from .utils import log_response
import logging

logger = logging.getLogger(__name__)

@app.route("/")
@log_response
def index():
    logger.info("Index route accessed")
    return "Hello from Docker! Use /api/likers, /api/post, or /api/comments with ?url= parameter to get Instagram data."

@app.route("/api/likers")
@log_response
def api_likers():
    url = request.args.get('url')
    if not url:
        logger.error("URL parameter is missing in /api/likers request")
        return jsonify({"error": "URL parameter is missing"}), 400
    try:
        liker_data = get_likers(url)
        logger.info(f"Successfully retrieved liker data for URL: {url}")
        return jsonify({"likers": liker_data})
    except Exception as e:
        logger.error(f"Error in /api/likers: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/post")
@log_response
def api_post():
    url = request.args.get('url')
    if not url:
        logger.error("URL parameter is missing in /api/post request")
        return jsonify({"error": "URL parameter is missing"}), 400
    try:
        post_data = get_post_data(url)
        logger.info(f"Successfully retrieved post data for URL: {url}")
        return jsonify({"post": post_data})
    except Exception as e:
        logger.error(f"Error in /api/post: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/comments")
@log_response
def api_comments():
    url = request.args.get('url')
    if not url:
        logger.error("URL parameter is missing in /api/comments request")
        return jsonify({"error": "URL parameter is missing"}), 400
    try:
        comment_data = get_post_comments(url)
        logger.info(f"Successfully retrieved comment data for URL: {url}")
        return jsonify({"comments": comment_data})
    except Exception as e:
        logger.error(f"Error in /api/comments: {str(e)}")
        return jsonify({"error": str(e)}), 500