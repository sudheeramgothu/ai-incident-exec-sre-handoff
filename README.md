# 🧠 AI-Driven Incident Briefing & Response Orchestrator (Advanced Demo)

### AI in Incident Response: Automating Context, Not Judgment  

Welcome!  
This repo powers the live demo from the **KSU IT 7103 / Industry Workshop (Oct 30 2025)** led by **Sudheer Amgothu**, *Principal Cloud Operations Engineer at Google*.  

In this session, we explored how **AI can accelerate incident response** without replacing human judgment.  
You’ll build and run a small, enterprise-style **AI-Assisted Incident Briefing Orchestrator** that simulates how real SRE and DevOps teams communicate during live outages.

---

## 🚀 What You’ll Build
- 🧩 **Collector Service** – Ingests synthetic monitoring alerts  
- 🤖 **AI Engine** – Drafts both:  
  - 🧾 *Executive Brief* – leadership summary  
  - 🔧 *SRE Handoff* – technical recovery checklist  
- 🔒 **Governance Layer** – enforces “human-in-the-loop” approval  
- 📊 **Streamlit Dashboard** – review and approve drafts  
- 💬 **Optional Slack Integration** – posts staged updates to a channel  

---

## 🎯 Learning Outcomes
- Understand how AI can **automate context generation**, not control  
- Design **approval workflows** around AI systems for enterprise safety  
- Explore **incident-response automation** using real DevOps concepts (monitoring, notifications, dashboards)  
- Experience how **SRE principles and AI** intersect in modern cloud operations  

---

## ⚙️ Tech Stack
**Python 3 · Streamlit · Requests · JSON Store · (Optionally Slack Webhooks)**  

This project is an **enterprise-style simulation** of an AI-assisted incident-communication workflow.  
It demonstrates architecture, governance, Slack-style notifications, and a live approval dashboard.

---

## 🧱 Components
| File | Purpose |
|------|----------|
| `collector.py` | Simulates alert ingestion from monitoring (Prometheus / CloudWatch / Datadog) |
| `ai_engine.py` | Generates two drafts (Executive Brief + SRE Handoff) **offline-safe** |
| `notifier.py` | Posts drafts to Slack (optional) or prints to console |
| `timeline.py` | Persists incidents + approval state in a local JSON store |
| `dashboard.py` | Streamlit dashboard for visualization & approval |
| `run_demo.py` | End-to-end orchestrator to simulate a new incident |
| `config.example.json` | Template config file — copy to `config.json` and add your Slack webhook |
| `incident_store.json` | Local JSON file where incidents are stored |

---

## ⚡ Quick Start

```bash
# 1️⃣  Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows PowerShell

# 2️⃣  Install dependencies
pip install requests streamlit

# 3️⃣  Run a simulated incident
python run_demo.py

# 4️⃣  In a separate terminal, launch the dashboard
streamlit run dashboard.py
