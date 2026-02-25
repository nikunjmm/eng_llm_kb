# Project Folder Structure

The project is segregated into distinct directories representing the separate architectural concerns (Client, Server, and Knowledge Base/Ingestion).

```text
eng_llm_kb/
│
├── docs/                               # Project Documentation
│   └── architecture/
│       ├── 01-architecture-design.md   # Final Brainstorming & Architecture Decisions
│       ├── 02-tech-stack.md            # Approved Technology Stack
│       └── 03-folder-structure.md      # This file
│
├── src/                                # Source Code Root
│   │
│   ├── client/                         # Client-Side Application Code
│   │   ├── csharp-bridge/              # C# DLL for Context Extraction & Action Execution
│   │       ├── ContextExtractors/      # Extractors for fetching local desktop data
│   │       ├── ActionHandlers/         # Handlers for executing Agent commands
│   │       └── WebView2Host/           # Bridge controllers for communicating with UI
│   │   │
│   │   └── react-ui/                   # UI Application (Runs in WebView2 & Browser)
│   │       ├── src/
│   │           ├── components/         # Chat UI, Approval Cards, Status Indicators
│   │           ├── hooks/              # WebView2 / REST API communication hooks
│   │           └── store/              # State management
│   │
│   ├── server/                         # Central Python Orchestration Server
│   │   ├── api/                        # FastAPI routers and endpoints
│   │   ├── agents/                     # LangChain/LlamaIndex agent definitions and prompts
│   │   ├── tools/                      # Tool definitions mapped to C# DLL actions
│   │   └── rag/                        # Retrieval logic (querying Qdrant)
│   │
│   └── ingestion/                      # Offline Document Processing Pipeline
│       ├── parsers/                    # Docling integration for PDF to Markdown
│       ├── chunking/                   # Text chunking and embedding logic
│       └── storage/                    # Interfaces for Qdrant and MinIO
│
├── data/                               # Local storage for Raw and Processed data (Ignored in Git)
│   ├── raw_documents/                  # Source PDFs and SOPs for ingestion
│   └── processed/                      # Intermediate structures (e.g. extracted images before MinIO)
│
├── docker/                             # Infrastructure definitions
│   ├── minio/                          # Docker configuration for MinIO
│   ├── qdrant/                         # Docker configuration for Qdrant setup
│   └── docker-compose.yml              # Combined infrastructure runner
│
└── .gitignore                          # Standard git ignores (excluding /data, /docker volumes)
```
