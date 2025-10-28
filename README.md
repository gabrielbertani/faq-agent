# 🤖 FAQ Agent — GitHub Repo QA Assistant

> An agent that indexes a GitHub repository, performs semantic search, and answers questions with source references — with a Streamlit UI, unit tests, and CI.

[![CI](https://img.shields.io/github/actions/workflow/status/gabrielbertani/faq-agent/ci.yml?branch=develop)](https://github.com/gabrielbertani/faq-agent/actions)
![Python](https://img.shields.io/badge/python-3.11-blue)

---

## 1) Project Title & Description
**FAQ Agent** — Ask questions about a GitHub repository (e.g., `DataTalksClub/faq`) and get cite-able answers via a simple web UI.

---

## 2) Overview
- **Problem:** Docs/FAQs spread across files and issues are hard to navigate quickly.
- **Solution:** Lightweight indexing of a GitHub repo + an agent that answers questions from the index, exposed via a Streamlit chat UI.
- **Why it’s useful:**
  - Fast setup (no heavy infra)
  - CI with tests and coverage
  - Simple, responsive UI
- **Screenshots/GIFs (add later):**
  ```md
  ![demo](assets/streamlit_demo.gif)
  ```

---

## 3) Installation

### Requirements
- **Python 3.11**
- **pip + venv** (or Poetry)
- API key for your LLM provider (e.g., `GROQ_API_KEY`) if applicable

### Setup (pip + venv)
```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# App dependencies
pip install -r requirements.txt

# Dev dependencies (tests, coverage, lint)
pip install -r requirements-dev.txt
```

### Environment variables
Create a `.env` or export in your shell:
```bash
export GROQ_API_KEY="YOUR_KEY_HERE"   # if your agent uses GROQ or similar
```

---

## 4) Usage

### Run the UI (Streamlit)
**Recommended (module mode):**
```bash
streamlit run -m app.app
```

**Alternative (file mode; code includes a safe import fallback):**
```bash
streamlit run app/app.py
```

### Change the target repository
Edit `app/app.py` → `init_agent()` and set:
```python
repo_owner = "DataTalksClub"
repo_name  = "faq"
```
Adjust the `filter_doc` function to restrict which files are indexed.

---

## 5) Features
- 🔎 GitHub repository indexing (with simple path/filename filtering)
- 🧠 Question-answering agent over the index
- 🌐 Streamlit web UI with streaming responses
- ✅ Unit tests (pytest) + Coverage (fail-under configured)
- ⚙️ CI with GitHub Actions (Ubuntu, Python 3.11)
- 🧱 Modular code structure under `app/`

**Roadmap (suggested):**
- [ ] Source citations with deep links to repo lines
- [ ] Multiple collections/indexes
- [ ] Persistent chat history
- [ ] CLI mode

---

## 6) Contributing
- Fork and branch from **`develop`**.
- Follow code style (e.g., `ruff`).
- Open PRs with clear descriptions and tests for changed logic.
- Optional: add `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.

---

## 7) Tests

### Run tests locally
```bash
pytest -q
```

### With coverage (package `app/` only)
```bash
pytest -q --maxfail=1 --disable-warnings --cov=app --cov-report=term-missing --cov-report=xml
```

**Coverage config:**
- `.coveragerc` focuses on `app/` and temporarily omits IO/network/CLI modules until tests cover them.
- Build fails under **80%** coverage (adjustable).

---

## 8) Deployment (optional)
CI is ready. For CD (e.g., Azure Web App, slots, or Docker/ACR), add a `cd.yml` workflow later:
- Use publish profiles (DEV/PROD) as GitHub secrets
- Configure `GROQ_API_KEY` in the target environment (App Settings)
- Document release steps in the repo

Open an issue if you want CD enabled.

---

## 9) FAQ / Troubleshooting
**ImportError: attempted relative import with no known parent package**  
Run with `streamlit run -m app.app`. A fallback in `app/app.py` also supports `streamlit run app/app.py`.

**Hangs during tests/streaming**  
Streaming uses a producer thread + queue; we always send a sentinel in `finally` to avoid deadlocks. Update to the latest `app/app.py`.

**CI didn’t run on my branch**  
CI triggers on push/PR to `main` and `develop`. Open a PR targeting `develop` (or update `ci.yml` to include your branch).

---

## 10) Credits / Acknowledgments
- Inspired by the DataTalks.Club AI/RAG exercises and the AI Agents crash course community.
- Thanks to open-source contributors and libraries used in this project.

---

## 12) Evaluations
Evaluations are essential for AI projects.

**Suggested structure**
```
eval/
  data-gen.ipynb        # question/case generation
  evaluations.ipynb     # evaluation logic and metrics
```

**What to mention here**
- Which metrics you use (e.g., factual accuracy, hit@k, citation precision)
- Headline results (e.g., “Acc@1: 78% over 200 questions”)
- A few good/bad examples

*Add your notebooks/scripts and a short summary of results in this section.*

---

## 13) Demo
Add a short video and a few GIFs/screenshots:

- 🎥 Main demo video — agent in action
- 🎞️ CLI gif (if you add a CLI)
- 🎞️ Streamlit gif of the web UI

Place assets in `assets/` and reference them:
```md
![ui](assets/ui.gif)
```

---


## 15) Project structure
```
faq-agent/
├── app/
│   ├── __init__.py
│   ├── app.py            # Streamlit UI (with import fallback)
│   ├── main.py           # CLI/entrypoint (if used)
│   ├── ingest.py         # GitHub indexing
│   ├── logs.py           # interaction logging
│   ├── search_agent.py   # agent initialization
│   └── search_tools.py   # utilities
├── tests/
│   ├── test_app_run.py
│   ├── test_app_stream.py
│   └── test_imports.py
├── .github/workflows/ci.yml
├── .coveragerc
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

