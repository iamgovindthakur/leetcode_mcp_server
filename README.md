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

Integrating with MCP clients (e.g., Copilot)

You can expose the running server as an MCP HTTP server so editor tooling (that supports MCP) — including Copilot-style integrations — can call `GET /daily` to obtain the problem of the day.

1. Start the server locally (example):

```bash
# using the Makefile
make run

# or directly
uvicorn leetcode_mcp:app --host 127.0.0.1 --port 8080
```

2. Confirm the endpoint is reachable:

```bash
curl http://127.0.0.1:8080/daily
```

3. Configure your editor MCP file so MCP-aware clients can discover the server. Example `.vscode/mcp.json` (already included in this repo under `.vscode/mcp.json`):

```json
{
	"servers": {
		"leetcode-mcp": {
			"type": "http",
			"url": "http://127.0.0.1:8080/daily"
		}
	}
}
```

4. Reload your editor (or the MCP extension) so it picks up the new MCP server configuration. The exact steps depend on the MCP client or Copilot integration you're using — consult that extension's docs if discovery doesn't happen automatically.

Quick test: from within the editor's MCP client UI (or via any MCP-capable extension), request the `leetcode-mcp` server and verify you receive the JSON response.

Security & networking notes

- The above setup is intended for local development. If you expose the endpoint on a network interface, secure it appropriately (firewall, authentication) before allowing remote access.
- If running in a container, map ports (e.g., `-p 8080:8080`) and use the appropriate host URL in `.vscode/mcp.json`.
- If your MCP client is remote (e.g., a cloud-based dev environment), you may need to expose the service via an SSH tunnel or a secure ngrok-like tunnel and update the MCP URL accordingly.

GitHub Copilot (MCP) integration and sample usage

This project is primarily a demo of how a small MCP HTTP server can enhance editor assistant capabilities (e.g., GitHub Copilot or other MCP-capable assistants) by exposing structured data. The steps below show how to wire the running server into an MCP-enabled Copilot integration and a sample prompt + expected output you can use to verify behavior.

Steps to integrate with Copilot / MCP-capable editor

1. Start the MCP server locally:

```bash
# start the server
make run
```

2. Ensure MCP discovery config is present in your workspace (this repo includes `.vscode/mcp.json`):

```json
{
	"servers": {
		"leetcode-mcp": {
			"type": "http",
			"url": "http://127.0.0.1:8080/daily"
		}
	}
}
```

3. Reload your editor or the Copilot/MCP extension so it picks up the new server entry.

4. Open Copilot Chat (or your MCP client) and call the `leetcode-mcp` server (the exact UI varies by extension). If the server is reachable you should see the JSON response and the assistant can use it to enrich its output.

Sample usage (prompt + expected assistant output)

Use this example to validate end-to-end integration. It assumes Copilot (or your MCP client) can call the registered MCP server and incorporate the returned JSON into assistant responses.

Sample prompt (input you give to Copilot/MCP):

```
Fetch today's LeetCode problem from the registered MCP server `leetcode-mcp` and produce:

1) A one-paragraph plain-English summary of the problem.
2) A concise algorithmic approach and complexity (time/space).
3) A short, correct Python function implementing the solution.

Please reference the problem title and URL in your answer.
```

Sample expected output (what the assistant could return):

```
Title: Find Minimum Operations to Make All Elements Divisible by Three
URL: https://leetcode.com/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/

Summary:
You are given an integer array `nums`. In one operation you can add or subtract 1 from any element. The goal is to make every element divisible by 3 using the minimum number of operations.

Approach:
Compute the remainder of each element modulo 3. Elements with remainder 0 need no change. Each element with remainder 1 or 2 can be fixed with one operation (+1 or -1 respectively) to become divisible by 3. Therefore the minimum number of operations equals the count of elements whose `x % 3 != 0`.

Complexity:
Time: O(n) — single pass to count non-multiples of 3.
Space: O(1) — constant extra space.

Python implementation:
```python
from typing import List

def min_operations_make_div_by_three(nums: List[int]) -> int:
		return sum(1 for x in nums if x % 3 != 0)

# Example
print(min_operations_make_div_by_three([1,2,3,4]))  # 3
```

Notes:
- This sample output is intentionally concise so the assistant can use it as a snippet to augment completions or to generate a fuller explanation or code walkthrough on demand.
- The assistant should prefer linking to the canonical `URL` rather than reproducing long problem statements verbatim.
```

Troubleshooting

- If Copilot (or the MCP client) does not show the server, confirm the server is running and that `.vscode/mcp.json` points to the correct URL. Some MCP integrations require an editor restart.
- Check the extension or editor logs to see the raw HTTP response if the assistant output does not match expectations.
