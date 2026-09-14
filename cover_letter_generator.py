# cover_letter_generator.py

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate


# ────────────────────────────────────────────────
# Load Environment Variables
# ────────────────────────────────────────────────

load_dotenv()


# ────────────────────────────────────────────────
# API Key
# ────────────────────────────────────────────────

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        GROQ_API_KEY = None


# ────────────────────────────────────────────────
# LLM
# ────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def get_llm():

    return ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0.3
    )


# ────────────────────────────────────────────────
# Prompt
# ────────────────────────────────────────────────

COVER_LETTER_PROMPT = PromptTemplate.from_template(
    """
Write a professional, compelling cover letter (300–450 words)
tailored specifically to the job description below.

Emphasize the candidate's most relevant experience, skills,
achievements and qualifications that directly match or exceed
the job requirements.

Use concrete examples from the resume where possible.

Show enthusiasm for the role and company without fabricating
information.

Structure the letter in standard business format:

- Header (date, employer's contact if known, or just salutation)

- Opening paragraph:
  State the position and briefly explain why the candidate is
  a strong fit.

- 1–2 body paragraphs:
  Highlight the strongest matching qualifications with evidence.

- Closing paragraph:
  Reiterate interest, include a call to action, and thank the employer.

Job Description:

{job_description}


Candidate's Resume:

{resume_text}


IMPORTANT:

Do not invent any experience, skills, achievements,
qualifications, or facts not present in the resume.

Generate only the cover letter.
"""
)


# ────────────────────────────────────────────────
# Streamlit Page Config
# ────────────────────────────────────────────────

st.set_page_config(
    page_title="Cover Letter Generator | Resume Genie",
    page_icon="✉️",
    layout="wide"
)


# ────────────────────────────────────────────────
# UI
# ────────────────────────────────────────────────

st.title("✉️ Cover Letter Generator")

st.markdown(
    """
    Upload your resume and paste the job description to generate
    a personalized AI-powered cover letter.
    """
)


# ────────────────────────────────────────────────
# API Key Check
# ────────────────────────────────────────────────

if not GROQ_API_KEY:

    st.error(
        "GROQ_API_KEY not found. "
        "Please add it to your .env file."
    )

    st.stop()


# Initialize LLM

llm = get_llm()


# ────────────────────────────────────────────────
# Layout
# ────────────────────────────────────────────────

col1, col2 = st.columns([5, 5])


# ────────────────────────────────────────────────
# Job Description
# ────────────────────────────────────────────────

with col1:

    st.subheader("Job Description")

    job_desc = st.text_area(
        "Paste the full job description here...",
        height=380,
        placeholder="""
Responsibilities:
• Build AI and Machine Learning applications
• Develop Generative AI solutions
• Work with Python and LLMs
        """,
        key="job_desc_input"
    )


# ────────────────────────────────────────────────
# Resume Upload
# ────────────────────────────────────────────────

with col2:

    st.subheader("Your Resume (PDF)")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"],
        accept_multiple_files=False,
        help="Only PDF files are supported."
    )


    generate_clicked = st.button(
        "✨ Generate Cover Letter",
        type="primary",
        disabled=not (
            uploaded_file
            and job_desc.strip()
        )
    )


# ────────────────────────────────────────────────
# Generate Cover Letter
# ────────────────────────────────────────────────

if generate_clicked:

    if not uploaded_file:

        st.warning(
            "Please upload your resume PDF."
        )


    elif not job_desc.strip():

        st.warning(
            "Please paste the job description."
        )


    else:

        tmp_path = None

        try:

            # ────────────────────────────────
            # Extract Resume Text
            # ────────────────────────────────

            with st.spinner(
                "Extracting resume text..."
            ):

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp:

                    tmp.write(
                        uploaded_file.getvalue()
                    )

                    tmp_path = tmp.name


                loader = PyPDFLoader(
                    tmp_path
                )


                documents = loader.load()


                resume_text = "\n\n".join(

                    doc.page_content

                    for doc in documents

                )


                if not resume_text.strip():

                    st.error(
                        "No readable text was extracted "
                        "from the PDF."
                    )

                    st.stop()


            # ────────────────────────────────
            # Generate Cover Letter
            # ────────────────────────────────

            with st.spinner(
                "Generating your cover letter..."
            ):

                chain = COVER_LETTER_PROMPT | llm


                response_container = st.empty()


                full_response = ""


                for chunk in chain.stream({

                    "job_description": job_desc,

                    "resume_text": resume_text

                }):


                    content = (

                        chunk.content

                        if hasattr(
                            chunk,
                            "content"
                        )

                        else str(chunk)

                    )


                    full_response += content


                    response_container.markdown(
                        full_response + "▌"
                    )


                response_container.markdown(
                    full_response
                )


            # ────────────────────────────────
            # Success
            # ────────────────────────────────

            st.success(
                "✅ Cover letter generated successfully!"
            )


            # ────────────────────────────────
            # Download Button
            # ────────────────────────────────

            st.download_button(

                label="⬇️ Download Cover Letter",

                data=full_response,

                file_name="Cover_Letter.md",

                mime="text/markdown"

            )


        except Exception as e:

            st.error(
                "Generation failed."
            )

            st.exception(e)


        finally:

            # Delete temporary file

            if (

                tmp_path

                and os.path.exists(tmp_path)

            ):

                os.unlink(tmp_path)


# ────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────

st.markdown("---")

st.caption(
    "🧞 Resume Genie • Powered by Groq + LangChain"
)