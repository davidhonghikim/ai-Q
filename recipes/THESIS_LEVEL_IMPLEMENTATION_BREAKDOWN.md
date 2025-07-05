# AI-Q Project: Thesis-Level Implementation Breakdown

## 1. System Requirements
- **Operating System:** Windows 10/11, Ubuntu 22.04 LTS, or macOS 13+
- **Python:** 3.10.7 (use `pyenv` or official installer)
- **Node.js:** 18.16.0 (for frontend)
- **pip:** 22.3.1+
- **npm:** 9.5.1+
- **PostgreSQL:** 15.3 (for persistent storage)
- **Redis:** 7.0.11 (for caching, rate limiting)
- **Nginx:** 1.24.0 (for reverse proxy, SSL)
- **CUDA:** 11.8 (if using GPU acceleration)
- **Python Packages:** See requirements.txt (must include `fastapi==0.95.2`, `uvicorn==0.22.0`, `pydantic==1.10.7`, `sentence-transformers==2.2.2`, `numpy==1.24.3`, `scikit-learn==1.2.2`, `psycopg2-binary==2.9.6`, `redis==4.5.5`, `pytest==7.3.1`, `httpx==0.24.1`, `python-dotenv==1.0.0`, `PyYAML==6.0`)
- **Node Packages:** See package.json (must include `react@18.2.0`, `axios@1.4.0`, `material-ui@5.13.7`, `vite@4.3.9`)

## 2. Directory Structure (Canonical)
```
ai-Q/
  playlist/           # Modular agent tasks (YAML)
  src/
    api/             # FastAPI backend
    utils/           # Python utilities
    config/          # Config loaders/parsers
    validation/      # Pydantic schemas
    web/             # Frontend (React)
  config/
    system_config.yml
    feature_flags.yml
    env/
      environment-template.json
    validation/
      env-schema.json
  data/
    search_indexes/
    embeddings/
  logs/
  tests/
  requirements.txt
  package.json
  README.md
```

## 3. Database Schema (PostgreSQL)
- **Database Name:** aiq_db
- **User:** aiq_user
- **Password:** aiq_pass
- **Tables:**
  - `documents` (id SERIAL PRIMARY KEY, path TEXT, content TEXT, metadata JSONB, created_at TIMESTAMP, updated_at TIMESTAMP)
  - `embeddings` (id SERIAL PRIMARY KEY, document_id INTEGER REFERENCES documents(id), vector FLOAT8[], model TEXT, created_at TIMESTAMP)
  - `search_logs` (id SERIAL PRIMARY KEY, query TEXT, results JSONB, timestamp TIMESTAMP)
  - `feature_flags` (id SERIAL PRIMARY KEY, key TEXT UNIQUE, value BOOLEAN, description TEXT)
  - `users` (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT, created_at TIMESTAMP)

## 4. Redis Keys
- `cache:document:<id>`: Cached document content
- `rate_limit:<ip>`: API rate limiting
- `session:<user_id>`: User session data

## 5. Backend (FastAPI) API Endpoints
- `GET /api/status` → Returns system health, version, uptime
- `GET /api/services` → Returns list of running services
- `GET /api/metrics` → Returns CPU, RAM, disk, GPU metrics
- `POST /api/rag/query` → Body: `{query: str, search_type: str, top_k: int, alpha: float}`
- `GET /api/content/summary` → Returns file counts, types, last update
- `POST /api/content/refresh` → Triggers content re-index
- `GET /api/search` → Query params: `q`, `type`, `top_k`
- `POST /api/content/upload` → Multipart file upload
- `POST /api/feature_flags/toggle` → Body: `{key: str, value: bool}`
- `POST /api/auth/login` → Body: `{username: str, password: str}`
- `POST /api/auth/logout` → Body: `{token: str}`

## 6. Frontend (React) Pages/Components
- `/dashboard` → System status, metrics, feature toggles
- `/search` → Search bar, results, filters, highlights
- `/upload` → File upload, progress, validation
- `/logs` → Log viewer, search, filter
- `/login` → Auth form
- `/admin` → User management, feature flags

## 7. Feature Flags (config/feature_flags.yml)
```yaml
search_acceleration: true
parallel_processing: true
gpu_embeddings: true
real_time_indexing: true
advanced_analytics: false
```

## 8. System Config (config/system_config.yml)
```yaml
system:
  name: "AI-Q Knowledge Library System"
  version: "2.1.0"
  environment: "development"
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
content_service:
  scan_interval_hours: 1
  max_file_size_mb: 10
search_service:
  embedding_model: "all-MiniLM-L6-v2"
  batch_size: 64
hardware:
  gpu_memory_fraction: 0.8
  max_workers: 8
  enable_gpu_acceleration: true
storage:
  index_path: "data/search_indexes"
  data_path: "data"
  logs_path: "logs"
monitoring:
  metrics_interval_seconds: 30
  health_check_interval_seconds: 60
  log_level: "INFO"
```

## 9. Exact Steps for Each Major Task (Example: Feature Flag Loader)
1. **Install dependencies:**
   ```bash
   pip install PyYAML==6.0
   ```
2. **File:** `src/utils/feature_flags.py`
3. **Function:**
   ```python
   import yaml
   from pathlib import Path

   def load_feature_flags(path: str = "config/feature_flags.yml") -> dict:
       with open(path, "r") as f:
           return yaml.safe_load(f)
   ```
4. **Test:**
   ```python
   def test_load_feature_flags():
       flags = load_feature_flags()
       assert isinstance(flags, dict)
       assert "search_acceleration" in flags
   ```
5. **Document:** Add usage to `README.md` and docstring in the function.

## 10. Versioning & Conventions
- All code must use 4-space indentation, UTF-8 encoding, and Unix line endings.
- All config files must be YAML 1.2, validated with `yamllint`.
- All Python code must pass `flake8` and `black` formatting.
- All REST APIs must return JSON with keys: `status`, `data`, `timestamp`, `request_id`.
- All database migrations must be tracked with Alembic (Python) or Prisma (Node).

## 11. Testing & CI
- All modules must have unit tests in `tests/`.
- Use `pytest` for Python, `jest` for Node/React.
- CI pipeline must run on every push (GitHub Actions or GitLab CI).
- All tests must pass before merge.

## 12. Documentation
- All modules must have a `README.md` with usage, API, and config examples.
- All public APIs must be documented in OpenAPI/Swagger.
- All config files must have inline comments for every key.

---

**This file is the canonical, unambiguous implementation recipe for the AI-Q project. All agents must follow it exactly.** 