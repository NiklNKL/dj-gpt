from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 

Base = declarative_base() 

class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(String, primary_key=True)
    fbid = Column(String, nullable=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    profile_url = Column(String)
    profile_image_link = Column(String)
    follower_count = Column(Integer, nullable=True)
    followees_count = Column(Integer, nullable=True)
    post_count = Column(Integer, nullable=True)
    biography = Column(Text, nullable=True)
    biography_hashtags = Column(JSON, nullable=True)
    category_name = Column(String, nullable=True)
    business_category_name = Column(String, nullable=True)
    is_business_account = Column(Boolean, nullable=True)
    is_professional_account = Column(Boolean, nullable=True)
    is_verified = Column(Boolean, nullable=True)
    is_private = Column(Boolean, nullable=True)
    avg_engagement = Column(Float, nullable=True)
    posts = Column(JSON, nullable=True)
    highlight_count = Column(Integer, nullable=True)
    partner_id = Column(Integer, nullable=True)
    email_address = Column(String, nullable=True)
    business_address = Column(JSON, nullable=True)
    related_profiles = Column(JSON, nullable=True)
    external_url = Column(String, nullable=True)

    followers = relationship("Follower", back_populates="profile")
    comments = relationship("Comment", back_populates="profile")
    collaborations = relationship("Collaborator", back_populates="profile")

class Follower(Base):
    __tablename__ = 'followers'
    profile_id = Column(String, ForeignKey('profiles.id'), primary_key=True)
    username = Column(String, unique=True, index=True)
    comment_count = Column(Integer, default=0)

    profile = relationship("Profile", back_populates="followers")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(String, primary_key=True)
    shortcode = Column(String)
    user_posted = Column(String)
    date_local = Column(DateTime)
    url = Column(String)
    content_type = Column(String)
    caption = Column(Text, nullable=True)
    caption_hashtags = Column(JSON, nullable=True)
    caption_mentions = Column(JSON, nullable=True)
    tagged_users = Column(JSON, nullable=True)
    video_view_count = Column(Integer, nullable=True)
    video_play_count = Column(Integer, nullable=True)
    video_duration = Column(Float, nullable=True)
    location = Column(JSON, nullable=True)
    media_count = Column(Integer)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    content_type = Column(String)
    post_content = Column(JSON)
    photos = Column(JSON, nullable=True) 
    videos = Column(JSON, nullable=True)
    audio = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)
    alt_text = Column(Text, nullable=True)
    thumbnail = Column(String, nullable=True)
    product_type = Column(String, nullable=True)
    coauthor_producers = Column(JSON, nullable=True)
    engagement_score_view = Column(Float, nullable=True)
    is_collab = Column(Boolean)
    total_follower_reach = Column(Integer, default=0)

    collaborators = relationship("Collaborator", back_populates="post")
    comments = relationship("Comment", back_populates="post")
  
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(String, primary_key=True)
    post_id = Column(String, ForeignKey('posts.id'))
    profile_id = Column(String, ForeignKey('profiles.id'), nullable=True)
    user_name = Column(String, index=True)
    parent_comment_id = Column(BigInteger, nullable=True)
    post_url = Column(String)
    replies_count = Column(Integer)
    replied_content = Column(JSON, nullable=True)
    text = Column(Text)
    likes_count = Column(Integer)
    created_at = Column(DateTime)
    hashtags = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)
    creator_replied = Column(Boolean, default=False)

    post = relationship("Post", back_populates="comments")
    profile = relationship("Profile", back_populates="comments")

class Collaborator(Base):
    __tablename__ = 'collaborators'
    post_id = Column(String, ForeignKey('posts.id'), primary_key=True)
    profile_id = Column(String, ForeignKey('profiles.id'), primary_key=True)
    username = Column(String, index=True)

    post = relationship("Post", back_populates="collaborators")
    profile = relationship("Profile", back_populates="collaborations")