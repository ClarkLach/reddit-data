import json

subreddits = [
    "GDPR",
    "GoogleAnalytics",
    "GoogleTagManager",
    "webdev",
    "web_design"
]

for subreddit_name in subreddits:
    file_path = f"subreddits/{subreddit_name}/{subreddit_name}_posts_all.json"
    post_ids = set()
    with open(file_path, "r", encoding="utf-8") as f:
        posts_data = json.load(f)
    
    for post in posts_data:
        if post['id'] in post_ids:
            print(f"Duplicate found in {subreddit_name}: {post['id']}")
        else:
            post_ids.add(post['id'])