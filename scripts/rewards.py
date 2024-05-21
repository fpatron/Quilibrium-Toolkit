import re
import json
import requests
import argparse

def get_main_js():
    res = requests.get("https://quilibrium.com/?/rewards")
    pattern = r"main\.([^.]+)\.js"
    match = re.search(pattern, res.content.decode('utf-8'))
    if match is None:
        return None
    return f"https://quilibrium.com/static/js/main.{match[1]}.js"

def get_rewards():
    js = get_main_js()
    print(f"wget {js}")
    if js is None:
        return []

    res = requests.get(js)
    regex = r"\[\s*\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*peerId(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}\s*(?:,\s*\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*peerId(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\})*\s*\]"
    match = re.search(regex, res.text)
    print(f"match: {not match is None}")
    if match is None:
        return []

    data = match.group(0)
    data = data.replace('!0', '"0"').replace('!1', '"1"')
    code = re.sub(r'(?<={|,)(\w+):([^,}]+)', r'"\1":\2', data)

    return eval(code)

def main(peer):
    rewards = {}
    total_rewards = 0
    data = get_rewards()

    for item in data:
        rewards[item["peerId"]] = float(item["reward"])
        total_rewards += float(item["reward"])
    
    my_rewards = rewards.get(peer, 0)

    result = {
        'total_users': len(rewards),
        'total_rewards': total_rewards,
        'my_rewards': my_rewards
    }

    print(json.dumps(result))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quilibrium rewards")
    parser.add_argument("peer_id", type=str, help="The peer ID to check rewards for")
    args = parser.parse_args()

    main(args.peer_id)

