# AI-Q Universal Digital Twin Project Requirements

## 1. Vision
A universal, AI-powered personal digital twin/companion that can ingest, store, organize, and reason over any type of user data: text, images, video, audio, documents, and more. The AI should process, search, summarize, and interact with all modalities, acting as a true digital extension of the user.

---

## 2. Core Requirements

### Data Ingestion & Storage
- **Supported File Types:** Text, images, video, audio, PDFs, Office docs, code, etc.
- **Upload Methods:** Web UI, API, drag-and-drop, mobile, email, integrations.
- **Storage Backend:**
  - **Object Storage:** Minio (S3-compatible) for all user files.
  - **Database:** Postgres for metadata, user data, relationships.
  - **Vector DB:** Weaviate (default) for semantic search across all modalities.
  - **Knowledge Graph:** Neo4j for relationships, context, and reasoning.

### AI Processing & Understanding
- **Text:** Summarization, Q&A, semantic search, RAG, chat.
- **Images:** OCR, tagging, captioning, similarity search, face/object detection.
- **Video:** Scene detection, transcription, summarization, keyframe extraction.
- **Audio:** Speech-to-text, speaker ID, sentiment analysis.
- **Documents:** Parsing, summarization, semantic search.
- **Code:** Syntax highlighting, code search, explanation.

### User Experience
- **Personalization:** User profiles, preferences, memory, context.
- **Privacy & Security:** Encryption, access control, audit logs.
- **APIs:** REST/gRPC for all operations.
- **UI:** Modern, responsive dashboard for all data types and AI features.
- **Mobile:** Optional, for uploads and notifications.

---

## 3. Required Services & Integrations

| Service      | Status   | Purpose/Notes                                                                 |
|--------------|----------|-------------------------------------------------------------------------------|
| **Minio**    | Required | Universal object storage for all file types.                                  |
| **Weaviate** | Required | Multi-modal vector search, semantic search, RAG.                              |
| **Neo4j**    | Required | Knowledge graph, relationships, context.                                      |
| **Postgres** | Required | Metadata, user data, permissions.                                             |
| **Redis/RQ** | Required | Caching, background jobs.                                                     |
| **Ollama, Llama.cpp, VLLM** | Required | LLM inference for text, chat, summarization.                 |
| **ComfyUI, A1111** | Required | Image generation, GPU/CPU support, user-selectable.                    |
| **n8n**      | Required | Visual workflow automation, user extensibility.                               |
| **Jupyter**  | Required | Data science, user scripting, analytics.                                      |
| **LangChain, etc.** | Optional/Pluggable | Advanced agentic orchestration, RAG pipelines.             |

---

## 4. Implementation Notes & Agent Task Guidance

- **Device Detection:**
  - Agents must check for GPU/CPU and enable/disable image generation accordingly.
  - Provide clear error messages or fallbacks if device does not support certain features.

- **User Toggles & Preferences:**
  - All major features (image generation, automation, data science, orchestration) must be toggleable per user and globally.
  - UI should allow users to select which backend/service to use for each feature.

- **Plugin/Extension System:**
  - Design the system so new AI tools (e.g., LangChain, new image generators) can be added as plugins without core changes.
  - Document the plugin interface and provide example plugins.

- **Security & Isolation:**
  - Jupyter and n8n must be isolated per user/session for privacy and security.
  - All file access must be permission-checked and auditable.

- **Documentation:**
  - Every feature and integration must be documented with exact setup, config, and usage instructions.
  - Provide "How to add a new backend" guides for each pluggable component.

---

## 5. Scalability & Extensibility
- **Microservices:** Each AI pipeline (text, image, video, audio) can be a separate service.
- **Plugin system:** Allow new file types and AI models to be added as plugins.
- **Feature flags:** Toggle features (e.g., image generation, video summarization) per user or globally.

---

## 6. Example Agent Tasks (Granular)
- Implement S3 upload endpoint for Minio.
- Write a Python script to extract EXIF metadata from images and store in Postgres.
- Build a Weaviate schema for multi-modal objects (text, image, video, audio).
- Integrate CLIP model for image embedding and search.
- Write a FastAPI endpoint for uploading and transcribing audio using Whisper.
- Create a React component for video upload and preview.
- Implement a Neo4j relationship for "file is related to event X".
- Write a background job to generate video thumbnails using ffmpeg.
- Add a feature flag for enabling/disabling image generation.
- Write a test suite for file upload and retrieval.

---

**This document is the canonical requirements reference for the AI-Q universal digital twin project. All agents and contributors must follow it.** 