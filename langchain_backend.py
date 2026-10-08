"""
LangChain Conversation Model for Gagandeep Kaur Portfolio
Integrates LangChain prompts, retrieval, and contextual knowledge to power
the "Start a Conversation" AI assistant.
"""

import os
import re
from typing import List, Dict, Any

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Profile Knowledge Base
PORTFOLIO_KNOWLEDGE = {
    "name": "Gagandeep Kaur",
    "title": "Governance & Development Professional | Project Management | MIS & Data Analysis | AI & Digital Solutions",
    "location": "Mohali, Punjab, India",
    "email": "gagan9041783@gmail.com",
    "phone": "+91 9041783035",
    "linkedin": "https://www.linkedin.com/in/gagandeepkaur25?utm_source=share_via&utm_content=profile&utm_medium=member_android",
    "upwork": "https://www.upwork.com/freelancers/~012d7b4c25524f13a6?mp_source=share",
    
    "bio": (
        "Gagandeep Kaur is a governance and development professional with expertise in project management, "
        "MIS systems, and public health initiatives. With proven experience at UNDP (United Nations Development Programme), "
        "TB Alert India, and CPLI, Gagandeep brings strong technical and organizational skills to roles that drive social impact. "
        "Holds MCA (2016) and BCA (2013) degrees from Punjabi University, Patiala."
    ),

    "experience": [
        {
            "role": "U-WIN Coordinator",
            "org": "United Nations Development Programme (UNDP), Patiala",
            "highlights": "Coordinated vaccine distribution and immunization programmes under U-WIN initiative; Managed cold chain logistics to ensure safe storage and delivery; Oversaw data collection and reporting through MIS systems to strengthen programme monitoring.",
            "tags": "Vaccination, Data monitoring, Supply chain, Public health"
        },
        {
            "role": "Vaccine & Cold Chain Manager",
            "org": "United Nations Development Programme (UNDP), Tarn Taran",
            "highlights": "Supervised vaccine supply chain operations across the district; Ensured compliance with WHO and national standards for cold chain management; Trained health workers on vaccine handling and reporting protocols.",
            "tags": "Cold chain, Logistics, Healthcare, Training"
        },
        {
            "role": "MIS Assistant",
            "org": "TB Alert India, Patiala",
            "highlights": "Supported tuberculosis control programmes through MIS data entry and analysis; Assisted in monitoring patient treatment adherence and programme outcomes; Prepared reports for district-level health authorities.",
            "tags": "MIS, Data, Reporting, Public Health"
        },
        {
            "role": "Trainer & Counsellor",
            "org": "CPLI, Ludhiana",
            "highlights": "Conducted counselling and mentoring sessions for students; Delivered training on career guidance, soft skills, and personal development; Facilitated workshops to enhance student engagement and confidence.",
            "tags": "Training, Counselling, Mentoring, Communication"
        },
        {
            "role": "Computer Operator & Office Executive",
            "org": "SD Public Senior Secondary School, Sangrur",
            "highlights": "Managed administrative tasks including documentation, record-keeping, and office coordination; Provided IT support for school operations and digital record systems; Assisted in organizing academic and extracurricular activities.",
            "tags": "Administration, IT Support, Documentation, Coordination"
        }
    ],

    "skills": {
        "Project Management": ["Project Management", "Public Health Program Management", "Programme Coordination", "Monitoring & Reporting", "Training & Counselling"],
        "Data & Business Tools": ["MIS & Data Analysis", "Advanced Excel (XLOOKUP, INDEX/MATCH, Pivot Tables)", "MS Office Suite", "Data Reporting", "Dashboard Development"],
        "Technology & AI": ["Python", "SQL Relational Databases", "AI & Machine Learning", "LangChain LLM Orchestration", "AI Development"],
        "Digital Marketing": ["Google Ads", "PPC Campaigns", "Keyword Research", "Search Campaign Planning", "Campaign Optimization"],
        "Creative": ["Visual Communication", "Logo Making", "Digital Design"]
    },

    "services": [
        "Project Management: coordination, programme monitoring, documentation, reporting, organizational support",
        "MIS & Data Analysis: data organization, validation, analysis, periodic reporting, dashboard solutions",
        "Advanced Excel: spreadsheets, reporting systems, dashboards, complex formulas, structured data modeling",
        "Google Ads / PPC: Google Search Ads planning, keyword research, ad concepts, conversion tracking, optimization",
        "AI & Machine Learning: Python solutions, machine-learning concepts, AI workflow exploration",
        "Python & SQL: automated data processing, SQL database design, complex querying, analytical solutions",
        "LangChain & AI Applications: LLM orchestration, RAG document search, prompt pipelines",
        "Visual Communication & Logo Design: professional visual concepts, communication materials, logo design"
    ],

    "projects": [
        {
            "name": "Google Ads Lead Generation Campaign",
            "badge": "DEMO / SAMPLE PROJECT",
            "description": "Sample Google Search Ads campaign planning for local home services (Plumbing, Heating, Installation) targeting high-intent search queries with negative match lists, conversion tracking, and CPC optimization.",
            "note": "Demo project — campaign structure and data are for portfolio demonstration and are not represented as actual client results."
        },
        {
            "name": "Public Health MIS Dashboard",
            "badge": "SAMPLE / DEMONSTRATION DASHBOARD",
            "description": "Fictional demonstration dashboard showing programme indicators, monthly activity, geographic summaries, and operational trends for health programs.",
            "note": "Sample dashboard — fictional figures do not represent real programme outcomes."
        },
        {
            "name": "Advanced Excel Data Analysis",
            "badge": "SAMPLE DATASET",
            "description": "Spreadsheet engineering, data cleansing, XLOOKUP/INDEX-MATCH formulas, Pivot Tables, dynamic charts, and summary audit reports."
        },
        {
            "name": "AI & Python Processing Pipeline",
            "badge": "PERSONAL / DEMONSTRATION PROJECT",
            "description": "Workflow: Data → Python → AI Model (LangChain) → Analysis → Output. Demonstrates automated data extraction and LLM orchestration."
        },
        {
            "name": "Healthcare Schema & SQL Query Suite",
            "badge": "SAMPLE SQL PROJECT",
            "description": "3NF relational schema, multi-table JOINs, conditional aggregations, and district compliance tracking."
        },
        {
            "name": "Visual Communication & Logo Design",
            "badge": "CREATIVE CONCEPTS / DEMO",
            "description": "Minimalist geometric logos, brand guidelines, and executive presentation graphics."
        }
    ],

    "education": [
        {"degree": "MCA (Master of Computer Applications)", "institution": "Punjabi University, Patiala", "year": "2016"},
        {"degree": "BCA (Bachelor of Computer Applications)", "institution": "Punjabi University, Patiala", "year": "2013"}
    ]
}

# LangChain Prompt Template
CONVERSATION_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["history", "question", "context"],
    template="""You are the AI Assistant for Gagandeep Kaur's professional portfolio, built using LangChain.
Your goal is to represent Gagandeep accurately, professionally, and helpfully.

Core Guidelines:
1. Speak knowledgeably about Gagandeep's real experience: UNDP (U-WIN & Cold Chain), TB Alert India, CPLI, SD Public School.
2. Emphasize her unique blend: Governance & Development + Data Analysis (MIS, Excel) + Technology & AI (Python, SQL, LangChain) + Google Ads / PPC.
3. Clearly distinguish demo/sample projects from professional experience as requested. Never invent fake client stats or employers.
4. Keep answers friendly, structured with bullet points where appropriate, and encourage starting a project or getting in touch.

Relevant Portfolio Context:
{context}

Previous Conversation:
{history}

Visitor's Message:
{question}

Response:"""
)

class LangChainPortfolioEngine:
    def __init__(self):
        self.openai_model = None
        # Check if OPENAI_API_KEY is available in environment
        openai_key = os.environ.get("OPENAI_API_KEY")
        if openai_key:
            try:
                from langchain_openai import ChatOpenAI
                self.openai_model = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")
            except Exception:
                self.openai_model = None

    def retrieve_context(self, query: str) -> str:
        """Simple keyword retrieval across knowledge base to form context."""
        q = query.lower()
        context_parts = []
        
        # Always include identity snippet
        context_parts.append(f"Profile: {PORTFOLIO_KNOWLEDGE['name']} — {PORTFOLIO_KNOWLEDGE['title']}. Location: {PORTFOLIO_KNOWLEDGE['location']}. Contact: {PORTFOLIO_KNOWLEDGE['email']}, Phone: {PORTFOLIO_KNOWLEDGE['phone']}.")
        
        # Check domain relevance
        if any(w in q for w in ["undp", "u-win", "vaccine", "cold chain", "tb alert", "experience", "work", "job", "career", "history", "cpli"]):
            exp_text = "Experience:\n" + "\n".join([f"- {e['role']} at {e['org']}: {e['highlights']}" for e in PORTFOLIO_KNOWLEDGE['experience']])
            context_parts.append(exp_text)

        if any(w in q for w in ["skill", "tool", "stack", "technology", "python", "sql", "excel", "langchain", "ai", "machine learning"]):
            skills_text = "Skills & Expertise:\n" + "\n".join([f"- {cat}: {', '.join(items)}" for cat, items in PORTFOLIO_KNOWLEDGE['skills'].items()])
            context_parts.append(skills_text)

        if any(w in q for w in ["service", "help", "offer", "hire", "consult", "work together"]):
            services_text = "Services Offered:\n" + "\n".join([f"- {s}" for s in PORTFOLIO_KNOWLEDGE['services']])
            context_parts.append(services_text)

        if any(w in q for w in ["project", "portfolio", "ads", "google", "dashboard", "case study"]):
            projects_text = "Projects & Case Studies:\n" + "\n".join([f"- {p['name']} ({p['badge']}): {p['description']}" for p in PORTFOLIO_KNOWLEDGE['projects']])
            context_parts.append(projects_text)

        if any(w in q for w in ["education", "degree", "university", "college", "mca", "bca"]):
            edu_text = "Education:\n" + "\n".join([f"- {ed['degree']} from {ed['institution']} ({ed['year']})" for ed in PORTFOLIO_KNOWLEDGE['education']])
            context_parts.append(edu_text)

        if any(w in q for w in ["contact", "email", "phone", "linkedin", "upwork", "reach", "call", "hire", "message"]):
            context_parts.append(f"Contact Info:\nEmail: {PORTFOLIO_KNOWLEDGE['email']}\nPhone: {PORTFOLIO_KNOWLEDGE['phone']}\nLinkedIn: {PORTFOLIO_KNOWLEDGE['linkedin']}\nUpwork: {PORTFOLIO_KNOWLEDGE['upwork']}")

        return "\n\n".join(context_parts)

    def generate_response(self, question: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate response via LangChain chain (or intelligent local fallback)."""
        if not question or not question.strip():
            return {
                "reply": "Hello! I am Gagandeep's AI conversation assistant powered by LangChain. How can I help you today? You can ask me about Gagandeep's UNDP experience, MIS & data analysis, Python/SQL, Google Ads, or AI applications.",
                "model": "LangChain v1.3.0 RAG Engine",
                "status": "success"
            }

        question_clean = question.strip()
        formatted_history = ""
        if history:
            formatted_history = "\n".join([f"{item.get('sender', 'User')}: {item.get('text', '')}" for item in history[-4:]])

        context = self.retrieve_context(question_clean)

        # 1. If OpenAI LLM is available, invoke the chain
        if self.openai_model:
            try:
                chain = CONVERSATION_PROMPT_TEMPLATE | self.openai_model | StrOutputParser()
                reply = chain.invoke({
                    "history": formatted_history,
                    "question": question_clean,
                    "context": context
                })
                return {
                    "reply": reply,
                    "model": "LangChain + OpenAI Chat",
                    "status": "success"
                }
            except Exception as e:
                pass  # Fallback to local LangChain knowledge engine

        # 2. Local Intelligent LangChain Knowledge Engine
        reply = self._generate_local_response(question_clean)
        return {
            "reply": reply,
            "model": "LangChain v1.3.0 Knowledge Chain",
            "status": "success"
        }

    def _generate_local_response(self, q: str) -> str:
        ql = q.lower()

        # Greetings
        if re.search(r"^(hi|hello|hey|greetings|start)", ql):
            return (
                "👋 **Hello! Welcome to Gagandeep Kaur's Portfolio Conversation.**\n\n"
                "I am Gagandeep's AI Assistant built using **LangChain**. I can share details on:\n\n"
                "• **Governance & Development:** Experience with UNDP (U-WIN & Cold Chain) and TB Alert India\n"
                "• **Data & Analytics:** MIS systems, Advanced Excel modeling, and data pipelines\n"
                "• **Technology & AI:** Python programming, SQL databases, and LangChain applications\n"
                "• **Digital Marketing:** Google Search Ads / PPC campaign planning & lead generation\n\n"
                "What would you like to explore or discuss?"
            )

        # UNDP / Experience
        if any(w in ql for w in ["undp", "u-win", "cold chain", "vaccine", "tb alert", "experience", "background", "work"]):
            return (
                "🏛️ **Gagandeep Kaur's Professional Experience:**\n\n"
                "1. **U-WIN Coordinator — UNDP, Patiala:**\n"
                "   Coordinated district-level vaccine distribution under the digital U-WIN initiative, monitored temperature and cold chain logistics, and oversaw data collection through MIS systems.\n\n"
                "2. **Vaccine & Cold Chain Manager — UNDP, Tarn Taran:**\n"
                "   Supervised district vaccine supply chain operations, ensured adherence to WHO & national standards, and trained healthcare workers on handling protocols and digital reporting.\n\n"
                "3. **MIS Assistant — TB Alert India, Patiala:**\n"
                "   Supported tuberculosis control programmes through accurate data entry, tracked patient treatment adherence, and prepared district reports.\n\n"
                "4. **Trainer & Counsellor — CPLI, Ludhiana:**\n"
                "   Conducted career guidance, student mentorship, and soft skills training workshops.\n\n"
                "5. **Computer Operator & Office Executive — SD Public School, Sangrur:**\n"
                "   Managed administrative documentation, IT support, and digital records."
            )

        # MIS / Excel / Data
        if any(w in ql for w in ["mis", "excel", "data", "dashboard", "analysis", "pivot", "xlookup"]):
            return (
                "📊 **MIS & Data Analysis Capabilities:**\n\n"
                "Gagandeep combines field governance with strong quantitative and analytical methods:\n\n"
                "• **MIS Architecture:** Establishing standardized data collection, validation checks, and reporting pipelines for public health and institutional projects.\n"
                "• **Advanced Excel:** Deep experience with dynamic formulas (`XLOOKUP`, `INDEX-MATCH`, `SUMIFS`), multi-variable Pivot Tables, dynamic slicers, and executive dashboard design.\n"
                "• **Relational Data:** Designing normalized SQL schemas and writing multi-table JOIN and aggregation queries for program auditing."
            )

        # Google Ads / PPC
        if any(w in ql for w in ["ads", "google ads", "ppc", "keyword", "search ads", "marketing"]):
            return (
                "🎯 **Google Ads / PPC Lead Generation:**\n\n"
                "Gagandeep plans and executes structured Google Search Ads campaigns:\n\n"
                "• **High Commercial Intent:** Targeting keywords with explicit buying/service intent while scrubbing non-converting traffic via negative keyword master lists.\n"
                "• **Themed Ad Group Structure:** Tight alignment between search queries, ad copy variations, and landing pages.\n"
                "• **Conversion Focus:** Setting up conversion tracking, tracking Cost-Per-Click (CPC) and Cost-Per-Acquisition (CPA) to maximize return on ad spend.\n\n"
                "*(Note: Portfolio project is a structured demonstration for local home services).* "
            )

        # AI / LangChain / Python
        if any(w in ql for w in ["langchain", "ai", "machine learning", "python", "model", "llm", "rag"]):
            return (
                "🤖 **AI & LangChain Development:**\n\n"
                "Gagandeep actively develops and explores AI-powered solutions:\n\n"
                "• **LangChain Orchestration:** Building contextual RAG (Retrieval-Augmented Generation) pipelines, prompt chains, and agentic workflows.\n"
                "• **Python Data Engineering:** Automated data cleaning with Pandas, script-based data ingestion, and API integration.\n"
                "• **Machine Learning Concepts:** Practical model evaluation and transforming unstructured data into structured executive summaries."
            )

        # Education
        if any(w in ql for w in ["education", "degree", "university", "college", "mca", "bca", "qualification"]):
            return (
                "🎓 **Academic Credentials:**\n\n"
                "• **MCA (Master of Computer Applications)** — Punjabi University, Patiala (2016)\n"
                "• **BCA (Bachelor of Computer Applications)** — Punjabi University, Patiala (2013)\n\n"
                "Equipped with comprehensive academic training in software engineering, database design, algorithms, and information management systems."
            )

        # Contact / Hire / Collaboration
        if any(w in ql for w in ["contact", "email", "phone", "hire", "collaborate", "reach", "call", "connect", "meeting", "touch", "talk"]):
            return (
                "📬 **Let's Connect with Gagandeep Kaur:**\n\n"
                "• **Email:** [gagan9041783@gmail.com](mailto:gagan9041783@gmail.com)\n"
                "• **Phone / WhatsApp:** +91 9041783035\n"
                "• **Location:** Mohali, Punjab, India\n"
                "• **LinkedIn:** [View Profile](https://www.linkedin.com/in/gagandeepkaur25?utm_source=share_via&utm_content=profile&utm_medium=member_android)\n"
                "• **Upwork:** [View Freelance Profile](https://www.upwork.com/freelancers/~012d7b4c25524f13a6?mp_source=share)\n\n"
                "You can also use the contact form on this website to send a direct project inquiry!"
            )

        # General inquiry fallback
        return (
            f"Thank you for your question about Gagandeep Kaur's work!\n\n"
            f"Gagandeep brings a unique combination of **governance and public health leadership (UNDP)**, "
            f"**rigorous data analysis (MIS, Advanced Excel)**, and **cutting-edge technology (Python, SQL, LangChain AI, Google Ads)**.\n\n"
            f"Would you like more details on her experience, services, specific case studies, or how to get in touch?"
        )

# Singleton Instance
langchain_engine = LangChainPortfolioEngine()
