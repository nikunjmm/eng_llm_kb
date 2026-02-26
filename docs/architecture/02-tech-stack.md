# Tech Stack

The Agentic RAG framework is built upon the following technologies to ensure an enterprise-grade, open-source architecture that bridges C# desktop environments with powerful Python AI orchestration.

## 1. Client Application
The client acts as the user interface and context provider, residing within an existing C# desktop application.

*   **Desktop Host:** C# (.NET Framework or .NET Core)
*   **Embedded Browser:** Microsoft Edge WebView2 Control
*   **User Interface:** React (TypeScript)
    *   *Purpose:* Renders the chat interface, documents, and 'Approve Action' prompts. It allows sharing the identical UI codebase with the standalone Web version.
*   **Bridge Layer:** C# Class Library (DLL)
    *   *Purpose:* Orchestrates the communication between the Desktop Host, the WebView2 React UI, and the Python Central server. Handles Context extraction and native Action Execution.

## 2. Central API & Orchestrator
The central server handles natural language processing, RAG orchestration, and LLM communication.

*   **API Framework:** FastAPI (Python)
    *   *Purpose:* High-performance REST gateway and Streaming Interfaces (WebSockets/SSE) to receive context/prompts from the client and stream responses back in real-time.
*   **AI Orchestration Framework:** Raw SDK Calls + Pydantic (Python)
    *   *Purpose:* Manages primary loops, long-term memory threads, context-isolated sub-agents, RAG retrieval logic, Context analyzing, and Tool dispatching without the overhead of heavy frameworks like LangChain. Ensures full control over prompts and tool schemas.
*   **Large Language Model (MVP):** Google Gemini API
    *   *Purpose:* The reasoning engine using raw `google-generativeai` SDK. (Architecture ensures easy swapping to vLLM/Ollama for fully private local hosting in the future).
*   **Embedding Model:** `text-embedding-004` (Google's multimodal embedding model, or equivalent, swappable later)
*   **LLM Observability:** Langfuse
    *   *Purpose:* Fully open-source, self-hosted platform for tracing LLM executions, managing prompts, and monitoring agent iterations without cloud dependency.

## 3. Domain Knowledge Base (Storage & Ingestion)
Responsible for ingesting, parsing, and searching complex manufacturing domain knowledge.

*   **Primary Database / Vector Store:** PostgreSQL + pgvector
    *   *Purpose:* Open-source, highly capable relational database serving a dual purpose: storing structured chat threads/memory, and operating as a highly scalable vector search engine. Deployed locally via Docker. Stores chunked text embeddings and metadata for RAG.
*   **Search & Reranking:** Cross-Encoder / Ranking Model
    *   *Purpose:* Powers a two-stage retrieval pipeline combining hybrid search (vector + keyword in Postgres) followed by a reranking step to maximize context relevance.
*   **Document Parsing Engine:** Docling (Python)
    *   *Purpose:* Specialized parsing engine for multi-format documents (PDF, DOCX, XLSX/Excel, HTML, Markdown). Extract features, structures, metadata, and crucially, tabular data common in manufacturing SOPs natively, efficiently converting them to standard representation. Also incorporates deduplication logic hashing to prevent repeated records.
*   **Image Storage:** MinIO
    *   *Purpose:* A local, open-source S3-compatible object storage service. Used to store images extracted from PDFs by Docling, keeping the Vector DB lightweight.

## 4. Development & Deployment
*   **Containerization:** Docker & Docker Compose (for PostgreSQL, MinIO, Langfuse, and FastAPI)
*   **Version Control:** Git
