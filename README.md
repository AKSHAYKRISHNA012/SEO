<div align="center">

# 🚀 SEO Intelligence — AI-Powered SEO / GEO / AEO Analyzer

![SEO Intelligence Banner](https://img.shields.io/badge/SEO-Intelligence-6366f1?style=for-the-badge&logo=google&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)

**A production-quality web application that analyzes any publicly accessible webpage and generates an actionable SEO, GEO, and AEO audit report — with a stunning, modern UI.**

[Live Demo](#) · [Report an Issue](https://github.com/AKSHAYKRISHNA012/seo-intelligence/issues) · [Portfolio](https://github.com/AKSHAYKRISHNA012)

</div>

---

## ✨ Features

### 🔍 Traditional SEO Analysis
- **Meta Tag Auditing** — Title length, meta description, canonical, robots directives
- **Open Graph & Twitter Cards** — Social sharing readiness
- **Heading Architecture** — H1–H6 hierarchy and keyword distribution
- **Content Quality** — Word count, readability (Flesch score), keyword density
- **Link Equity** — Internal/external link ratios, broken link flags
- **SERP Preview Simulator** — Real-time Google snippet preview

### 🤖 AEO — Answer Engine Optimization
- **Featured Snippet Readiness** — Question-based headings, direct answers
- **FAQ / Q&A Detection** — Extracted user questions with generated snippet answers
- **Structured List Analysis** — Ordered/unordered lists for AI parsing
- **Definition Blocks** — "What is…" style definitional content detection

### 🌐 GEO — Generative Engine Optimization
- **AI Readability Index** — How well ChatGPT, Perplexity, Gemini, and Claude can cite this page
- **Named Entity Recognition (NER)** — People, places, organizations, dates extracted
- **Fact Density Score** — Quantifiable claims and statistics
- **Author & E-E-A-T Signals** — Trust, expertise, authority signals
- **External Reference Quality** — Citation credibility analysis

### ⚙️ Technical SEO
- **Response Time & Status Codes** — Server latency and HTTP health
- **SSL/HTTPS Verification** — Secure connection audit
- **robots.txt & sitemap.xml** — Crawlability checks
- **Image Optimization** — Alt text compliance and lazy loading
- **Mobile Friendliness** — Viewport meta detection

### 📊 Structured Data
- **JSON-LD Schema Inspector** — Validates existing schema types
- **Microdata & RDFa Detection** — All structured data formats
- **Schema Recommendations** — Missing schemas with implementation code
- **Rich Result Potential** — FAQPage, Article, BreadcrumbList, Product support

### 📈 Scoring & Reports
- **Composite Score (0–100)** — Weighted across all 5 pillars
- **Interactive Dashboard** — Tabs, charts, and drill-down recommendations
- **Priority Action Plan** — Color-coded critical / warning / info items
- **PDF Report Export** — Downloadable executive audit report

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + TypeScript + Vite |
| **Styling** | TailwindCSS 3 + Custom Design System |
| **Charts** | Recharts |
| **Icons** | Lucide React |
| **PDF Export** | jsPDF + html2canvas |
| **Backend** | FastAPI + Python 3.11 |
| **Scraping** | httpx + BeautifulSoup4 + lxml |
| **Database** | SQLite (dev) / PostgreSQL (prod) via SQLModel |
| **Report Gen** | ReportLab |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **npm 9+**
- Git

---

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/AKSHAYKRISHNA012/seo-intelligence.git
cd seo-intelligence

# Create and activate virtual environment
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at: **http://127.0.0.1:8000**  
Interactive API docs: **http://127.0.0.1:8000/docs**

---

### Frontend Setup

```bash
# From the project root
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be available at: **http://localhost:5173**

---

### Environment Variables (Optional)

Create a `.env` file in `/backend/`:

```env
# Optional: Use PostgreSQL instead of SQLite
DATABASE_URL=postgresql://user:password@localhost/seointel

# Optional: Gemini API key for AI-enhanced analysis
GEMINI_API_KEY=your_key_here
```

---

## 📂 Project Structure

```
seo-intelligence/
├── backend/
│   ├── app/
│   │   ├── analyzer/
│   │   │   ├── fetcher.py          # Async webpage fetcher (httpx)
│   │   │   ├── seo_analyzer.py     # Traditional & technical SEO
│   │   │   ├── aeo_analyzer.py     # Answer Engine Optimization
│   │   │   ├── geo_analyzer.py     # Generative Engine Optimization
│   │   │   ├── schema_analyzer.py  # Structured data / JSON-LD
│   │   │   ├── scoring.py          # Weighted composite scoring
│   │   │   └── recommendations.py  # Priority action plan generator
│   │   ├── api/
│   │   │   └── routes.py           # FastAPI route handlers
│   │   ├── config.py               # Settings with pydantic-settings
│   │   ├── database.py             # SQLite/PostgreSQL engine
│   │   ├── models.py               # SQLModel database models
│   │   ├── schemas.py              # Pydantic request/response schemas
│   │   └── main.py                 # FastAPI app entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # App pages / views
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── utils/                  # Helpers and API client
│   │   ├── types/                  # TypeScript type definitions
│   │   ├── App.tsx                 # Root component
│   │   └── main.tsx                # Entry point
│   ├── public/
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── package.json
├── .gitignore
└── README.md
```

---

## 🎯 How It Works

```mermaid
graph LR
    A[User enters URL] --> B[FastAPI Backend]
    B --> C[httpx Fetcher]
    C --> D[BeautifulSoup Parser]
    D --> E1[SEO Analyzer]
    D --> E2[AEO Analyzer]
    D --> E3[GEO Analyzer]
    D --> E4[Schema Analyzer]
    E1 & E2 & E3 & E4 --> F[Scoring Engine]
    F --> G[Recommendations Engine]
    G --> H[React Dashboard]
    H --> I[PDF Report Export]
```

---

## 📸 Screenshots

| Landing Page | Analysis Results |
|---|---|
| ![Landing](https://via.placeholder.com/500x300?text=Landing+Page) | ![Results](https://via.placeholder.com/500x300?text=Analysis+Report) |

| AEO Tab | GEO Tab |
|---|---|
| ![AEO](https://via.placeholder.com/500x300?text=AEO+Analysis) | ![GEO](https://via.placeholder.com/500x300?text=GEO+Analysis) |

---

## 📡 API Reference

### `POST /api/analyze`
Analyze a webpage URL.

**Request:**
```json
{
  "url": "https://example.com",
  "force_fresh": false
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "overall_score": 78,
  "seo": { ... },
  "aeo": { ... },
  "geo": { ... },
  "technical": { ... },
  "structured_data": { ... },
  "recommendations": [ ... ],
  "analyzed_at": "2024-01-01T00:00:00Z"
}
```

### `GET /api/history`
Retrieve past audit records.

### `GET /api/health`
API health check endpoint.

---

## 🏆 Portfolio Context

This project was built as a **professional portfolio project** demonstrating expertise across:

- ✅ Full-stack web development (React + FastAPI)
- ✅ SEO / GEO / AEO strategy and implementation
- ✅ Web scraping and HTML parsing at scale
- ✅ REST API design and async Python
- ✅ Modern UI/UX with Tailwind and Recharts
- ✅ Database design with SQLModel (SQLite/PostgreSQL)
- ✅ AI-readiness analysis for LLM search engines

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ by [Akshay Krishna](https://github.com/AKSHAYKRISHNA012)**

⭐ Star this repo if you found it useful!

</div>
