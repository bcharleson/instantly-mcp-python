FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir -e .

# Default port
ENV PORT=8000
ENV HOST=0.0.0.0

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run HTTP server
CMD ["python", "-m", "instantly_mcp.server", "--transport", "http"]

