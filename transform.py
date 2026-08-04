

from datetime import datetime


def parse_github_datetime(value: str| None) -> datetime | None:
    if value is None:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")

def github_issue_to_incident_dict(raw:dict) -> dict:
    return {
        "github_id" : raw["id"],
        "github_number" : raw["number"],
        "html_url" : raw["html_url"],
        "title" : raw["title"],
        "body" : raw.get("body"), # not all issues have a body
        "state" : raw["state"],
        "labels" : [label["name"] for label in raw.get("labels",[])],
        "created_at" : parse_github_datetime(raw.get("created_at")),
        "closed_at" : parse_github_datetime(raw.get("closed_at")),
        "severity" : None,
        "category" : None,
        "summary" : None
    }