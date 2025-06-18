import streamlit as st
from extract_jd import extract_job_details
from chroma_setup import get_top_links, setup_chroma_if_needed
from email_generator import generate_email

st.title("📧 Smart Cold Email Generator for JD")

url = st.text_input("Enter Job Description URL:")

if url:
    with st.spinner("🔍 Extracting job description..."):
        job_desc = extract_job_details(url)

    st.subheader("📄 Extracted JD")
    st.markdown(job_desc)

    with st.spinner("📌 Matching your portfolio..."):
        setup_chroma_if_needed()
        jd_data = extract_job_details(url, return_json=True)
        top_links = get_top_links(jd_data["skills"])

    with st.spinner("✍️ Generating cold email..."):
        email = generate_email(job_desc, top_links)
        st.markdown(email, unsafe_allow_html=True)