FROM python:3.12-slim

WORKDIR /app

# install system deps (if any) and python deps
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy source
COPY . /app

EXPOSE 8080

CMD ["uvicorn", "leetcode_daily:app", "--host", "0.0.0.0", "--port", "8080"]
