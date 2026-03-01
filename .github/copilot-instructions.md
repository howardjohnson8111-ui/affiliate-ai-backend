# Copilot Instructions for Affiliate AI Pro

## Project Overview
Affiliate AI Pro is a multi-persona AI assistant system for affiliate marketing, finance, learning, and multilingual support. It combines a Python AI service (`ai_service.py`) and a Node.js backend (`server.js`). The system uses Google Gemini API and is designed for extensibility and natural language interaction.

## Architecture & Data Flow
- **Personas:** Six executive personas (Campaign Manager, Stock Analyst, Learning Manager, Financial Assistant, App Customizer, Language Assistant).
- **Persona Detection:** Input is routed by explicit mention or keyword analysis (see `demo_personas.py`).
- **Tool Routing:** Gemini selects persona-specific tools/functions, which are executed by Python or Node.js backend.
- **Backend:** Node.js (`server.js`) exposes REST endpoints for campaigns and transactions. Supabase integration is planned.
- **Documentation:** Key guides are in `SYSTEM_DOCUMENTATION.md` and `QUICK_REFERENCE.md`.

## Developer Workflows
- **Start Backend:**
  ```powershell
  $env:GOOGLE_API_KEY='your-api-key'
  node server.js
  ```
- **Start AI Service:**
  ```bash
  python ai_service.py
  ```
- **Run Persona Demo:**
  ```bash
  python demo_personas.py
  ```
- **Test Transaction Logging:**
  ```bash
  python test_transaction.py
  ```
- **API Endpoints:**
  - Campaigns: `/api/campaigns` (CRUD)
  - Transactions: `/api/transactions` (POST, GET)
  - Health: `/api/health`

## Project-Specific Patterns & Conventions
- **Persona invocation:** Explicit ("Campaign Manager, ...") or implicit (keyword-based).
- **Tool execution:** Functions are called via Gemini, not direct user commands.
- **Error handling:** All endpoints validate input and avoid leaking sensitive info.
- **Environment:** API keys must be set in environment variables.
- **Extensibility:** Placeholders for stock, learning, app customizer, and language tools are ready for implementation.
- **Testing:** Scripts in root directory (e.g., `test_api.py`, `test_e2e.py`).

## Integration Points
- **Google Gemini API:** Used for AI persona logic and tool execution.
- **Node.js Backend:** Handles campaign and transaction data; ready for Supabase migration.
- **Supabase:** Planned for persistent storage (see `SUPABASE_SCHEMA.sql`).

## Key Files & Directories
- `ai_service.py` — Main AI logic, persona routing, tool execution
- `server.js` — Node.js backend, REST API
- `demo_personas.py` — Persona detection demo
- `SYSTEM_DOCUMENTATION.md` — Architecture and usage guide
- `QUICK_REFERENCE.md` — Command reference
- `test_transaction.py` — Transaction test script

## Example Usage
- "Create a new Instagram campaign called Summer Sale"
- "Log a $500 affiliate payout"
- "Translate to French"

## Troubleshooting
- If `GOOGLE_API_KEY` not set: `$env:GOOGLE_API_KEY='your-api-key'`
- If port 3001 is busy: Stop Node processes and restart
- If Python module missing: `pip install google-generativeai requests`

---
For more, see `SYSTEM_DOCUMENTATION.md` and `README_COMPLETE.md`. Update this file as new features are added.
