FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY . .

EXPOSE 8888

CMD ["/app/.venv/bin/jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]