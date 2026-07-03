# Autonomous Literature Research for Tad

**Status:** parked — not needed while bttdb research material is unexhausted; idea logged in backlog

Research into how to build a system where Claude Code autonomously conducts literature review, extracts knowledge, generates hypotheses, and produces structured research — with minimal human in the loop.

> **Methodological note — scan adjacent ecosystems.** The initial research focused on infrastructure (how to build the system) and missed HuggingFace as a major content source until the human asked about it. Lesson: when running multi-agent research sprints, always include an **"adjacent ecosystems" sweep** — a dedicated pass that checks major data/content platforms (HuggingFace, Kaggle, Papers With Code, Quantopian archives, QuantConnect, domain-specific forums) for relevant resources that aren't obviously connected to the infrastructure question. Codify this as a mandatory step in `/lit-survey` and similar research skills.

## Context

Tad needs a literature and SOTA review to guide its roadmap — covering short-term reversal, regime detection, position sizing, earnings drift, conditional strategies, and more. The goal is to build infrastructure so Claude can do this research autonomously, not a workflow where the human reads papers.

## Why Not NotebookLM

The initial hypothesis was to use NotebookLM as a queryable document backend for Claude via MCP. After thorough research: **skip it**.

- **No official API.** Google has never released a public API for consumer NotebookLM. The Enterprise API (v1alpha, Sep 2025) can manage notebooks/sources but has **no query/chat endpoint** — the core RAG functionality is missing from the official API.
- **All MCP servers use unofficial APIs.** The ~7 GitHub repos (most popular: `jacob-bd/notebooklm-mcp-cli` at 2.7k stars) either reverse-engineer internal RPC endpoints or use Puppeteer browser automation with extracted Google cookies. Auth breaks periodically, any Google UI update can break everything.
- **Heavy context cost.** The most complete MCP server exposes 35 tools — a lot of context window to burn.
- **Better alternatives exist.** Purpose-built local RAG MCP servers are more reliable, faster, and don't depend on a third party's undocumented internals.

## Recommended Architecture

### Layer 1: Discovery (Find Papers Automatically)

| Tool             | Type       | Purpose                                                                                                              |
| ---------------- | ---------- | -------------------------------------------------------------------------------------------------------------------- |
| ScholarMCP       | MCP server | Federated search: OpenAlex, Crossref, Semantic Scholar, Google Scholar. Full PDF download + citation graph traversal |
| arxiv-mcp-server | MCP server | arXiv search, download, read. 2.4k stars, most mature                                                                |
| Exa MCP          | MCP server | Semantic web search — blog posts, code, non-academic sources. 4.1k stars                                             |

### Layer 2: Knowledge Backend (Ingest, Search, Reason)

Three levels, each building on the previous:

## Level a — Direct PDF Reading (No Infra, Start Here)

- Download PDFs to `docs/literature/papers/`
- Claude reads them directly with the Read tool (up to 20 pages per call)
- Works for ~10-30 papers. Zero setup.

## Level B — Markdown Conversion + Grep (Light Infra)

- Convert PDFs to markdown using Marker (32.9k stars, handles equations/tables/academic formatting, `pip install marker-pdf`)
- Store in a directory, use native Grep/Read
- Scales to ~200 papers. Setup: 30 minutes.

## Level C — Local RAG MCP (Full Semantic Search)

- **kb-mcp-server** (txtai-based) — portable knowledge bases, customizable embedding model (can use finance-specialized `voyage-finance-2`), knowledge graph construction
- Alternative: **mcp-local-rag** (171 stars) — zero-setup (`npx`), generic embeddings
- Scales to 500+ papers. Setup: 1-2 hours.

### Layer 3: Autonomous Research Workflow

**ARIS** (`wanshuiyin/Auto-claude-code-research-in-sleep`, 2.7k stars) is the most mature framework for autonomous research with Claude Code:

- Implemented as plain markdown skill files (zero dependencies)
- Multi-phase workflow: literature survey -> idea generation -> novelty validation -> experiment -> review
- Cross-model adversarial review (Claude researches, another model critiques)
- Ralph loops for crash-resilient multi-session execution
- First community paper scored 8/10 at conference review

**Anthropic's multi-agent research system** validates the pattern: orchestrator (Opus) + 3-5 subagents (Sonnet) in parallel. 90.2% improvement over single-agent. Key lesson: subagents store artifacts externally, pass lightweight references.

### Proposed System Layout

```text
Claude Code skills:
  /lit-search <topic>     — discover papers via MCP servers
  /lit-ingest <paper>     — read & extract structured data
  /lit-survey <question>  — multi-agent survey across sources
  /lit-hypothesis <idea>  — generate testable hypothesis for Tad
  /lit-gap-analysis       — cross-reference literature vs Tad's implementation

docs/literature/
  _index.md               — master map: topics -> papers -> findings
  reversal.md             — topic synthesis
  regime-detection.md     — topic synthesis
  position-sizing.md      — topic synthesis
  extractions/            — per-paper structured data
    lo-mackinlay-1990.md
    ...
  papers/                 — downloaded PDFs/markdown
```

### Per-Paper Extraction Schema

| Field                      | Example                            |
| -------------------------- | ---------------------------------- |
| Signal definition          | 5-day return normalized by 20d vol |
| Universe                   | S&P 500, liquid US equities        |
| Holding period             | 5-20 days                          |
| Reported Sharpe            | 0.8-1.2 annualized                 |
| Key conditioning variables | Volatility regime, volume, sector  |
| Decay profile              | Alpha halves every 3 years         |
| Data period                | 1990-2020                          |
| Relevant to Tad?           | Direct — same signal family        |
| Implementation delta       | Tad uses X, paper suggests Y       |

## LLM-Driven Alpha Mining (Relevant Prior Art)

Several recent systems do programmatically what Tad does with a human in the loop:

| System                | Year | Key Result                                                                                                                                                           |
| --------------------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AlphaAgent (KDD)      | 2025 | Multi-agent: hypothesis -> factor construction -> evaluation. 81% hit ratio improvement, 37%+ excess returns on S&P 500                                              |
| Microsoft RD-Agent(Q) | 2025 | Most mature open-source. Full pipeline: hypothesize -> implement -> backtest -> multi-armed bandit for next direction. 2x returns, 70% fewer factors. Built on Qlib. |
| QuantaAlpha           | 2026 | LLM reasoning + code generation for factor construction with iterative backtest feedback                                                                             |
| QuantEvolve           | 2025 | Multi-agent evolutionary strategy generation and refinement                                                                                                          |
| Alpha-GPT (EMNLP)     | 2025 | Interactive human-AI alpha mining via prompt engineering                                                                                                             |

## Further Investigation

- **Polymarket as an insider trading signal.** Prediction markets are less regulated, pseudonymous, and lower-barrier than equity markets — potentially attractive for informed participants to trade on private information ahead of corporate/regulatory events. Unusual volume/price action on event-specific contracts could be a leading indicator. Needs investigation: what event-specific contracts exist, whether volume is sufficient for anomaly detection, academic work on prediction markets as informed-trading canaries, and whether Kalshi (regulated US competitor) has more relevant contract types. Polymarket has excellent data access (free API, Python SDK, 163GB HuggingFace dataset of all trades).

## Implementation Plan

1. **Phase 1 — Install discovery layer (30 min):** Install ScholarMCP, arxiv-mcp-server, optionally Exa MCP. Test with a sample query.
2. **Phase 2 — Build research skills (2-3 hours):** Create `/lit-search`, `/lit-ingest`, `/lit-survey` skills. Define extraction schema. Create `docs/literature/` structure.
3. **Phase 3 — First autonomous research sprint:** Multi-agent survey on core strategy areas. Produce initial literature map. Gap analysis vs Tad's current implementation.
4. **Phase 4 — Knowledge backend (when corpus hits 20+ papers):** Set up Marker for PDF->markdown. Optionally set up kb-mcp-server for semantic search.

## Sources

### NotebookLM MCP Servers

- [jacob-bd/notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) — 2.7k stars, most feature-complete, reverse-engineered APIs
- [PleasePrompto/notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp) — 1.5k stars, TypeScript, Puppeteer-based
- [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) — 6.4k stars, underlying unofficial Python client
- [Google Cloud: NotebookLM Enterprise API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) — v1alpha, no query endpoint
- [Google AI Forum: How to Access NotebookLM Via API](https://discuss.ai.google.dev/t/how-to-access-notebooklm-via-api/5084)

### Discovery Tools (MCP Servers)

- [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) — federated academic search + PDF ingestion
- [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) — 2.4k stars, arXiv search/download/read
- [exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) — 4.1k stars, semantic web search
- [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) — 107 stars
- [xingyulu23/Academix](https://github.com/xingyulu23/Academix) — unified search across 5 databases

### Knowledge Backend / RAG

- [Geeksfino/kb-mcp-server](https://github.com/Geeksfino/kb-mcp-server) — txtai-based, portable knowledge bases
- [shinpr/mcp-local-rag](https://github.com/shinpr/mcp-local-rag) — 171 stars, zero-setup local RAG
- [juanqui/pdfkb-mcp](https://github.com/juanqui/pdfkb-mcp) — Docker, multi-parser, hybrid search
- [chroma-core/chroma-mcp](https://github.com/chroma-core/chroma-mcp) — 514 stars, official Chroma MCP
- [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) — 1.3k stars, official Qdrant MCP
- [lyonzin/knowledge-rag](https://github.com/lyonzin/knowledge-rag) — local hybrid search for Claude Code
- [jztan/pdf-mcp](https://github.com/jztan/pdf-mcp) — PDF reading with SQLite caching

### PDF-to-Markdown Conversion

- [datalab-to/marker](https://github.com/datalab-to/marker) — 32.9k stars, best for academic papers
- [opendatalab/MinerU](https://github.com/opendatalab/MinerU) — 56.6k stars, scientific documents
- [docling-project/docling](https://github.com/docling-project/docling) — 56.2k stars, IBM Research, has MCP integration

### Autonomous Research Frameworks

- [wanshuiyin/Auto-claude-code-research-in-sleep (ARIS)](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) — 2.7k stars, most mature
- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — 15.6k stars, 170+ skills (bioscience focused)
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) — 25.9k stars, planner-executor-publisher
- [stanford-oval/storm](https://github.com/stanford-oval/storm) — Wikipedia-style article generation via multi-perspective research
- [Alibaba-NLP/DeepResearch](https://github.com/Alibaba-NLP/DeepResearch) — 18.5k stars, open-source deep research

### LLM-Driven Alpha Mining

- [Automate Strategy Finding with LLM in Quant Investment](https://arxiv.org/html/2409.06289v2) — EMNLP 2025
- [AlphaAgent: LLM-Driven Alpha Mining](https://arxiv.org/html/2502.16789v2) — KDD 2025
- [QuantEvolve](https://arxiv.org/html/2510.18569v1) — multi-agent evolutionary strategies
- [QuantaAlpha](https://arxiv.org/html/2602.07085v1) — LLM reasoning for factor construction
- [From Deep Learning to LLMs: A Survey of AI in Quantitative Investment](https://arxiv.org/html/2503.21422v1)
- [The New Quant: A Survey of LLMs in Financial Prediction and Trading](https://arxiv.org/html/2510.05533v1)
- [Microsoft RD-Agent on GitHub](https://github.com/microsoft/RD-Agent)
- [Microsoft Qlib on GitHub](https://github.com/microsoft/qlib)
- [virattt/dexter](https://github.com/virattt/dexter) — 18.1k stars, autonomous financial research agent

### AI Literature Review Tools (Non-MCP)

- [Elicit](https://elicit.com/) — systematic review workflow, 94-99% extraction accuracy
- [Semantic Scholar](https://www.semanticscholar.org/) — 200M+ papers, free
- [Connected Papers](https://www.connectedpapers.com/) — visual similarity graph from seed papers
- [Research Rabbit](https://www.researchrabbit.ai/) — collection-based exploration
- [Litmaps](https://www.litmaps.com/) — citation maps + new paper monitoring
- [Consensus](https://consensus.app/) — research Q&A with consensus meter

---

## Hugging Face Datasets

HF has three genuine connections to Tad's research system.

### 1. Literature Review Corpus

HF hosts 1.7M arXiv papers as a dataset. Filter to `q-fin.*` categories for a searchable corpus of quant finance papers with abstracts and metadata. No SSRN equivalent exists on HF.

| Dataset                         | Size        | Content                                                |
| ------------------------------- | ----------- | ------------------------------------------------------ |
| `arxiv-community/arxiv_dataset` | 1.7M papers | Titles, authors, categories, abstracts, full-text PDFs |
| `common-pile/arxiv_papers`      | 2.4M papers | Broader coverage                                       |

### 2. NLP-Based Signal Data

HF's strongest area for quant finance. Could feed a news/earnings NLP signal sleeve orthogonal to reversal.

**Earnings transcripts:**

| Dataset                            | Size             | Content                                          |
| ---------------------------------- | ---------------- | ------------------------------------------------ |
| `kurry/sp500_earnings_transcripts` | 33k+ transcripts | S&P 500 earnings calls, 685 companies, 20+ years |

**Financial news:**

| Dataset                                                  | Size                      | Content                             |
| -------------------------------------------------------- | ------------------------- | ----------------------------------- |
| `Brianferrell787/financial-news-multisource`             | 57M rows                  | 24 public news datasets normalized  |
| `Zihan1004/FNSPID`                                       | 29.7M news + 15.7M prices | 4,775 S&P 500 companies, 1999-2023  |
| `KrossKinetic/SP500-Financial-News-Articles-Time-Series` | —                         | News time-aligned with S&P 500 data |

**Sentiment models:**

| Model                                          | Type | Notes                                                      |
| ---------------------------------------------- | ---- | ---------------------------------------------------------- |
| `ProsusAI/finbert`                             | BERT | The standard. 3-class sentiment. QuantConnect integration. |
| `yiyanghkust/finbert-tone`                     | BERT | Fine-tuned on analyst report sentences                     |
| `ahmedrachid/FinancialBERT-Sentiment-Analysis` | BERT | Pre-trained on large financial corpora                     |

**SEC filings:**

| Dataset                             | Size      | Content                                                           |
| ----------------------------------- | --------- | ----------------------------------------------------------------- |
| `jlohding/sp500-edgar-10k`          | S&P 500   | 10-K filings 2010-2022 with n-day future returns from filing date |
| `JanosAudran/financial-reports-sec` | 1993-2020 | 10-K filings broken into 20 sections                              |

### 3. HF MCP Server (Official)

One-liner to add to Claude Code for discovering datasets and models:

```bash
claude mcp add --transport http hf-skills https://huggingface.co/mcp?bouquet=skills --header "Authorization: Bearer $HF_TOKEN"
```

Good for discovery. Actual data loading still requires `datasets` library or direct Parquet URLs.

### Where HF Is Weak for Tad

- **Factor/alpha datasets**: None. Use [Open Source Asset Pricing](https://www.openassetpricing.com/) (319 characteristics) or WRDS.
- **Survivorship-bias-free universes**: None.
- **Point-in-time fundamentals**: None.
- For price/fundamental data quality, Tad's existing Massive API + Nasdaq setup is better.

### HF Sources

- [Traders-Lab/TroveLedger](https://huggingface.co/datasets/Traders-Lab/TroveLedger) — community OHLCV, S&P 500 + global indices
- [mito0o852/OHLCV-1m](https://huggingface.co/datasets/mito0o852/OHLCV-1m) — minute-level US stocks 1992-2025
- [FNSPID](https://huggingface.co/datasets/Zihan1004/FNSPID) — 29.7M news + 15.7M prices
- [financial-news-multisource](https://huggingface.co/datasets/Brianferrell787/financial-news-multisource) — 57M rows
- [sp500_earnings_transcripts](https://huggingface.co/datasets/kurry/sp500_earnings_transcripts) — 33k+ transcripts
- [sp500-edgar-10k](https://huggingface.co/datasets/jlohding/sp500-edgar-10k) — 10-K with returns
- [financial-reports-sec](https://huggingface.co/datasets/JanosAudran/financial-reports-sec)
- [financial_phrasebank](https://huggingface.co/datasets/takala/financial_phrasebank) — classic sentiment benchmark
- [ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert) — standard financial sentiment model
- [FinGPT](https://huggingface.co/FinGPT) — open financial LLMs
- [Open FinLLM Leaderboard](https://huggingface.co/spaces/finosfoundation/Open-Financial-LLM-Leaderboard)
- [HF MCP Server docs](https://huggingface.co/docs/hub/en/hf-mcp-server)
- [paperswithbacktest on HF](https://huggingface.co/paperswithbacktest) — 13 datasets (subscription required)
- [Open Source Asset Pricing](https://www.openassetpricing.com/) — 319 characteristics (not on HF)
