import pytest
import respx
import httpx

from leetcode_mcp.app import parse_daily_from_home, fetch_daily_via_graphql
from leetcode_mcp import app as _app  # ensure package import works


def test_parse_daily_from_home_simple():
    html = '<a href="/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/">link</a>'
    parsed = parse_daily_from_home(html)
    assert parsed["title"] == "Find Minimum Operations To Make All Elements Divisible By Three"
    assert parsed["url"].startswith("https://leetcode.com/problems/")


@pytest.mark.asyncio
async def test_fetch_daily_via_graphql_returns_question():
    api = respx.mock
    api.start()
    try:
        graphql_url = "https://leetcode.com/graphql"
        resp = {
            "data": {
                "activeDailyCodingChallengeQuestion": {
                    "question": {
                        "title": "Test Title",
                        "titleSlug": "test-title",
                        "content": "<p>content</p>",
                    }
                }
            }
        }
        api.post(graphql_url).mock(return_value=httpx.Response(200, json=resp))

        async with httpx.AsyncClient() as client:
            out = await fetch_daily_via_graphql(client)
            assert out["title"] == "Test Title"
            assert "test-title" in out["url"]
            assert out["snippet"] is not None
    finally:
        api.stop()
