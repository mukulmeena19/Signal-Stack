"""Public, no-auth source ingestion for a usable development MVP."""
import json
import re
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from xml.etree import ElementTree


def fetch_json(url: str) -> dict:
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "SignalStack-MVP"})
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def github_documents(topic: str, limit: int = 8) -> list[dict]:
    payload = fetch_json(f"https://api.github.com/search/repositories?q={quote_plus(topic)}&sort=updated&order=desc&per_page={limit}")
    documents = []
    for item in payload.get("items", []):
        description = item.get("description") or "Open-source repository related to this technical topic."
        documents.append({"id": f"github:{item['id']}", "title": item["full_name"], "source": "GitHub", "source_type": "github", "kind": "Try this", "url": item["html_url"], "tags": [topic, item.get("language") or "open source"], "content": f"{description} Primary language: {item.get('language') or 'unspecified'}. Stars: {item.get('stargazers_count', 0)}.", "action": "Inspect the README, recent commits, license, and open issues before adopting it.", "published_at": item.get("updated_at")})
    return documents


def arxiv_documents(topic: str, limit: int = 8) -> list[dict]:
    url = f"https://export.arxiv.org/api/query?search_query=all:{quote_plus(topic)}&start=0&max_results={limit}&sortBy=submittedDate&sortOrder=descending"
    request = Request(url, headers={"User-Agent": "SignalStack-MVP"})
    with urlopen(request, timeout=15) as response:
        root = ElementTree.fromstring(response.read())
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    documents = []
    for entry in root.findall("atom:entry", namespace):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=namespace)).split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=namespace)).split())
        url = entry.findtext("atom:id", default="", namespaces=namespace)
        identifier = re.sub(r"\W+", "-", url.rsplit("/", 1)[-1])
        documents.append({"id": f"arxiv:{identifier}", "title": title, "source": "arXiv", "source_type": "research", "kind": "Learn this", "url": url, "tags": [topic, "research"], "content": summary, "action": "Read the method and limitations, then look for implementation code before treating it as production-ready.", "published_at": entry.findtext("atom:published", default="", namespaces=namespace)})
    return documents
