# GreenMind AI - AI Helper & PDF Analyzer

import os
import pypdf
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenRouter API
api_key = os.getenv("OPENROUTER_API_KEY")
ai_available = False
client = None

if api_key and api_key != "YOUR_OPENROUTER_API_KEY_HERE":
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        ai_available = True
    except Exception as e:
        print(f"Error configuring OpenRouter API: {e}")

def extract_pdf_text(uploaded_file):
    """
    Extracts text from an uploaded PDF file using pypdf.
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def generate_rag_answer(query, retrieved_contexts, chat_history=None):
    """
    Generates an answer grounded in the retrieved knowledge base contexts.
    Uses Gemini API if available, else falls back to local rule-based generation.
    """
    # Truncate user query to prevent huge context injections
    safe_query = query[:500]

    # Format contexts
    context_str = ""
    for idx, ctx in enumerate(retrieved_contexts):
        context_str += f"[Source {idx+1}: {ctx['source']}]\n{ctx['text']}\n\n"
        
    system_prompt = (
        "You are GreenMind AI, an expert sustainability decision-support copilot for campuses.\n"
        "Your task is to answer user queries using ONLY the provided retrieved context below.\n"
        "If the query cannot be answered using the context, state that clearly and suggest consulting site facilities.\n"
        "Format your answer beautifully in markdown. Acknowledge the sources of your information.\n"
        "Adhere to Responsible AI guidelines: be transparent, mention any limitations, and maintain an objective tone.\n\n"
        f"--- RETRIEVED CONTEXT ---\n{context_str}\n"
    )
    
    if ai_available:
        try:
            api_messages = [{"role": "system", "content": system_prompt}]
            
            # Append historical messages for conversational memory (limit to last 4 to save context window)
            if chat_history:
                for msg in chat_history[-4:]:
                    # Skip the current query which was just appended to the chat_history in copilot.py before calling this
                    # Actually, copilot appends the user_query to history before calling generate_rag_answer
                    # Let's just pass all history except the very last one if it's the current query
                    if msg["content"] != query:
                        api_messages.append({"role": msg["role"], "content": msg["content"]})
                        
            api_messages.append({"role": "user", "content": safe_query})
            
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=api_messages,
                max_tokens=600,  # Hard limit on output tokens
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return _generate_fallback_rag_answer(query, retrieved_contexts, error_msg=str(e))
    else:
        return _generate_fallback_rag_answer(query, retrieved_contexts)

def analyze_pdf_content(filename, pdf_text):
    """
    Analyzes uploaded PDF content (energy/water audit, policy) to extract:
    1. Executive Summary
    2. Key Sustainability Issues/Leaks/Inefficiencies
    3. Identified Risks
    4. Suggested Actionable Improvements
    5. UN SDG Mapping
    """
    system_prompt = (
        "You are GreenMind AI, an expert sustainability auditor. Analyze the following document text "
        "and generate a structured sustainability audit report.\n"
        "Format the output in markdown with clear headings:\n"
        "## Executive Summary\n"
        "## Key Sustainability Issues\n"
        "## Identified Risks (Environmental, Financial, Operational)\n"
        "## Suggested Actionable Improvements\n"
        "## SDG Mapping (Map findings to specific UN SDGs, especially 6, 7, 11, 12, 13)\n\n"
        "Be extremely specific to the numbers and data found in the text. If no specific numbers are found, note that."
    )
    
    if ai_available:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"--- DOCUMENT TEXT ({filename}) ---\n{pdf_text[:6000]}\n"}  # Reduced from 12000 to save context costs
                ],
                max_tokens=1000, # Hard limit on audit output
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenRouter API Error: {e}")
            return _generate_fallback_pdf_analysis(filename, pdf_text, error_msg=str(e))
    else:
        return _generate_fallback_pdf_analysis(filename, pdf_text)

# --- FALLBACK GENERATORS (for Offline / Missing API Key use cases) ---

def _generate_fallback_rag_answer(query, retrieved_contexts, error_msg=None):
    """Fallback generator for RAG questions when Gemini API is unavailable."""
    # Find matching keywords and combine contexts
    answer = ""
    if error_msg:
        answer += f"> *[Notice: Running in offline mode due to API configuration issue. Displaying local RAG synthesis.]*\n\n"
    else:
        answer += f"> *[Notice: Running in offline/local RAG mode. Configure OPENROUTER_API_KEY in .env for full AI capabilities.]*\n\n"
        
    answer += "### Summary of Retrieved Guidance:\n"
    
    sources = set()
    for ctx in retrieved_contexts:
        sources.add(ctx["source"])
        
    # Standard responses based on matching words in query
    query_lower = query.lower()
    
    if "electricity" in query_lower or "energy" in query_lower or "solar" in query_lower:
        answer += (
            "- **HVAC optimization:** Keep AC units set to 24°C - 26°C. Every 1°C increase saves ~6% energy. Clean filters regularly.\n"
            "- **LED Upgrade:** Swap fluorescent tubes for LEDs to reduce lighting power consumption by 50%.\n"
            "- **Solar PV Feasibility:** Rooftop solar PV systems yield about 4 units (kWh) per kWp daily. 1 kWp requires ~10 sq. meters of space.\n"
        )
    elif "water" in query_lower or "leak" in query_lower or "conservation" in query_lower:
        answer += (
            "- **Low-Flow Fixtures:** Installing aerators on faucets reduces flow from 15 L/min to <6 L/min.\n"
            "- **Dual-Flush Systems:** Use 3L/6L dual flush mechanisms instead of traditional 9-12L units.\n"
            "- **Rainwater Harvesting:** Collect roof runoff. 1 mm of rain on 1 sq. meter roof produces ~0.9 liters of harvestable water.\n"
        )
    elif "waste" in query_lower or "plastic" in query_lower or "recycle" in query_lower or "compost" in query_lower:
        answer += (
            "- **Waste Segregation:** Deploy color-coded bins (Green for organic, Blue for dry recyclables, Red/Black for landfill).\n"
            "- **On-site Composting:** Process food waste via aerobic or vermicomposting to generate organic fertilizers for landscaping.\n"
            "- **Paper Reduction:** Transition admin registers and student homework assignments to cloud platforms.\n"
        )
    else:
        answer += (
            "Based on our campus sustainability guidelines:\n"
            "- We recommend adopting source segregation, sensor-based lights, and sub-metering to track usage.\n"
            "- Set thermostats to 24°C and ensure regular maintenance of overhead water tanks to prevent overflows.\n"
        )
        
    answer += "\n### Grounded Sources Utilized:\n"
    for s in sources:
        answer += f"- *{s}*\n"
        
    answer += "\n*Note: This response is synthesized using keyword retrieval from your local knowledge repository.*"
    return answer

def _generate_fallback_pdf_analysis(filename, pdf_text, error_msg=None):
    """Fallback generator for PDF analysis when Gemini API is unavailable."""
    report = ""
    if error_msg:
        report += f"> *[Notice: Running in offline mode due to API configuration issue. Displaying rule-based text analysis.]*\n\n"
    else:
        report += f"> *[Notice: Running in offline document analysis mode. Configure OPENROUTER_API_KEY in .env for full AI capabilities.]*\n\n"
        
    # Analyze text length and search keywords to build a mock smart summary
    words = pdf_text.lower()
    
    # Simple rule based checks to see what the PDF is about
    doc_type = "Sustainability Audit Report"
    if "energy" in words or "electricity" in words or "kwh" in words:
        doc_type = "Energy Consumption & Audit Report"
    elif "water" in words or "liters" in words or "flow" in words:
        doc_type = "Water Utility & Management Report"
    elif "waste" in words or "recycling" in words or "landfill" in words:
        doc_type = "Solid Waste Audit"

    report += f"# Sustainability Document Analysis: {filename}\n\n"
    report += f"## Executive Summary\n"
    report += f"The uploaded document appears to be a **{doc_type}**. We have scanned {len(pdf_text)} characters of text. "
    report += "Initial assessment indicates resource usage patterns typical of institutional settings. "
    
    # Key issues
    report += "\n## Key Sustainability Issues\n"
    issues = []
    if "energy" in words or "electricity" in words:
        issues.append("High standby energy consumption (vampire load) from IT labs and smart classrooms overnight.")
        issues.append("Inefficient HVAC filtration leading to higher compressor workload.")
    if "water" in words or "leak" in words:
        issues.append("Unmonitored water usage in hostels leading to average consumption exceeding 135 LPCD.")
        issues.append("Absence of sub-meters, preventing isolation of underground pipe leakages.")
    if len(issues) == 0:
        issues.append("Standard operating baseline requires modernization.")
        issues.append("Lack of real-time monitoring and sensor-based controls.")
        
    for issue in issues:
        report += f"- {issue}\n"
        
    # Identified risks
    report += "\n## Identified Risks\n"
    report += "- **Financial:** Exposure to rising municipal energy/water tariffs due to high consumption baselines.\n"
    report += "- **Environmental:** High carbon footprint from carbon-intensive grid electricity.\n"
    report += "- **Operational:** Infrastructure strain on pump sets and plumbing valves from continuous operations.\n"
    
    # Improvements
    report += "\n## Suggested Actionable Improvements\n"
    if "energy" in words or "electricity" in words:
        report += "- **Action 1:** Install motion-sensor lights in public bathrooms and corridors.\n"
        report += "- **Action 2:** Conduct a solar feasibility study for building rooftops (100 kWp potential).\n"
    if "water" in words or "leak" in words:
        report += "- **Action 3:** Retrofit standard faucets with low-flow aerators.\n"
        report += "- **Action 4:** Implement bi-annual plumbing pressure tests to trace pipe degradation.\n"
    if "waste" in words:
        report += "- **Action 5:** Implement organic waste vermicomposting for mess kitchen scraps.\n"
        
    # SDG Mapping
    report += "\n## SDG Mapping\n"
    if "energy" in words or "electricity" in words:
        report += "- **SDG 7 (Affordable and Clean Energy):** Targets 7.2 (increasing renewable share) and 7.3 (doubling energy efficiency).\n"
    if "water" in words or "leak" in words:
        report += "- **SDG 6 (Clean Water and Sanitation):** Target 6.4 (improving water-use efficiency).\n"
    report += "- **SDG 11 (Sustainable Cities & Communities):** Enhancing micro-campus infrastructure.\n"
    report += "- **SDG 12 (Responsible Consumption):** Lowering institutional operational waste.\n"
    
    return report
