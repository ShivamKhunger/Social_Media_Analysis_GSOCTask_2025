# -*- coding: utf-8 -*-
# !pip install pandas nltk emoji
# !pip install praw
# !pip install python-dotenv

import pandas as pd
import emoji
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
import os 
import dotenv
import time
import praw

nltk.download("stopwords")
nltk.download('punkt')
nltk.download('punkt_tab')

def text_preprocessing(text):
    text = emoji.replace_emoji(text, replace="")
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    words = word_tokenize(text.lower())
    words = [word for word in words if word not in stopwords.words("english")]
    return " ".join(words)

KEYWORDS = ["depressed","feeling down","hopeless","worthless","empty","no way out","exhausted","broken inside","overthinking","social anxiety","lonely","suicidal","ending it all"]
SUBREDDITS = ["depression", "suicidewatch", "stopdrinking", "addiction", "mentalhealth"]

from google.colab import drive
drive.mount('/content/drive', force_remount=True)                   #Client Keys hiding for security
old_path = "/content/drive/My Drive/Colab_keys/.env.txt"
new_path = "/content/drive/My Drive/Colab_keys/.env"
env_path = "/content/drive/My Drive/Colab_keys/.env"
if os.path.exists(old_path):
    os.rename(old_path, new_path)
    print("Renamed .env.txt to .env")
else:
    print(".env.txt file not found!")
dotenv.load_dotenv(env_path)

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

print("Reddit API authenticated successfully!")

posts = []
for subreddit in SUBREDDITS:
    subreddit_obj = reddit.subreddit(subreddit)

    for post in subreddit_obj.hot(limit=250):
        if any(keyword in post.title.lower() or keyword in post.selftext.lower() for keyword in KEYWORDS):
            posts.append({
                "post_id": post.id,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(post.created_utc)),
                "title": text_preprocessing(post.title),
                "content": text_preprocessing(post.selftext),
                "upvotes": post.score,
                "comments": post.num_comments
            })

df = pd.DataFrame(posts)
df.to_csv("reddit_mentalhealth_data.csv", index=False)

