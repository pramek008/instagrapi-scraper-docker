from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
import os
import json
import logging
import datetime

logger = logging.getLogger(__name__)

def login_user(username, password, proxy=None):
    cl = Client()
    if proxy:
        cl.set_proxy(proxy)

    cl.delay_range = [1, 3]

    session_file = f"sessions/instagram_session_{username}.json"

    login_via_session = False
    login_via_pw = False

    if os.path.exists(session_file):
        logger.info(f"Session file found for {username}. Attempting to load...")
        try:
            cl.load_settings(session_file)
            cl.login(username, password)

            try:
                cl.get_timeline_feed()
                login_via_session = True
                logger.info(f"Successfully logged in via session for {username}")
            except (LoginRequired, ClientError) as e:
                logger.info(f"Session is invalid for {username}: {e}. Will attempt login via username and password")
                cl.set_settings({})
                cl.login(username, password)
                login_via_pw = True
        except Exception as e:
            logger.info(f"Couldn't login user {username} using session information: {e}")

    if not login_via_session and not login_via_pw:
        try:
            logger.info(f"Attempting to login via username and password. username: {username}")
            if cl.login(username, password):
                login_via_pw = True
                logger.info(f"Successfully logged in via username and password for {username}")
        except Exception as e:
            logger.error(f"Couldn't login user {username} using username and password: {e}")

    if not login_via_pw and not login_via_session:
        raise Exception(f"Couldn't login user {username} with either password or session")

    # Save session for future use
    os.makedirs('sessions', exist_ok=True)
    cl.dump_settings(session_file)
    logger.info(f"Session saved to {session_file} for {username}")
    return cl


def get_liker_data(cl, url):
    logger.info(f"Fetching liker data for URL: {url}")
    media_pk = cl.media_pk_from_url(url)
    likers = cl.media_likers(media_pk)

    liker_data = []
    current_time = datetime.datetime.now().isoformat()  # Current date and time in ISO format
    for liker in likers:
        liker_info = {
            "id": liker.pk,
            "originalId": liker.pk,
            "username": liker.username,
            "name": liker.full_name,
            "created_at": current_time,  # Add current date and time
            "profile_pic_url": str(liker.profile_pic_url),
            "is_private": liker.is_private}
        liker_data.append(liker_info)

    logger.info(f"Fetched {len(liker_data)} likers")
    return liker_data

def get_post(cl, url):
    logger.info(f"Fetching post data for URL: {url}")
    media_pk = cl.media_pk_from_url(url)
    post = cl.media_info(media_pk)
    post_data = post.dict()

    # Extracting essential data
    extracted_data = {
        "post_id": post_data["id"],
        "taken_at": post_data["taken_at"].isoformat() if post_data["taken_at"] else None,
        "media_type": post_data["media_type"],
        "images": [
            {
                "width": img["width"],
                "height": img["height"],
                "url": img["url"]
            } for img in post_data.get("image_versions2", {}).get("candidates", [])
        ],
        "caption_text": post_data["caption"]["text"] if post_data.get("caption") else None,
        "location": {
            "name": post_data["location"]["name"] if post_data.get("location") else None,
            "lat": post_data["location"]["lat"] if post_data.get("location") else None,
            "lng": post_data["location"]["lng"] if post_data.get("location") else None
        },
        "user": {
            "username": post_data["user"]["username"],
            "full_name": post_data["user"]["full_name"],
            "profile_pic_url": str(post_data["user"]["profile_pic_url"]),
            "is_private": post_data["user"]["is_private"]
        },
        "comment_count": post_data["comment_count"],
        "like_count": post_data["like_count"],
        "has_liked": post_data["has_liked"],
        "usertags": [
            {
                "username": tag["user"]["username"],
                "full_name": tag["user"]["full_name"],
                "profile_pic_url": str(tag["user"]["profile_pic_url"]),
                "is_private": tag["user"]["is_private"],
                "x": tag["position"][0],
                "y": tag["position"][1]
            } for tag in post_data.get("usertags", [])
        ],
        "resources": [
            {
                "thumbnail_url": res["thumbnail_url"],
                "media_type": res["media_type"],
                "video_url": res["video_url"]
            } for res in post_data.get("resources", [])
        ]
    }

    logger.info("Post data fetched and processed successfully")
    return extracted_data


def get_comments(cl, url):
    logger.info(f"Fetching comments for URL: {url}")
    media_pk = cl.media_pk_from_url(url)
    comments = cl.media_comments(media_pk)
    
    comment_data = []
    for comment in comments:
        comment_info = {
            "id": comment.pk,
            "user_id": comment.user.pk,
            "username": comment.user.username,
            "text": comment.text,
            "profile_pic_url": str(comment.user.profile_pic_url),
            "name": comment.user.full_name,
            "is_private": comment.user.is_private,
            "created_at": comment.created_at_utc.isoformat()  # Convert datetime to ISO format
        }
        comment_data.append(comment_info)
    
    logger.info(f"Fetched {len(comment_data)} comments")
    return comment_data
