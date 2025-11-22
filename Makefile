PYTHON=python3

.PHONY: install run test docker-build docker-run

install:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	uvicorn leetcode_mcp:app --host 127.0.0.1 --port 8080

test:
	PYTHONPATH=. pytest -q

docker-build:
	docker build -t leetcode-mcp:latest .

docker-run:
	docker run --rm -p 8080:8080 leetcode-mcp:latest
