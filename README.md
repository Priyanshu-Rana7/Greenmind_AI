# 🌱 GreenMind AI

**GreenMind AI** is an intelligent, AI-powered sustainability decision-support dashboard designed specifically for educational institutions and campus facility managers. It was developed as part of the **IBM SkillsBuild / AICTE Internship Program** to demonstrate the application of Artificial Intelligence in achieving the United Nations Sustainable Development Goals (SDGs).

![GreenMind AI](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

---

## ✨ Key Features

1. **💬 AI Sustainability Copilot (RAG System):** 
   A conversational assistant that answers campus-specific policy and conservation queries. It is grounded in verified policy documents using a custom-built, pure-Python TF-IDF semantic search engine, ensuring zero hallucinations.
   
2. **📄 Document Analyzer:** 
   Upload dense campus utility bills or energy audits (PDFs). The AI automatically summarizes the document, flags operational risks, highlights inefficiencies, and maps findings directly to specific UN SDGs (e.g., SDG 6, 7, 11, 12, 13).

3. **🎛️ What-If Scenario Simulator:** 
   An interactive physics engine that allows administrators to adjust infrastructure levers (e.g., adding a 100kW solar array, fixing water leaks) and instantly calculates the resulting environmental impact, carbon offsets, and annual utility bill savings in real-time.

---

## 🛠️ Technology Stack

* **Frontend:** Streamlit (styled with modern, minimalist CSS overrides and Inter typography)
* **Backend:** Python
* **AI Integration:** OpenRouter API (`openai/gpt-4o-mini`)
* **Vector Search:** Custom In-Memory TF-IDF Indexer
* **Data Visualization:** Plotly Graph Objects

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Priyanshu-Rana7/Greenmind_AI.git
   cd Greenmind_AI
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key:**
   Create a `.env` file in the root directory and add your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 🛡️ Security & Limitations

To ensure stable operation and prevent API abuse, GreenMind AI implements:
* **Session Rate Limiting:** Capped at 15 queries per session for the Copilot.
* **Token Limits:** Hard token limits on generated output to prevent context window overflow.
* **Input Truncation:** Aggressive context truncation for PDF extractions to optimize OpenRouter costs.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
