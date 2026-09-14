# app.py

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate


# ───────────────────────────────────────────────
# Config
# ───────────────────────────────────────────────

st.set_page_config(
    page_title="Resume Genie",
    layout="wide"
)

load_dotenv()


# ───────────────────────────────────────────────
# API Key
# ───────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        GROQ_API_KEY = None


if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY not found. "
        "Please set it in your .env file or Streamlit secrets."
    )
    st.stop()


# ───────────────────────────────────────────────
# LLM
# ───────────────────────────────────────────────

@st.cache_resource(
    show_spinner="Initializing AI model..."
)
def get_llm():

    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0.1
    )


llm = get_llm()


# ───────────────────────────────────────────────
# Prompt
# ───────────────────────────────────────────────

EVAL_PROMPT = """
You are an advanced resume evaluation assistant.

Analyze the provided resume text and score it out of 100 based on the following criteria:

- Clarity
- Relevance
- Format
- Comprehensiveness
- Keywords and ATS-friendliness

Your response MUST follow this exact structure:

1. **Score**: X/100

2. **Strengths**:
   • Point one
   • Point two
   • Point three

3. **Weaknesses / Areas for Improvement**:
   • Point one
   • Point two
   • Point three

4. **Skills Explicitly Mentioned**:
   • Skill 1
   • Skill 2
   • Skill 3

5. **Recommended Additional Skills**:
   Suggest skills that could make the resume stronger,
   more ATS-friendly, and future-ready.

   • Suggestion 1
   • Suggestion 2
   • Suggestion 3

6. **Suggested Next Career Steps / Roles**:
   • Realistic next role 1
   • Realistic next role 2
   • Longer-term career direction

Be specific, honest, constructive, and professional.

IMPORTANT:
Analyze only the resume text provided below.
Do not ask the user to upload or provide the resume again.

RESUME TEXT:

{context}
"""


prompt_template = PromptTemplate(
    input_variables=["context"],
    template=EVAL_PROMPT
)


# ───────────────────────────────────────────────
# UI
# ───────────────────────────────────────────────

st.title("🧞 Resume Genie")

st.markdown(
    """
    ### Your AI-Powered Career Assistant

    Upload your resume and receive an AI-powered evaluation,
    ATS-friendly score, strengths, weaknesses, skill suggestions,
    and career recommendations.
    """
)


col1, col2 = st.columns([3, 2])


with col1:

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"],
        accept_multiple_files=False,
        help="Only PDF files are currently supported"
    )


    evaluate_button = st.button(
        "✨ Evaluate Resume",
        type="primary",
        disabled=not uploaded_file
    )


# ───────────────────────────────────────────────
# Resume Evaluation
# ───────────────────────────────────────────────

if evaluate_button and uploaded_file:

    with st.spinner(
        "Reading PDF... Extracting text... Analyzing your resume..."
    ):

        tmp_path = None

        try:

            # Save uploaded file temporarily

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getvalue()
                )

                tmp_path = tmp_file.name


            # Load PDF

            loader = PyPDFLoader(
                tmp_path
            )


            documents = loader.load()


            # Extract text

            context = "\n\n".join(

                doc.page_content

                for doc in documents

            )


            # Check extracted text

            if not context.strip():

                st.error(
                    "No readable text was extracted from the PDF."
                )

                st.stop()


            # Create LangChain chain

            chain = prompt_template | llm


            # Invoke Groq model

            response = chain.invoke(

                {
                    "context": context
                }

            )


            # ───────────────────────────────────
            # Output
            # ───────────────────────────────────

            st.subheader(
                "📊 Resume Evaluation Result"
            )


            st.markdown(
                response.content
            )


        except Exception as e:

            st.error(
                "An error occurred during processing."
            )

            st.exception(e)


        finally:

            # Delete temporary PDF

            if tmp_path and os.path.exists(tmp_path):

                os.unlink(tmp_path)


# ───────────────────────────────────────────────
# Footer
# ───────────────────────────────────────────────

st.markdown("---")

st.caption(
    "🧞 Resume Genie • Built with Streamlit + LangChain + Groq"
)