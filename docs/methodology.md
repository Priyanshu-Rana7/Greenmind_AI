### 1. The Design Thinking Framework

**Empathize:**
* **Who it's for:** Campus facility managers and administrators who lack real-time tracking of where power and water are wasted.
* **Key pain point:** Reviewing large utility bills with no actionable insights or strategies.

**Define:**
* **Problem:** Campuses over-consume electricity, water, and produce excess waste — but administrators lack expert tools to act.
* **Scope:** Bridge the gap between raw utility data and optimized sustainable decisions.

**Ideate:**
Three AI-driven solutions were chosen:
1. **RAG Copilot** — answer campus-specific policy and conservation queries.
2. **PDF Auditor** — auto-summarize utility bills and flag risks.
3. **What-If Engine** — instant simulation without complex code.

**Prototype:**
Built with **Python + Streamlit**, OpenRouter API (`gpt-4o-mini`) for AI, and a local TF-IDF semantic search engine for RAG.

**Test:**
Tested PDF uploads on sample audits, validated calculations against benchmark guidelines, and audited RAG answers for source consistency.

---

### 2. Technical Architecture

* **Frontend:** Streamlit interactive browser UI styled with CSS overrides.
* **RAG Vector Database:** TF-IDF In-Memory Indexer loaded at runtime with local reference policies.
* **AI Processing Model:** OpenRouter API (`openai/gpt-4o-mini`) for synthesizing grounded RAG answers and auditing documents.
* **Simulation Engine:** Programmatic calculator evaluating energy, water, carbon indices, and potential score improvements.

---

### 3. Expected Project Impact

* **Environmental Impact:** Directly reduces greenhouse gas emissions and municipal water withdrawals via optimized controls.
* **Economic Impact:** Decreases monthly utility overheads, delivering immediate cost-savings.
* **Social & Educational Impact:** Instills a culture of resource consciousness among students, faculty, and administrative leadership.

---

### 4. Evaluation Guide

Quick steps to evaluate this prototype for the **IBM SkillsBuild + AICTE** presentation:

1. **Document Upload:** Go to *Document Analyzer* → click **Load Sample Energy Audit**. Check how the AI maps findings to SDG 7 and SDG 13.
2. **Simulation:** Go to *What-If Simulator* → set Solar PV to `100 kW` + Water Reduction to `25%`. Watch the grade and savings update live.
3. **RAG Chat:** Go to *AI Copilot* → ask *"How can our campus reduce electricity consumption?"* and verify the RAG source citations.
