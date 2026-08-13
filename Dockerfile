FROM python:3.10-slim
WORKDIR /app

# Copy runtime requirements. For reproducible builds prefer adding a pinned
# `requirements.lock` (with hashes) or a `constraints.txt` file and the build
# will prefer those automatically.
COPY requirements.txt ./
COPY constraints.txt ./
COPY requirements.lock ./

# Use lockfile if available, otherwise use constraints, otherwise install runtime deps.
RUN if [ -f requirements.lock ]; then \
			pip install --no-cache-dir --require-hashes -r requirements.lock; \
		elif [ -f constraints.txt ]; then \
			pip install --no-cache-dir -r requirements.txt --constraint constraints.txt; \
		else \
			pip install --no-cache-dir -r requirements.txt; \
		fi

COPY . .

# Production entry. For local development you may want `--reload` and a mounted volume.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]