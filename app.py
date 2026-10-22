import streamlit as st
import pdfplumber
from google import genai

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.markdown("### Powered by Gemini AI")

# --- APNI GEMINI API KEY YAHAN EK HI BAAR PASTE KAR DE ---
API_KEY = "AQ.Ab8RN6IMHIBQbi7Yu7nveKIdKWGQFT3heVAH-isXwbSIWWCDlw"

# Initialize session state for resume text
if 'resume_text' not in st.session_state:
    st.session_state['resume_text'] = ""

# Layout: Two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Candidate Resume")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"], key="resume_uploader")
    
    if uploaded_file is not None:
        try:
            with pdfplumber.open(uploaded_file) as pdf:
                text_data = ""
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_data += t + "\n"
            if text_data.strip():
                st.session_state['resume_text'] = text_data
        except Exception as e:
            st.error(f"PDF read error: {e}")

with col2:
    st.subheader("2. Enter Job Description")
    job_description = st.text_area("Paste the job description here...", height=150, key="jd_input")

# Editable Resume Text Area
st.subheader("📝 Candidate Resume Content")
st.session_state['resume_text'] = st.text_area(
    "Resume text will appear here automatically after uploading PDF (You can also edit or paste directly):", 
    value=st.session_state['resume_text'], 
    height=200
)

# Analyze Button
if st.button("🚀 Analyze Resume with AI", type="primary"):
  if not st.session_state.get("resume_text", "").strip():
    st.warning("Pehle koi resume upload karo ya text paste karo bhai!")
  elif not job_description.strip():
    st.warning("Pehle Job Description toh daalo!")
  else:
    with st.spinner("AI is analyzing the resume against the job description..."):
      try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=API_KEY)
                
        prompt = f"""
                You are an expert HR recruiter and ATS system. Analyze the following candidate resume against the provided job description.
                
                Job Description:
                {job_description}
                
                Candidate Resume:
                {st.session_state['resume_text']}
                
                Provide a detailed evaluation containing:
                1. Match Score out of 10
                2. Key Strengths of the candidate regarding this role
                3. Missing Skills or Weaknesses
                4. Final Recommendation (Shortlist / Reject with reasoning)
                """
                
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
                st.success("Analysis Complete!")
                st.markdown("### 📊 AI Evaluation Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error aa gaya bhai: {e}")


# ================= AI RESUME BUILDER (UPDATED CODE) =================

st.markdown("\n")
st.divider()
st.header("✍️ AI Resume Generator & Builder")
st.markdown("Apna naam, target role aur details yahan daalo, aur AI tere liye ekdum professional aur ATS-ready resume bana kar dega!")

col_b1, col_b2 = st.columns(2)
with col_b1:
    builder_name = st.text_input("Full Name", placeholder="Apna pura naam yahan likho...", key="b_name_empty")
with col_b2:
    builder_role = st.text_input("Target Job Title", placeholder="Jaise: Software Developer, Data Analyst...", key="b_role_empty")

builder_details = st.text_area(
    "Apni experience, skills, projects aur education ke baare me yahan points me likho:",
    height=180,
    placeholder="Jaise: 10th, 12th percentage, B.Tech CSE, skills, projects, hackathons...",
    key="b_details_empty"
)

if st.button("🚀 Generate Professional Resume with AI", type="primary", key="generate_resume_btn_custom"):
    if not API_KEY.strip():
        st.warning("Bhai, code ke andar `API_KEY` me apni key toh daal!")
    elif not builder_name.strip():
        st.warning("Pehle apna naam toh daal bhai!")
    elif not builder_role.strip():
        st.warning("Pehle Target Job Title toh daal bhai!")
    elif not builder_details.strip():
        st.warning("Pehle apni details ya background toh likh bhai!")
    else:
        with st.spinner("AI is crafting your professional resume..."):
            try:
                client = genai.Client(api_key=API_KEY.strip())
                build_prompt = f"""
                You are an expert professional resume writer and ATS optimization specialist. 
                Create a well-structured, highly professional, and ATS-friendly resume based on the following candidate information:
                
                Name: {builder_name}
                Target Role: {builder_role}
                Candidate Background & Details: {builder_details}
                
                Format the resume cleanly using standard headings: Professional Summary, Core Skills, Education, Projects, and Personal Details. Make it look neat and impactful using Markdown.
                """
                
                build_response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=build_prompt
                )
                
                st.success("Resume Generated Successfully!")
                st.markdown("### 📄 Your AI-Generated Professional Resume")
                st.markdown(build_response.text)
                st.session_state['generated_resume'] = build_response.text
                
            except Exception as f:
                st.error(f"Error aa gaya bhai: {f}")

if 'generated_resume' in st.session_state and st.session_state['generated_resume']:
    file_prefix = builder_name.replace(' ', '_') if builder_name.strip() else "Candidate"
    st.download_button(
        label="📥 Download Generated Resume (.txt)",
        data=st.session_state['generated_resume'],
        file_name=f"{file_prefix}_Resume.txt",
        mime="text/plain",
        key="download_gen_resume_custom"
    )
