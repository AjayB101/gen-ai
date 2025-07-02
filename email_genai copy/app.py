import streamlit as st

from email_generator import generate_message


st.title("📧 Smart Referral Message Generator")
st.markdown(
    "Generate professional referral request messages from job posting content")

st.markdown("### 📝 **How to use:**")
st.info("""
1. **Go to the job posting** in your browser
2. **Copy the entire job description** (Ctrl+A, then Ctrl+C)
3. **Paste it below** in the text area
4. **Click Generate** to create your referral message
""")

# Main input area
st.markdown("### 📋 **Paste Job Description Here:**")
job_content = st.text_area(
    "Job Description Content",
    height=300,
    placeholder="""Paste the complete job posting here including:
- Job Title
- Company Name  
- Job Requirements
- Job Description
- Job ID (if available)
- Any other relevant details

Example:
Software Engineer - Google
Job ID: 12345
We are looking for a Software Engineer to join our team...
Requirements: Python, JavaScript, React...
""",
    help="Copy and paste the entire job posting content from the company's website"
)

# Character count
if job_content:
    char_count = len(job_content.strip())
    st.caption(f"📊 Content length: {char_count} characters")

    if char_count < 100:
        st.warning(
            "⚠️ Content seems too short. Please paste the complete job description for better results.")
    elif char_count > 50:
        st.success("✅ Good content length detected!")

# Generate button and results
if st.button("🚀 Generate Referral Message", type="primary", use_container_width=True):
    if job_content and len(job_content.strip()) > 50:
        with st.spinner("✍️ Generating your referral message..."):
            try:
                message = generate_message(job_content)

                st.success("🎉 Referral message generated successfully!")

                st.markdown("### 📝 **Your Referral Message:**")
                st.markdown("**Copy the message below and personalize it:**")

                # Display the message in a text area for easy copying
                st.text_area(
                    "Generated Message",
                    value=message,
                    height=250,
                    key="generated_message",
                    help="Select all (Ctrl+A) and copy (Ctrl+C) this message"
                )

                # Add copy button simulation
                st.markdown(
                    "**✂️ To copy:** Click in the text area above → Press Ctrl+A → Press Ctrl+C")

            except Exception as e:
                st.error(f"❌ Error generating message: {str(e)}")
                st.markdown("**Please try:**")
                st.markdown("- Check your internet connection")
                st.markdown("- Verify your GROQ API key in the .env file")
                st.markdown(
                    "- Make sure the job content is properly formatted")
    else:
        st.error(
            "❌ Please paste the job description content (at least 50 characters)")

# Tips and instructions
st.markdown("---")
st.markdown("### 💡 **Tips for Best Results:**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✅ **Include in your paste:**")
    st.markdown("""
    - Job title
    - Company name
    - Job requirements
    - Job description
    - Job ID/Reference number
    - Location (if mentioned)
    """)

with col2:
    st.markdown("#### 🎯 **Personalization Tips:**")
    st.markdown("""
    - Replace [Name] with employee's actual name
    - Replace [Your Name] with your name
    - Add how you found their contact
    - Mention mutual connections if any
    - Keep it concise and professional
    """)

st.markdown("### 📋 **Example Job Content Format:**")
with st.expander("View Example", expanded=False):
    st.code("""
Software Engineer - Meta
Job ID: SWE-2024-001
Location: Menlo Park, CA

We are seeking a talented Software Engineer to join our team...

Requirements:
- Bachelor's degree in Computer Science
- 3+ years of experience with Python, JavaScript
- Experience with React, Node.js
- Strong problem-solving skills

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, efficient code
""", language="text")

st.markdown("### ❓ **Troubleshooting:**")
with st.expander("Common Issues", expanded=False):
    st.markdown("""
    **Message not generating?**
    - Check if you have a valid GROQ API key in your .env file
    - Ensure the content is substantial (more than 50 characters)
    - Try refreshing the page if it's stuck
    
    **Poor message quality?**
    - Include more details from the job posting
    - Make sure job title and company name are clearly mentioned
    - Include key requirements and responsibilities
    
    **Can't copy the message?**
    - Click inside the message text area
    - Press Ctrl+A to select all
    - Press Ctrl+C to copy
    - Or manually select and right-click → Copy
    """)
