# LeetCode MCP Example

This repository contains a minimal example of an MCP-style HTTP server that exposes a `GET /daily` endpoint returning the LeetCode "Problem of the Day" (title, url, snippet). It is designed as a small example integrating with editor tooling (e.g., GitHub Copilot or an MCP client).

Features
- FastAPI application in the `leetcode_mcp` package
- Robust fetch strategy: GraphQL endpoint first, then homepage parsing fallback
- Configuration via environment variables (`LC_USER_AGENT`, `LC_TIMEOUT`)
- Tests using `pytest` and `respx` for HTTP mocking

Quickstart

1. Create and activate a virtual environment (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the server locally (package entrypoint):

```bash
uvicorn leetcode_mcp:app --host 127.0.0.1 --port 8080
```

3. Health check:

```bash
curl http://127.0.0.1:8080/health
```

4. Get the daily problem:

```bash
curl http://127.0.0.1:8080/daily
```

Compatibility shim

The repository previously included a small compatibility shim module `leetcode_daily.py` that exposed the same `app` object as `leetcode_mcp`. That shim has been removed — use `leetcode_mcp:app` as shown above.

Testing

```bash
pytest -q
```

Environment

Set `LC_USER_AGENT` if you need to override the default user agent string.

Notes
- This is a small demonstration project. For production use consider adding:
  - Structured logging and metrics
  - Retries/backoff and circuit-breakers for network calls
  - More robust HTML parsing (e.g., BeautifulSoup) and schema validation
  - CI pipeline and containerization
