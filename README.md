# DocSense AI

DocSense AI is an advanced agentic system powered by LlamaIndex and Google Gemini (gemini-2.0-flash). It processes, indexes, and queries complex PDF documents using Retrieval-Augmented Generation (RAG) while persisting session records dynamically via local tool integration.

## System Architecture

```mermaid
graph TD
    User([User CLI]) -->|Queries| Agent[ReAct Agent]
    Agent -->|1. Route Request| Router{Tool Router}
    Router -->|If PDF Query| RAG[LlamaIndex Query Engine]
    Router -->|If Note Saving| Notes[Note Saver Tool]
    RAG -->|Retrieve Context| Storage[(Vector Store Index)]
    Storage -.->|Token Chunking| PDF[Sri_Lanka.pdf]
    RAG -->|Generate Answer| LLM[Google Gemini 2.0]
    Notes -->|Write Notes| File[data/notes.txt]
    LLM -->|Answer| Agent
    Agent -->|Final Output| User

    %% Styles with high contrast dark text for dark-mode safety
    style User fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#0a2540
    style Agent fill:#ede7f6,stroke:#4a148c,stroke-width:2px,color:#0a2540
    style Router fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#0a2540
    style RAG fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px,color:#0a2540
    style Notes fill:#fbe9e7,stroke:#bf360c,stroke-width:2px,color:#0a2540
    style Storage fill:#e8eaf6,stroke:#1a237e,stroke-width:2px,color:#0a2540
    style PDF fill:#fce4ec,stroke:#880e4f,stroke-width:2px,color:#0a2540
    style LLM fill:#e0f2f1,stroke:#004d40,stroke-width:2px,color:#0a2540
    style File fill:#efebe9,stroke:#3e2723,stroke-width:2px,color:#0a2540
```

## Core Features
* **Intelligent ReAct Agent**: Autonomously determines whether to consult knowledge bases or execute procedural tools (e.g. saving summaries).
* **API Rate-Limit Optimizer**: Special token-splitting batch loader with custom delay buffers to respect free-tier API quotas.
* **Persistent Vector Indexing**: Caches document vectors locally to guarantee instantaneous search on subsequent runs.
