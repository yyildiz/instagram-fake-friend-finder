import helpers
import time
import json
from random import randint
import os
from dotenv import load_dotenv
load_dotenv()

api = helpers.get_instagram_api()
all_unfollowers = set()
USER_ID = os.getenv('USERID')
PREV_FOLLOWERS_FILE = 'prev_followers.json'
def get_current_followers():
    rank_token = api.generate_uuid()
    results = api.user_followers(USER_ID, rank_token)
    next_max_id = results.get('next_max_id')
    users = {}
    all_users = results.get('users', [])
    while next_max_id:
        for user in all_users:
            users[user.get('username')] = True
        rand = randint(2, 5)
        print('waiting for ' + str(rand) + ' seconds')
        time.sleep(rand)
        results = api.user_followers(USER_ID, rank_token, max_id=next_max_id)
        all_users = results.get('users', [])
        next_max_id = results.get('next_max_id')
    return users

def get_all_unfollowers(prevFollowers, nextFollowers):
    for follower in prevFollowers:
        if follower not in nextFollowers:
            all_unfollowers.add(follower)
    return all_unfollowers
def get_prev_followers():
    with open(PREV_FOLLOWERS_FILE) as f:
        return json.loads(f.read())

def update_prev_followers(prev):
    with open(PREV_FOLLOWERS_FILE, 'w') as f:
        json.dump(prev, f)

if __name__ == "__main__":
    current_followers = get_current_followers()
    update_prev_followers(current_followers)
    while(True):
        next_followers = get_current_followers()
        prev_followers = get_prev_followers()
        all_unfollowers = get_all_unfollowers(prev_followers, next_followers)
        update_prev_followers(next_followers)
        print(all_unfollowers)
        # not advised to be used like this
        # rather than a sleep, you should put this on a server and assign a cron job
        print('sleeping for 24 hours')
        time.sleep(24 * 60 * 60)

    
