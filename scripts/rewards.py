import re
import json
import requests
import argparse

def get_rewards(url, peer_id):
    response = requests.get(url)
    data = response.json()
    for item in data:
        if item['peerId'] == peer_id:
            return float(item['reward'])
    return 0 

def get_existing_rewards(peer_id):
    return get_rewards("https://quilibrium.com/rewards/existing.json", peer_id)

def get_pre_rewards(peer_id):
    return get_rewards("https://quilibrium.com/rewards/pre-1.4.18.json", peer_id)

def get_post_rewards(peer_id):
    return get_rewards("https://quilibrium.com/rewards/post-1.4.18.json", peer_id)

def get_disqualified(peer_id):
    response = requests.get("https://quilibrium.com/rewards/disqualified.json")
    data = response.json()
    for item in data:
        if item['peerId'] == peer_id:
            return item['criteria']
    return None
    

def main(peer_id):
    result = {}
    
    disqualified = get_disqualified(peer_id)
    if (disqualified is not None):
         result = f"{peer_id};0;0;0;0;true;{disqualified}"
    else:
        existing = get_existing_rewards(peer_id)
        pre_rewards = get_pre_rewards(peer_id)
        post_rewards = get_post_rewards(peer_id)
        total = pre_rewards + post_rewards
        result = f"{peer_id};{str(existing).replace('.',',')};{str(pre_rewards).replace('.',',')};{str(post_rewards).replace('.',',')};{str(total).replace('.',',')};false;"

    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quilibrium rewards")
    parser.add_argument("peer_id", type=str, help="The peer ID to check rewards for")
    args = parser.parse_args()

    main(args.peer_id)

