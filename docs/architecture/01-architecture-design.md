# Agentic RAG Framework Architecture

An enterprise-grade, open-source Agentic RAG framework designed for a C# desktop application in the manufacturing domain. 

## Understanding Summary
- **What is being built**: An AI assistant for a C# desktop application in the manufacturing domain (Equipment Design, Plant Layout, Process Control).
- **Why it exists**: To help users perform tasks based on their requests by automatically extracting context from their C# app and leveraging domain expertise to suggest and execute actions.
- **Who it is for**: Enterprise users (10-20 per plant) using the C# desktop application.
- **Key constraints**: Must use open-source or private capabilities. Architecture must support local deployment, though the MVP will use public LLM APIs (Gemini/OpenAI) due to current hardware limitations. Low traffic expectations.
- **Explicit non-goals**: Not a fully autonomous agent (requires human-in-the-loop approval). Not building the underlying LLM itself.

## Architecture Components

### 1. Client Application (Desktop & Web)
- **Host**: Existing C# Desktop application.
- **UI**: A React application rendered inside a Microsoft Edge WebView2 control. This handles the chat interface, displaying documents, and showing the "Approve/Reject Action" prompts. This React app can also be served independently as a Web App.
- **Bridge (C# DLL)**: Sits between the C# App and WebView2.
  - **Context Aggregator**: Maintains a rolling buffer (last N events/lines) of user activity in the C# App.
  - **Event Interceptor**: Receives user prompts from the React UI, bundles them with the buffered C# context, and calls the Central Python API.
  - **Action Executor**: Receives JSON action commands from the Python Server (upon user approval) and executes native C# functions (e.g., `SelectEquipment(id="PUMP-101")`).

### 2. Central API & Orchestrator
- **Gateway**: FastAPI (Python) exposing REST endpoints (e.g., `/api/v1/chat`) and Streaming Interfaces (via Server-Sent Events or WebSockets) for real-time conversational experiences.
- **Orchestrator**: Custom Agent Loop (Raw SDKs + Pydantic).
  - **Context Analyzer**: Evaluates the incoming C# context.
  - **Retrieval Engine (RAG)**: Queries the Vector DB using hybrid search (combining vector similarity with keyword search) and applies a reranking stage for optimal context retrieval.
  - **Agent Loop & Sub-agents**: Uses the LLM to reason about the prompt, context, and RAG data. The main agent can dispatch tasks to specialized, context-isolated sub-agents.
  - **Chat & Memory Manager**: Persists conversation threads, user interactions, and memory state to a relational database.
- **Tool Definitions**: Registered tools mapped to C# DLL functions. The LLM outputs structured JSON commands (e.g., `{"action": "SetPressure", "parameters": {"value": 50}}`).

### 3. Domain Knowledge Base (Manufacturing Data)
- **Database & Vector Store**: PostgreSQL + pgvector (Open Source, local Docker deployment). Handles both relational data (chat history, user threads) and vector embeddings, simplifying the tech stack.
- **Ingestion Pipeline**: 
  - **Document Parsing**: Uses `Docling` to extract text and complex tables from multi-format manufacturing documents (PDF, DOCX, XLSX/Excel, HTML). Converts them to Markdown format.
  - **Image Extraction**: Images are extracted from documents, saved to **MinIO** (a local S3-compatible object store), and referenced via standard markdown image links pointing to the local MinIO bucket.
  - **Embedding & Chunking**: Markdown text is chunked, structured metadata is extracted, and the text is embedded using an Embedding API (e.g., `text-embedding-3-small` for MVP, later local HuggingFace) before insertion into PostgreSQL.
  - **Record Management**: Ingestion logic leverages document hashes to automatically handle deduplication.
  - **Search Configuration**: Chunks are stored alongside rich metadata (e.g., equipment ID, document type) to feed hybrid search and reranking workloads.

## Decision Log

1. **Execution Environment**
   - **Decision**: Centralized Python API Server with a C# Context Extraction DLL. MVP uses Public LLMs, but architecture allows swapping to local LLMs (e.g., Ollama) later.
   - **Alternatives Considered**: Fully local (Desktop) execution, or C# Native Semantic Kernel server.
   - **Why**: Centralized server makes updates easier and handles the heavy RAG/Vector DB workload better than individual desktops. Python provides a vastly superior ecosystem for RAG, Document Parsing (especially manufacturing tables), and Agent loops compared to C#.

2. **Context Extraction**
   - **Decision**: User-Triggered with Buffered Context (A + C). The user triggers the agent, but the C# DLL automatically sends the last N lines/events of context to the server.
   - **Alternatives Considered**: Purely on-demand (no history) or continuous automated polling.
   - **Why**: Balances performance (no constant API polling) with high contextual awareness for the LLM.

3. **Action Execution**
   - **Decision**: Human-in-the-loop approval of Agent proposed actions (with an option to auto-approve specific tasks).
   - **Alternatives Considered**: Read-only conversational UI, or fully autonomous execution.
   - **Why**: Safety is paramount in manufacturing applications. Users must review and approve actions (e.g., changing equipment parameters) before the C# DLL executes them.

4. **UI Implementation**
   - **Decision**: React App hosted in WebView2 within the C# Desktop app.
   - **Alternatives Considered**: Native C# WPF/WinForms chat UI.
   - **Why**: Allows sharing the exact same UI codebase between the Desktop App and the separate Web App.

5. **Document Ingestion**
   - **Decision**: Use Docling to convert PDFs to Markdown. Extract images to MinIO and reference them in Markdown. Store Markdown chunks in Qdrant.
   - **Alternatives Considered**: Standard PyMuPDF text extraction or storing base64 images directly in the Vector DB.
   - **Why**: Manufacturing documents rely heavily on tables and diagrams. MD format preserves table structure well for LLMs. MinIO provides a robust local object storage solution for the extracted images, keeping the Vector DB lightweight.

6. **Advanced Retrieval (Knowledge Graphs / Fine-Tuning)**
   - **Decision**: Deferred for MVP. We will leverage the C# Application's existing logical hierarchy.
   - **Alternatives Considered**: Building a standalone Knowledge Graph (GraphRAG), Ontology mapping, or Fine-Tuning a local LLM on manufacturing terms from day one.
   - **Why**: 
     - **Knowledge Graphs:** Since the C# application naturally maintains equipment hierarchy (e.g. Pump belongs to System A), we can pass this hierarchy in the *Context Extraction* phase. The Python Orchestrator can simply use this context to perform strict Metadata filtering in the Vector DB (e.g., `WHERE hierarchy_path STARTS_WITH 'SystemA/Pump'`). This simulates GraphRAG without the overhead of maintaining a separate graph database system.
     - **Fine-Tuning:** It is expensive, hard to update when documents change, and generally worse for *factual retrieval* than RAG. We will stick to prompt engineering and pure RAG.

## Implementation Handoff Readiness
The architecture is fully defined and validated against the non-functional requirements. The project can now proceed to implementation, starting with:
1. Setting up the C# WebView2 + React UI scaffolding.
2. Building the FastAPI Python Server skeleton with streaming endpoints.
3. Establishing the PostgreSQL/pgvector database for memory and vector storage.
4. Implementing the multi-format Docling parsing + MinIO ingestion pipeline.
