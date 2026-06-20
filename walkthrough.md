# Project Walkthrough - GreenMind AI

GreenMind AI is a sustainability-focused AI decision-support system designed to align with the **IBM SkillsBuild + AICTE AI for Sustainability Internship** requirements. 

This document summarizes the files created, system features, and guides you through presenting the prototype using the built-in demo materials.

---

## 📁 Project Structure Built

All project files have been built inside `d:/Files and Docs/B.Tech/Projects/Greenmind_AI`:

```text
Greenmind_AI/
│
├── .env.example          # Template for environment settings
├── requirements.txt      # Python library dependencies
├── app.py                # Main Streamlit entrance & layout router
├── generate_samples.py   # Script that generated the sample PDFs
│
├── utils/
│   ├── ai_helper.py      # Gemini API wrappers & pypdf parser
│   ├── calculations.py   # Mathematical scoring formulas & simulator backend
│   └── rag_store.py      # Local TF-IDF search indexer
│
├── components/
│   ├── dashboard.py      # Overall scorecard & Responsible AI page
│   ├── copilot.py        # AI RAG chat system
│   ├── doc_analyzer.py   # PDF uploader and auditor
│   ├── simulator.py      # What-If sliders & Plotly graphs
│   └── methodology.py    # Design thinking & evaluation walkthrough
│
├── knowledge_base/       # Raw curated RAG text guidelines
│   ├── campus_sustainability_policies.txt
│   ├── energy_conservation_best_practices.txt
│   ├── government_sustainability_reports.txt
│   ├── un_sdg_documentation.txt
│   ├── waste_management_guidelines.txt
│   └── water_conservation_guidelines.txt
│
└── sample_data/          # Generated PDF audit reports
    ├── sample_energy_audit.pdf
    └── sample_water_consumption.pdf
```

---

## 🚀 Key Features Implemented

### 1. Sustainability Score & Dashboard (Page 1)
* **Score & Grade System:** Programmatic grading (A+ to F) evaluating real-time campus metrics (kwh/student, LPCD, waste recycling, carbon offsets).
* **Responsible AI & Transparency:** Dedicated footer block detailing exact scoring math, RAG parameters, privacy protocols (in-memory parsing), and limitations/uncertainties.
* **Plotly Visual Comparison:** Double-bar chart comparing baseline performance against simulated optimizations.

### 2. AI Sustainability Copilot (Page 2)
* **Local RAG Integration:** Queries are grounded against local reference files using a custom in-memory TF-IDF index.
* **Sources & Citations Accordion:** Displays retrieved passages and matching scores below generated text for citation transparency.

### 3. PDF Document Analyzer (Page 3)
* **PDF Parser:** Uses `pypdf` to read custom uploaded energy audit sheets.
* **Auditing:** Extracts summary, risks, actionable changes, and maps results to SDGs.
* **Demo Mode:** Clickable buttons to instantly feed in pre-loaded energy/water PDF reports.

### 4. What-If Scenario Simulator (Page 4)
* **Interactive Sliders:** Adjust energy, solar, water, and waste variables.
* **Real-time Metrics:** Displays CO2 offsets, tree equivalencies, and monetary savings.
* **Dashboard Locking:** Button to apply parameters globally to the main scorecard.

### 5. Design Thinking & Methodology (Page 5)
* Summarizes the 5 phases (Empathize, Define, Ideate, Prototype, Test), architecture details, and presentation instructions.

---

## 📸 Interactive Verification & Walkthrough

Here is the recorded video demonstration and screenshots captured from the verified prototype interface:

### 🎥 Prototype Demo Recording
![Walkthrough Video](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/greenmind_ai_demo_1781274120770.webp)

---

### 🖼️ Step-by-Step UI Screenshots

````carousel
![1. Default Scorecard Dashboard (Grade F)](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/baseline_scorecard_1781274140869.png)
<!-- slide -->
![2. PDF Document Analyzer Audit Output](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/energy_audit_analysis_1781275769534.png)
<!-- slide -->
![3. What-If Simulator Page (100 kW Solar Added)](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/simulator_page_1781276042999.png)
<!-- slide -->
![4. Updated Scorecard showing Grade B](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/updated_scorecard_1781276136749.png)
<!-- slide -->
![5. AI Sustainability Copilot grounded RAG Chat](/C:/Users/monst/.gemini/antigravity/brain/11b25c3f-07c7-47ef-a798-20396b862e99/copilot_rag_response_1781276110840.png)
````

---

## ⚙️ How to Run Locally

To run the system on your computer:

1. **Activate the Environment:** Navigate to `Greenmind_AI` and ensure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API Key (Optional):** Copy `.env.example` to `.env` and paste your Google Gemini API Key.
   * *If no key is configured, the application automatically runs in an offline/local mode with built-in rule-based summaries and keywords retrieval, so it remains 100% functional for presentations!*
3. **Launch the Application:**
   ```bash
   streamlit run app.py
   ```
4. Open the displayed URL (normally `http://localhost:8501`) in your browser to interact with the prototype.
