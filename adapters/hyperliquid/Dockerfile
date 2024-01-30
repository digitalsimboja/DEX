FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/app:${PYTHONPATH}"

CMD ["python", "jobs/hyperliquid/hyperliquid_job.py"]