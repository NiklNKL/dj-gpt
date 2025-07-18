import json
import numpy as np
import re
from sqlalchemy import func
from sqlalchemy.orm import Session
from database_structure import Comment, Likes, Follower


def format_list(current_list: list) -> list:
    """
    Formatiert Hashtags, indem sie in Kleinbuchstaben umgewandelt werden.
    """
    try:
        if isinstance(current_list, np.ndarray):
            current_list = current_list.tolist()
            if current_list and isinstance(current_list[0], str) and current_list[0].startswith('['):
                current_list = current_list[0]
        if isinstance(current_list, str) and current_list.startswith('[') and current_list.endswith(']'):
            current_list = json.loads(current_list)
        if not isinstance(current_list, list):
            return None
        return current_list
    except Exception as e:
        print(f"Original value: {current_list}")
        print(f"Error formatting list: {e}")


def extract_mentions(text: str) -> list[str]:
    """
    Extrahiert @mentions aus einem Text.
    Es werden nur Wörter extrahiert, die mit @ anfangen
    und aus gültigen Instagram-Nutzernamen bestehen (Buchstaben, Zahlen, Punkte, Unterstriche).
    """
    if not isinstance(text, str):
        return []

    # Instagram erlaubt Benutzernamen mit Buchstaben, Zahlen, Punkt und Unterstrich (max. 30 Zeichen)
    pattern = r'@([A-Za-z0-9._]{1,30})\b'

    return re.findall(pattern, text)

def get_media_count(post_content: list) -> int:
    """
    Zählt die Anzahl der Medien in einem Post.
    """
    post_content = json.loads(post_content) if isinstance(post_content, str) else post_content
    if not isinstance(post_content, list):
        return 0
    return len(post_content)

def get_video_duration(videos: list) -> float:
    """
    Extrahiert die Dauer des Videos aus der Liste der Videos.
    """
    videos = json.loads(videos) if isinstance(videos, str) else videos
    if not isinstance(videos, list) or len(videos) == 0:
        return None
    video = videos[0]
    if isinstance(video, dict) and 'video_duration' in video:
        return video['video_duration']
    return None

def did_dorfterror_reply(values: list) -> bool:
    """
    Überprüft, ob der Creator in der Liste der Collaborators enthalten ist.
    """
    if not isinstance(values, list) or not values:
        return False
    for value in values:
        if isinstance(value, dict) and value.get('reply_user') == 'dorfterror':
            return True
    return False

def extract_hashtags(text: str) -> list[str]:
    """
    Extrahiert Hashtags aus einem Text.
    Es werden nur Wörter extrahiert, die mit # anfangen und aus gültigen Instagram-Hashtags bestehen.
    """
    if not isinstance(text, str):
        return []

    # Instagram erlaubt Hashtags mit Buchstaben, Zahlen und Unterstrichen (max. 30 Zeichen)
    pattern = r'#([A-Za-z0-9_]{1,30})\b'

    return re.findall(pattern, text)

def get_total_follower_reach(user_post: str, collaborators: list, profile_mapping: dict) -> int:
    """
    Berechnet die Gesamtanzahl der Follower für alle Collaborators.
    """
    if not isinstance(collaborators, list) or not collaborators:
        collaborators = []
    all_accounts = set([user_post.lower()] + collaborators)

    total_reach = 0
    for account in all_accounts:
        _, follower_count = profile_mapping.get(account, (None, 0))
        total_reach += follower_count
    return total_reach

def get_follower_comment_count(profile_id: str, session: Session) -> int:

    comment_counts = (
        session.query(Comment.profile_id, func.count(Comment.id))
        .filter(Comment.profile_id == profile_id)
        .group_by(Comment.profile_id)
        .count()
    )

    return comment_counts if comment_counts else 0

def get_follower_like_count(profile_id: str, session: Session) -> int:

    like_counts = (
        session.query(Likes.profile_id, func.count(Likes.profile_id))
        .filter(Likes.profile_id == profile_id)
        .group_by(Likes.profile_id)
        .count()
    )

    return like_counts if like_counts else 0

def get_post_follower_like_count(post_id: str, session: Session) -> int:

    follower_likes = (
        session.query(Likes.post_id, func.count(Likes.post_id))
        .filter(Likes.post_id == post_id)
        .filter(Likes.profile_id.in_(session.query(Follower.profile_id)))
        .group_by(Likes.post_id)
        .count()
    )

    return follower_likes if follower_likes else 0