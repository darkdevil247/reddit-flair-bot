import praw
import time

def authenticate():
    """Instantiates a Reddit instance using credentials from praw.ini."""
    # PRAW automatically looks for the 'DEFAULT' section in praw.ini 
    # for the required client_id, client_secret, user_agent, etc.
    print("Authenticating PRAW...")
    try:
        reddit = praw.Reddit('DEFAULT')
        # Check if the instance is read-only (it should not be for posting)
        if reddit.read_only:
            print("Authentication Failed: PRAW is read-only. Check praw.ini settings.")
            return None
        print(f"Successfully authenticated as u/{reddit.user.me().name}")
        return reddit
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return None

def run_bot(reddit_instance):
    """The main function to perform the bot's task."""
    if not reddit_instance:
        return

    # 1. Target a subreddit (use a non-critical one like 'test' first)
    subreddit_name = 'test'
    subreddit = reddit_instance.subreddit(subreddit_name)
    
    # 2. Get the top submission from the subreddit
    print(f"Fetching top post from r/{subreddit_name}...")
    try:
        # Get the first submission in the 'hot' listing
        submission = next(subreddit.hot(limit=1))
    except StopIteration:
        print(f"No posts found in r/{subreddit_name}.")
        return

    # 3. Post a comment to the submission
    comment_text = "Hello World! This is an automated comment from my new PRAW bot. \n\n*Beep Boop*"
    
    print(f"Attempting to comment on post: '{submission.title}'")
    try:
        submission.reply(comment_text)
        print("✅ Comment posted successfully!")
    except Exception as e:
        # This will catch rate limits, forbidden access, etc.
        print(f"❌ Failed to post comment. Error: {e}")

if __name__ == "__main__":
    reddit = authenticate()
    if reddit:
        run_bot(reddit)

