from jinja2 import Environment, FileSystemLoader
from pathlib import Path

import requests

import os

GITHUB_TOKEN = os.environ["PAGES_COMMIT_TOKEN"]
TEMPLATES_DIR = Path(__file__).parent / "templates"
SITE_DIR = Path(__file__).parent / "docs"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

response = requests.get(
    "https://api.github.com/repos/adenwuts/adenwuts.github.io/commits?sha=pages",
    headers=headers,
)

recent_commits = [
    (commit["commit"]["message"], commit["commit"]["author"]["date"])
    for commit in response.json()[:10]
]

environment = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
template = environment.get_template("index.html")
output = template.render(recent_commits=recent_commits)

with open(SITE_DIR / "index.html", "w") as f:
    f.write(output)
