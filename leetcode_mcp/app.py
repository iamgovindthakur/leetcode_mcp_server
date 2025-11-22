"""FastAPI app and helper functions for fetching LeetCode daily problem."""
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import re
import logging

from .config import settings

logger = logging.getLogger("leetcode_mcp")


class DailyResponse(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    snippet: Optional[str] = None
    error: Optional[str] = None


app = FastAPI(title="LeetCode Daily Fetcher (mcp)")


async def fetch_daily_via_graphql(client: httpx.AsyncClient) -> Dict[str, Any]:
    """GraphQL fetch: returns title/slug/content if available."""
    query = (
        "query{activeDailyCodingChallengeQuestion{question{title titleSlug content}}}"
    )
    r = await client.post("https://leetcode.com/graphql", json={"query": query})
    r.raise_for_status()
    payload = r.json()
    q = payload.get("data", {}).get("activeDailyCodingChallengeQuestion", {})
    question = q.get("question") or {}
    title = question.get("title")
    slug = question.get("titleSlug")
    content = question.get("content")
    url = f"https://leetcode.com/problems/{slug}/" if slug else None
    snippet = None
    if content:
        snippet = re.sub(r"<[^>]+>", "", content)[:400]
    return {"title": title, "url": url, "snippet": snippet}


def parse_daily_from_home(html: str) -> Dict[str, Any]:
    """Heuristic: find first /problems/<slug> href and return a readable title."""
    m = re.search(r'href=["\'](/problems/([^"\'/]+)[^"\']*)["\']', html)
    if not m:
        return {"error": "no /problems/ link found"}
    href = m.group(1)
    slug = m.group(2)
    url = f"https://leetcode.com{href}"
    title = slug.replace("-", " ").title()
    return {"title": title, "url": url, "snippet": None}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/daily")
async def daily_post(payload: Dict[str, Any] = Body(...)):
    if isinstance(payload, dict) and payload.get("method") == "initialize":
        id_ = payload.get("id")
        result = {"capabilities": {}}
        if id_ is not None:
            return {"jsonrpc": "2.0", "id": id_, "result": result}
        return {"result": result}
    return await get_daily()


@app.get("/daily", response_model=DailyResponse)
async def get_daily(force_graphql_fail: bool = False):
    """Fetch daily; set `?force_graphql_fail=true` to skip GraphQL and exercise the HTML fallback."""
    headers = {"User-Agent": settings.user_agent, "Referer": "https://leetcode.com/"}
    async with httpx.AsyncClient(timeout=settings.timeout, headers=headers, follow_redirects=True) as client:
        if not force_graphql_fail:
            try:
                res = await fetch_daily_via_graphql(client)
                if res.get("title") and res.get("url"):
                    return res
            except Exception as exc:  # pragma: no cover - network dependent
                logger.debug("GraphQL fetch failed: %s", exc)

        try:
            r = await client.get("https://leetcode.com/")
            r.raise_for_status()
            html = r.text
            parsed = parse_daily_from_home(html)
            if parsed.get("title") and parsed.get("url"):
                return parsed
        except Exception as e:  # pragma: no cover - network dependent
            logger.debug("Homepage fetch failed: %s", e)
            return {"error": f"fetch error: {e}"}

    return {"error": "could not locate daily problem"}
