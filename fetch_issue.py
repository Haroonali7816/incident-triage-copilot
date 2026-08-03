# first-> ingest incident data from Github Issues.

#Source-> tiangolo/fastapi
# Cap-> 300 issues and Pull requests(PR) filtered out.

import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

OWNER = "tiangolo"
REPO = "fastapi"
MAX_ISSUES = 300
PER_PAGE = 100 #Github's max page size.

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def is_actual_issue(item:dict)->bool:
    #We check if the item is an actual issue and not a pull request.
    return "pull_request" not in item


def build_headers()-> dict:
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables.")
    return{
        "Authorization" : f"token {GITHUB_TOKEN}",
        "Accept" : "application/vnd.github+json",
        "X-GitHub_Api_Version" : "2022-11-28"
    }

def check_rate_limit(response: requests.Response)-> None:
    remaining = response.headers.get("X-RateLimit-Remaining")
    if remaining is not None and int(remaining) < 5:
        reset_ts = int(response.headers.get("X-RateLimit-Reset",0))
        wait = max(reset_ts - time.time(),0)
        print(f"Rate limit is nearly exhausted. Sleeping {wait:.0f}s...")
        time.sleep(wait + 1)

def fetch_all_issues()-> list[dict]:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

    params = {
        "state" : "all",
        "per_page" : PER_PAGE,
        "sort" : "created",
        "direction": "desc" #this is the most recent first.
    }
    headers = build_headers()

    collected: list[dict] = []
    request_params = params

    while True:
        response = requests.get(url,headers=headers,params=request_params)

        if response.status_code == 403:
            check_rate_limit(response)
            continue # retry same url after sleeping

        response.raise_for_status() # raises for any other non-200

        page_items = response.json()
        real_issues = [item for item in page_items if is_actual_issue(item)]
        collected.extend(real_issues)

        print(f"Fetched page: {len(page_items)} items," 
              f"{len(real_issues)} real issues, "
              f"{len(collected)} total so far")

        if len(collected) >= MAX_ISSUES:
            break

        next_url = response.links.get("next", {}).get("url")
        if not next_url:
            break #no more pages to fetch

        url = next_url
        request_params = None

        time.sleep(0.5)

    return collected[:MAX_ISSUES]

def save_issues(issues: list[dict], path: str = "data/raw_issues.json") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(issues,f, indent=2, ensure_ascii=False)
    print(f"Saved {len(issues)} issues to {path}")

if __name__ == "__main__":
    issues = fetch_all_issues()
    print(f"\nFetched {len(issues)} real issues (PR's filtered out)")
    save_issues(issues)