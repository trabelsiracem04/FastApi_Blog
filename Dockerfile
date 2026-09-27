FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy \
	PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install locked production dependencies before copying application code.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY alembic.ini .
COPY alembic ./alembic
COPY routers ./routers
COPY static ./static
COPY templates ./templates
COPY auth.py config.py database.py email_utils.py image_utils.py main.py models.py schemas.py ./

RUN mkdir -p media/profile_pics

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
