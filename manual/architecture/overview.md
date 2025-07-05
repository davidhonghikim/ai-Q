# AI-Q System Architecture Overview

## Layers
- **Ingestion Layer:** Handles all user uploads (text, image, video, audio, docs, code) via UI, API, or integrations.
- **Storage Layer:** Minio (object storage), Postgres (metadata), Weaviate (vector search), Neo4j (knowledge graph), Redis (cache/queue).
- **Processing Layer:** AI/ML pipelines for text, image, video, audio; background jobs (RQ); workflow automation (n8n).
- **API Layer:** FastAPI/Fastify REST/gRPC endpoints for all operations.
- **Frontend Layer:** React UI, user dashboards, search, gallery, automation, data science (Jupyter).

## Data Flow
1. User uploads or creates data via UI/API.
2. Data is stored in Minio (raw), Postgres (metadata), and indexed in Weaviate/Neo4j.
3. AI/ML pipelines process and enrich data (embeddings, tags, summaries, relationships).
4. Users interact with data via search, dashboards, automations, and analytics.

## Core Components
- **Minio:** Universal file/object storage.
- **Weaviate:** Multi-modal vector search and semantic retrieval.
- **Neo4j:** Knowledge graph for relationships and context.
- **Postgres:** Metadata, user data, permissions.
- **Redis/RQ:** Caching, background jobs, queues.
- **Ollama, Llama.cpp, VLLM:** LLM inference for text, chat, summarization.
- **ComfyUI, A1111:** Image generation (GPU/CPU).
- **n8n:** Workflow automation.
- **Jupyter:** Data science and analytics.

---

**See subdirectories for detailed specs on each component and layer.** 