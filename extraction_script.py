# This file scrapes each subreddit for posts containing the specified keywords.
# It saves the data from each keyword group to a separate json file.

import praw
import os
import json
import time

reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent=""
)

subreddits = [
    "GDPR",
    "GoogleAnalytics",
    "GoogleTagManager",
    "webdev",
    "web_design"
]

keywords = {
    "consent": [
        "consent"
    ],

    "cookie": [
        "cookie",
        "cookies"
    ],

    "tag": [
        "GTM",
        "Google Tag Manager",
        "Tag Manager",
        "Tag",
        "Tags"
    ],

    "children": [
        "child",
        "children",
        "kid",
        "kids"
    ],

    "CMP": [
        "CMP",
        "Consent Management Platform",
        "Consent Management"
    ],

    "responsibility": [
        "responsible",
        "responsibility",
        "responsibilities"
    ]
}

all_keywords = [kw for sublist in keywords.values() for kw in sublist]

# Hard date of Jan 1, 2020 instead of exact 5 year from run time.
five_years_ago = int(time.mktime(time.strptime("2020-01-01", "%Y-%m-%d")))


posts_data = []
post_ids = set()  # Set to track post IDs and avoid duplicates

def search_posts(subreddit_name, keywords):
    subreddit = reddit.subreddit(subreddit_name)
    for keyword in keywords:
        cur_posts = subreddit.search(keyword, limit=1000)
        for post in cur_posts:
            # Checks for duplicates and if the post is a text post
            if post.id in post_ids or (not post.is_self):
                  continue
            # Skip posts older than 5 years
            if post.created_utc < five_years_ago:
                continue
            post_info = {
                "subreddit": subreddit_name,
                "created": post.created_utc,
                "title": post.title,
                "author": post.author.name if post.author else None,
                "id": post.id,
                "selftext": post.selftext,
                "score": post.score,
                "url": post.url,
                "num_comments": post.num_comments,
                "comments": []
            }
            post.comments.replace_more(limit=0)  # Replace "MoreComments" instances
            for comment in post.comments.list():
                comment_info = {
                    "body": comment.body,
                    "author": comment.author.name if comment.author else None,
                    "score": comment.score
                }
                post_info["comments"].append(comment_info)
            
            # Sort comments by score in descending order
            post_info["comments"].sort(key=lambda x: x["score"], reverse=True)

            post_ids.add(post.id)  # Add post ID to the set to avoid duplicates
            posts_data.append(post_info)
        
        print(f"{subreddit_name} - {keyword}")

    print(f"Scraped {subreddit_name}")

# Search for each keyword group in the subreddits
for subreddit_name in subreddits:
        search_posts(subreddit_name, all_keywords)

        os.makedirs(f"subreddits/{subreddit_name}", exist_ok=True)
        file_path = f"subreddits/{subreddit_name}/{subreddit_name}_posts_all.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(posts_data, f, ensure_ascii=False, indent=4)

        print(f"Data saved to {file_path}")
        posts_data.clear()  # Clear posts_data for the next subreddit
        post_ids.clear()    # Clear post_ids for the next subreddit