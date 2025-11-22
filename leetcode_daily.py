"""Entrypoint for running the MCP example server.

This file keeps a minimal shim so you can still run:

  uvicorn leetcode_daily:app --host 127.0.0.1 --port 8080

The actual application implementation lives in the `leetcode_mcp` package.
"""

from leetcode_mcp import app

__all__ = ["app"]

if __name__ == "__main__":
    # Allow running the module directly for quick development.
    import uvicorn

    uvicorn.run("leetcode_daily:app", host="127.0.0.1", port=8080, log_level="info")
