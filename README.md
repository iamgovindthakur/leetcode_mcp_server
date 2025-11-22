# LeetCode MCP Example

Minimal example of an MCP-style HTTP server exposing `GET /daily` that returns the LeetCode "Problem of the Day" (title, url, snippet). This project is a small demo useful for editor integrations or as a template for feature experiments.

Features
- FastAPI application in the `leetcode_mcp` package
- Fetch strategy: GraphQL first, then homepage parsing fallback
- Configuration via environment variables (`LC_USER_AGENT`, `LC_TIMEOUT`)
- Tests using `pytest` and `respx` (HTTP mocking)

Prerequisites
- Python 3.10+ (3.12 used in CI)
- Docker (optional, if you want to run the container)

Quickstart (local)

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

You can also use the `Makefile`:

```bash
make install   # creates .venv and installs deps
make run       # starts uvicorn on 127.0.0.1:8080
```

Health check

```bash
curl http://127.0.0.1:8080/health
```

Get the daily problem

```bash
curl http://127.0.0.1:8080/daily
```

Run with Docker

```bash
docker build -t leetcode-mcp:latest .
docker run --rm -p 8080:8080 leetcode-mcp:latest
```

Testing

Run tests from the repository root (ensure `PYTHONPATH=.` or activate the venv):

```bash
source .venv/bin/activate
PYTHONPATH=. pytest -q
```

Configuration

Set environment variables to adjust behavior:
- `LC_USER_AGENT` — override the default User-Agent string used for requests to LeetCode.
- `LC_TIMEOUT` — request timeout in seconds (defaults to `10.0`).

Notes & production considerations
- This is a demonstration project. For production readiness consider:
  - Structured logging and metrics
  - Retries/backoff and circuit-breakers for network calls
  - More robust HTML parsing (e.g., BeautifulSoup) and stricter schema validation
  - CI and container image scanning
  - Adding a license and CONTRIBUTING guide

If you want the repository to provide a named CLI (console script), I can add a `pyproject.toml` and a small packaging configuration.
