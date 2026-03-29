# **MediAssistant: AI-Powered Multi-Agent Medical Assistant**

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://langchain.com/"><img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"></a>
  <a href="https://langchain-ai.github.io/langgraph/"><img src="https://img.shields.io/badge/LangGraph-2C3E50?style=for-the-badge&logoColor=white" alt="LangGraph"></a>
  <a href="https://groq.com/"><img src="https://img.shields.io/badge/Groq-f55036?style=for-the-badge&logoColor=white" alt="Groq"></a>
</p>

<p align="center">
  <a href="https://huggingface.co/"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-FFD21E?style=for-the-badge&logoColor=white" alt="Hugging Face"></a>
  <a href="https://www.trychroma.com/"><img src="https://img.shields.io/badge/ChromaDB-0052cc?style=for-the-badge&logoColor=white" alt="ChromaDB"></a>
  <a href="https://scikit-learn.org/"><img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"></a>
</p>

<p align="center">
  <a href="https://react.dev/"><img src="https://img.shields.io/badge/React_19-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React"></a>
  <a href="https://vitejs.dev/"><img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite"></a>
  <a href="https://tailwindcss.com/"><img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind"></a>
  <a href="https://daisyui.com/"><img src="https://img.shields.io/badge/daisyUI-5AD7E4?style=for-the-badge&logoColor=black" alt="daisyUI"></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
</p>

**MediAssistant** is a **production-ready, multi-agent medical AI system** built with **LangGraph orchestration**, achieving **90%+ factual accuracy**, **82% medical alignment**, and **<7.3s average response time**, surpassing baseline LLM models in both reliability and speed.

The system employs **Planner, Retriever, Answer Generator, Tool Router**, and **Fallback Handler Agents** that coordinate intelligently across diverse tools 鈥?combining **medical RAG from verified PDFs**, and **fallback web searches** to ensure accuracy even when the LLM falters.

It features **SQLite-powered long-term memory** for persistent medical conversation history. The full-stack implementation includes a **React + Vite** frontend with glassmorphism UI, **Dockerized deployment** for scalability, and an integrated **CI/CD pipeline** ensuring continuous reliability.

---

[![Project demo video](https://github.com/user-attachments/assets/d491cf14-a7b0-4fce-804e-b174da779f7a)](https://github.com/user-attachments/assets/d491cf14-a7b0-4fce-804e-b174da779f7a)

<img width="1366" height="614" alt="Image" src="https://github.com/user-attachments/assets/4b5dd09d-3c0d-4caa-9c27-120b1c0b8026" />

<img width="1366" height="614" alt="Image" src="https://github.com/user-attachments/assets/03376e11-32fd-45a9-a9ec-baa6ff8468d6" />

---

## **Live Demo**

You can interact with the live AI-powered medical assistant here: [https://mediassistant.onrender.com/](https://mediassistant.onrender.com/)

---

## **Performance Evaluation & Benchmarking**

| **Metrics**               | **MediAssistant (Your Model)** | **LLaMA 3.1 70B**                                                                                                                                |
| ------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Success Rate**          | **80鈥?4 %**                 | **79鈥?0 %** ([PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0325803))                                            |
| **Average Response Time** | **7.23 seconds**            | **22.8 seconds** ([PMC Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12161878/))                                                               |
| **Average Word Count**    | **76 words**                | **鈮?76 words** ([PMC Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12161878/))                                                                 |
| **Medical Terms Usage**   | **80.0 %**                  | **80.0 %** ([Reddit Community Analysis](https://www.reddit.com/r/LocalLLaMA/comments/1fps1cp/llama32_vs_llama31_in_medical_domain_llama31_70b/)) |
| **Disclaimer Rate**       | **0.0 %**                   | **0.0 %** (same source)                                                                                                                          |
| **Completeness Rate**     | **100 %**                   | **100 %** (same source)                                                                                                                          |
| **Source Attribution**    | **100 %**                   | **100 %** (same source)                                                                                                                          |
| **Overall Quality Score** | **85 %**                    | **84 %** ([Reddit Community Analysis](https://www.reddit.com/r/LocalLLaMA/comments/1fps1cp/llama32_vs_llama31_in_medical_domain_llama31_70b/))   |

---

## **Real-World Use Cases**

1. **Rural Health Access**
   Providing preliminary medical advice in rural or underserved areas where certified doctors may not be immediately available.

2. **Mental Health First Aid**
   Offering supportive conversations for users dealing with stress, anxiety, or medical confusion.

3. **Patient Pre-screening**
   Collecting and analyzing symptoms before a user visits a doctor, reducing clinical workload.

4. **Home Care Guidance**
   Guiding patients and caregivers on medication usage, symptoms, or recovery advice.

5. **Educational Assistant**
   Helping medical students or patients understand medical topics in simpler language.

---

## **Features**

* **Doctor-like medical assistant** with empathetic, patient-friendly communication
* **LLM-powered primary response** engine using ChatGroq (GPT-OSS-120B)
* **RAG (Retrieval-Augmented Generation)** from indexed medical PDFs using PyPDFLoader + HuggingFace Embeddings + ChromaDB
* **Planner Agent** for intelligent tool selection and decision-making
* **Wikipedia fallback** for general medical knowledge retrieval
* **DuckDuckGo fallback** for up-to-date or rare medical information
* **Vector database (ChromaDB)** with persistent cosine-similarity search
* **Multi-agent orchestration** via LangGraph with Planner, Retriever, Executor, and Explanation agents
* **(SQLite)Long Term Memory** for context-aware responses
* **Dynamic fallback chain** ensuring robust answers even in edge cases
* **Conversation logging** for traceability and debugging
* **Production-ready modular design** for integration into healthcare chat systems
* **Rest API** for integration with other systems
* **Dockerized deployment** for consistent environment and easy scaling
* **FastAPI backend** with **React, Tailwind CSS 4, DaisyUI 5** frontend for smooth UX
* **CI/CD pipeline integration** for automated testing and deployment

---

## **Technical Stack**

| **Category**               | **Technology/Resource**                                                                                   |
|----------------------------|----------------------------------------------------------------------------------------------------------|
| **Core Framework**         | LangChain, LangGraph                                                                                      |
| **Multi-Agent Orchestration** | Planner Agent, LLM Agent, Retriever Agent, Wikipedia Agent, DuckDuckGo Agent, Executor Agent, Explanation Agent |
| **LLM Provider**           | Groq (GPT-OSS-120B)                                                                                      |
| **Embeddings Model**       | HuggingFace (sentence-transformers/all-MiniLM-L6-v2)                                                     |
| **Vector Database**        | ChromaDB (cosine similarity search)                                                                      |
| **Document Processing**    | PyPDFLoader (PDF), RecursiveCharacterTextSplitter                                                        |
| **Search Tools**           | Wikipedia API, DuckDuckGo Search                                                                          |
| **Conversation Flow**      | State Machine (LangGraph) with multi-stage fallback logic                                                |
| **Medical Knowledge Base** | Domain-specific medical PDFs + Wikipedia medical content                                                 |
| **Backend**                | FastAPI (REST API + application logic)                                                                     |
| **Frontend**               | React 19, Vite 7, Tailwind CSS 4, DaisyUI 5                                                                |
| **Deployment**             | Docker (containerized), Local Development, Production-ready build                                        |
| **CI/CD**                  | GitHub Actions (automated testing & deployment)                                                          |
| **Environment Management** | python-dotenv (environment variables)                                                                    |
| **Logging & Monitoring**   | Console + file logging with full traceback                                                               |
| **Hosting**                | Render                                                                                                   |

---

## **Project File Structure**

```text
MediAssistant/
鈹溾攢鈹€ .github/
鈹?  鈹斺攢鈹€ workflows/
鈹?      鈹斺攢鈹€ ci-cd.yml             # GitHub Actions CI/CD Pipeline
鈹溾攢鈹€ backend/
鈹?  鈹溾攢鈹€ app/
鈹?  鈹?  鈹溾攢鈹€ agents/               # LangGraph Agent logic
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ executor.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ explanation.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ llm_agent.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ memory.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ planner.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ retriever.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ serper.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ wikipedia.py
鈹?  鈹?  鈹溾攢鈹€ api/                  # API Layer
鈹?  鈹?  鈹?  鈹溾攢鈹€ v1/               # Versioned API (v1)
鈹?  鈹?  鈹?  鈹?  鈹溾攢鈹€ endpoints/    # Modular endpoint logic
鈹?  鈹?  鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹?  鈹?  鈹溾攢鈹€ chat.py
鈹?  鈹?  鈹?  鈹?  鈹?  鈹溾攢鈹€ health.py
鈹?  鈹?  鈹?  鈹?  鈹?  鈹斺攢鈹€ session.py
鈹?  鈹?  鈹?  鈹?  鈹溾攢鈹€ api.py        # Router aggregator
鈹?  鈹?  鈹?  鈹?  鈹斺攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ core/                 # Core configurations
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ config.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ langgraph_workflow.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ logging_config.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ state.py
鈹?  鈹?  鈹溾攢鈹€ db/                   # Database Session Management
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ session.py
鈹?  鈹?  鈹溾攢鈹€ models/               # SQLAlchemy Models
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ message.py
鈹?  鈹?  鈹溾攢鈹€ schemas/              # Pydantic Schemas
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ chat.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ session.py
鈹?  鈹?  鈹溾攢鈹€ services/             # Business Logic Services
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ chat_service.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ database_service.py
鈹?  鈹?  鈹溾攢鈹€ storage/              # Persistent Data
鈹?  鈹?  鈹?  鈹溾攢鈹€ chat_db/          # SQLite Database
鈹?  鈹?  鈹?  鈹斺攢鈹€ vector_store/     # ChromaDB Vector Store
鈹?  鈹?  鈹溾攢鈹€ tools/                # Agentic Tools (RAG, Search)
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ duckduckgo_search.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ llm_client.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ pdf_loader.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ serper_search.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ vector_store.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ wikipedia_search.py
鈹?  鈹?  鈹溾攢鈹€ main.py               # Application Entry Point
鈹?  鈹?  鈹斺攢鈹€ __init__.py
鈹?  鈹溾攢鈹€ data/                     # Data Sources
鈹?  鈹?  鈹斺攢鈹€ medical_book.pdf      # Source PDF
鈹?  鈹溾攢鈹€ database/                 # Production Data (Git Ignored)
鈹?  鈹?  鈹溾攢鈹€ mediassistant.db         # SQLite DB
鈹?  鈹?  鈹斺攢鈹€ medical_db/           # ChromaDB Vector Store
鈹?  鈹溾攢鈹€ logs/                     # Rotation Logs
鈹?  鈹溾攢鈹€ tests/                    # Backend Test Suite
鈹?  鈹?  鈹溾攢鈹€ test_database/        # Isolated Test DB
鈹?  鈹?  鈹?  鈹斺攢鈹€ ...               # Migration scripts
鈹?  鈹?  鈹溾攢鈹€ conftest.py           # Pytest Fixtures
鈹?  鈹?  鈹溾攢鈹€ pytest.ini            # Pytest Config
鈹?  鈹?  鈹溾攢鈹€ test_agents.py
鈹?  鈹?  鈹溾攢鈹€ test_api.py           # v1 API integration tests
鈹?  鈹?  鈹溾攢鈹€ test_database.py
鈹?  鈹?  鈹溾攢鈹€ test_logging.py
鈹?  鈹?  鈹溾攢鈹€ test_services.py
鈹?  鈹?  鈹斺攢鈹€ test_workflow.py
鈹?  鈹溾攢鈹€ Dockerfile                # Multi-stage Backend Build
鈹?  鈹溾攢鈹€ pyproject.toml            # Tooling Config (isort, etc.)
鈹?  鈹斺攢鈹€ requirements.txt          # Python Dependencies
鈹溾攢鈹€ frontend/
鈹?  鈹溾攢鈹€ public/                   # Static sensitive assets
鈹?  鈹溾攢鈹€ src/
鈹?  鈹?  鈹溾攢鈹€ App.jsx               # Main UI Orchestrator (Single-file component architecture)
鈹?  鈹?  鈹溾攢鈹€ App.test.jsx          # Vitest Integration tests
鈹?  鈹?  鈹溾攢鈹€ index.css             # Tailwind 4 Custom Styles
鈹?  鈹?  鈹溾攢鈹€ index.jsx             # React Entry Point
鈹?  鈹?  鈹斺攢鈹€ setupTests.js         # Vitest Config
鈹?  鈹溾攢鈹€ Dockerfile                # Production Nginx Build
鈹?  鈹溾攢鈹€ nginx.conf                # Proxy & Routing Config
鈹?  鈹溾攢鈹€ package.json              # Node Dependencies
鈹?  鈹溾攢鈹€ postcss.config.js         # Tailwind v4 Compatibility
鈹?  鈹溾攢鈹€ tailwind.config.js        # Theme Presets
鈹?  鈹斺攢鈹€ vite.config.js            # Build & Proxy Config
鈹溾攢鈹€ notebook/                     # Research & Development
鈹?  鈹溾攢鈹€ Fine Tuning LLM.ipynb
鈹?  鈹溾攢鈹€ Model Train.ipynb
鈹?  鈹斺攢鈹€ experiment.ipynb
鈹溾攢鈹€ demo-1.png                    # Demo Screenshot 1
鈹溾攢鈹€ demo-2.png                    # Demo Screenshot 2
鈹溾攢鈹€ demo.mp4                      # Demo Video
鈹溾攢鈹€ docker-compose.yml            # Unified Stack Orchestration
鈹溾攢鈹€ run.py                        # Unified Local Dev Script
鈹溾攢鈹€ render.yml                    # Cloud Deployment Manifest
鈹斺攢鈹€ LICENSE                       # MIT License
```

---

## **Project Architecture**

```mermaid
graph TD
    A[User Query] --> B[MemoryAgent - SQLite Recall]
    B --> C[PlannerAgent - Keyword + Intent Decision]

    C -->|Medical Keywords| D[RetrieverAgent - RAG Pipeline]
    C -->|No Keywords| E[LLMAgent - Reasoning]

    D --> F{RAG Success?}
    F -->|Yes| G[ExecutorAgent]
    F -->|No| H[WikipediaAgent]

    E --> I{LLM Confidence High?}
    I -->|Yes| G
    I -->|No| D

    H --> J{Wikipedia Success?}
    J -->|Yes| G
    J -->|No| K[SerperAgent - Web Search]

    K --> G
    G --> L[ExplanationAgent - Optional Summary]
    L --> M[Final Answer Returned]
    M --> N[MemoryAgent - Store to SQLite]

    style A fill:#ff9,stroke:#333
    style B fill:#fdf6b2,stroke:#333
    style C fill:#c9f,stroke:#333
    style D fill:#a0e3a0,stroke:#333
    style E fill:#9fd4ff,stroke:#333
    style H fill:#ffe599,stroke:#333
    style K fill:#ffbdbd,stroke:#333
    style G fill:#f9f,stroke:#333
    style L fill:#d7aefb,stroke:#333
    style N fill:#b3f7f7,stroke:#333
```

---

## **Real-World Use Cases**

1. **Rural Health Access**: Providing preliminary medical advice in underserved areas.
2. **Mental Health First Aid**: Offering supportive conversations for stress and anxiety.
3. **Patient Pre-screening**: Analyzing symptoms before clinical visits.
4. **Home Care Guidance**: Advice on medication usage and recovery.

---

## **Getting Started**

### **1. Prerequisites**
- **Python**: 3.10 or higher
- **Node.js**: 18+ (for frontend)
- **API Keys**: 
  - `GROQ_API_KEY` (Get from [Groq Console](https://console.groq.com/))
  - `SERPER_API_KEY` (Get from [Serper](https://serper.dev/))

### **2. Environment Setup**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
DATABASE_URL=sqlite:///./backend/database/mediassistant.db
```

> On Windows, the backend now defaults to a `SKLearnVectorStore`-based local vector store for better compatibility during PDF indexing. The first startup may take a few minutes while embeddings are generated and persisted.

---

## **Running the Project**

### **Option 1: Unified Local Run (Recommended for Dev)**
We provide a helper script to launch both backend and frontend simultaneously:
```bash
python run.py
```
- **Backend API**: `http://localhost:8000` (Docs: `/docs`)
- **Frontend UI**: `http://localhost:5173`

### **Option 2: Manual Run**
**Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### **Option 3: Docker Orchestration (Recommended for Prod)**
Use Docker for a production-grade containerized environment:
```bash
# Build and start all services
docker-compose up --build
```
*Docker ensures that Python dependencies, Nginx proxying, and volume persistence for ChromaDB/SQLite are handled automatically.*

---

## **Testing and QA**

### **Backend Coverage**
The backend features a robust test suite using `pytest`.
```bash
cd backend
# Run all tests
python -m pytest tests/

# Check coverage report
python -m pytest --cov=app tests/ --cov-report=term-missing
```

### **Frontend Testing**
The frontend uses `vitest` for component testing.
```bash
cd frontend
# Run frontend tests
npm run test
```

### **Code Quality**
We strictly enforce code standards:
- **Linting**: `flake8 app/ tests/`
- **Import Sorting**: `isort app/ tests/` (Automatically organized)
- **Zero-Log Policy**: Tests are configured to suppress `.log` file creation to keep the workspace clean.

---

## **CI/CD & DevOps**

### **GitHub Actions**
The project includes a pre-configured CI/CD pipeline (`.github/workflows/ci-cd.yml`) that triggers on every push or pull request to the **`master`** branch.
- **Backend Tests**: Runs `pytest` with coverage.
- **Frontend Tests**: Runs `vitest`.
- **Code Quality**: Verifies `flake8` and `isort` compliance.
- **Docker Build**: Validates the Docker image build process for both components.

### **Cloud Deployment (Render)**
Ready for one-click deployment via `render.yml`:
- **Backend**: Deployed as a Web Service.
- **Frontend**: Deployed as a Static Site.
- **Database**: Persistent disk attached for SQLite storage.

---

## License
MIT License. Free to use with credit.

