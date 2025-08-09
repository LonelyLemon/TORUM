# Parent image
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# Set the working directory in the container
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Pre-install dependencies using lock + pyproject only
RUN --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    UV_NO_CACHE=1 uv sync --locked --no-install-project --no-dev

# Copy the app code into the container
COPY . /app

# Install project
RUN UV_NO_CACHE=1 uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "cd /app && alembic upgrade head && uvicorn backend.src.main:app --host 0.0.0.0 --port 8000"]
