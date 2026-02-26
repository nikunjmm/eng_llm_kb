# Engineering Agentic RAG Framework

An enterprise-grade, open-source Agentic RAG (Retrieval-Augmented Generation) framework designed to bridge C# desktop applications with powerful Python AI orchestration, specifically tailored for the manufacturing domain.

## Overview

This project provides an AI assistant capability for a C# desktop application (Equipment Design, Plant Layout, Process Control), helping engineering users by automatically extracting context and leveraging domain expertise to suggest and execute actions.

It utilizes a hybrid architecture:
1.  **Client Application**: A React UI embedded in a Microsoft Edge WebView2 control inside the existing C# Desktop host application.
2.  **Central API & Orchestrator**: A high-performance FastAPI Python server orchestrating a custom Agent Loop, managing context-isolated sub-agents, handling streaming responses, and coordinating Tool dispatching.
3.  **Domain Knowledge Base**: 
    *   **PostgreSQL + pgvector**: Unified database handling both relational data (like chat threads and memory) and highly scalable vector embeddings for semantic search.
    *   **Docling Pipeline**: Advanced multi-format document parser converting complex manufacturing PDFs, DOCX, XLSX (Excel) into Markdown, executing metadata extraction and deduplication.
    *   **MinIO**: Local S3-compatible object storage for extracted document images.

For deeper architectural details, see the `docs/architecture` directory.

## Core Capabilities
*   **Vector & Hybrid Search**: Combines semantic embeddings (via pgvector) with keyword search and reranking for superior context retrieval.
*   **Multi-Format Ingestion**: Capable of understanding complex tables and data natively extracted via Docling from PDFs, Excel, and Word files.
*   **Memory & Threads**: Long-term conversational memory persisted in PostgreSQL.
*   **Sub-agents**: Contextually isolated sub-agents managed by a primary deterministic loop.
*   **Human-in-the-Loop**: Safe execution in a C# environment where AI-proposed actions strictly require user review and approval before execution.
*   **Observability**: Integrated with Langfuse for robust prompt and cost tracking.

## Getting Started

To get the application scaffolding and databases running on your local machine, please follow the instructions in our [Developer Startup Guide](./docs/dev_startup.md).
