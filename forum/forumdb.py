# "Database code" for the DB Forum.

import datetime
import psycopg2

def get_posts():
    """Return all posts from the 'database', most recent first."""
    POSTS = psycopg2.connect("dbname=forum")
    c = POSTS.cursor()
    c.execute("DELETE FROM posts WHERE content = 'cheese'")
    POSTS.commit()
    c.execute("SELECT content, time FROM posts ORDER BY time DESC")
    posts = c.fetchall()
    POSTS.close()
    return posts

def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    POSTS = psycopg2.connect("dbname=forum")
    c = POSTS.cursor()
    c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
    POSTS.commit()
    POSTS.close()


