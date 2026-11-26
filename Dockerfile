FROM python:3.11-slim

WORKDIR /app

RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "-b", "0.0.0.0:5000", "app:app"]