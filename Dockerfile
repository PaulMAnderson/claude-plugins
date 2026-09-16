FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY hypercube/ /app/hypercube/
EXPOSE 8765
CMD ["python", "-m", "hypercube", "--config", "/config/projects.json", "--host", "0.0.0.0", "--port", "8765"]
