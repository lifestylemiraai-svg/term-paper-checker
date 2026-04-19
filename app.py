import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# 1. Setup - Replace with your key or use secrets
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("🎓 The CMS 17 Guardian")
    st.info("Upload your paper. I'll find the Chicago Style errors you missed.")

    uploaded_file = st.file_uploader("Upload Term Paper (PDF)", type="pdf")

    if uploaded_file:
        # Extract text from PDF
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        if st.button("Audit My Paper"):
            with st.spinner("Analyzing minute CMS 17 details..."):
                # The specialized prompt for researchers
                prompt = f"""
                You are a professional academic editor. Analyze this text for strict adherence to Chicago Manual of Style (17th Edition).
                Focus on these minute details:
                1. En-dashes (–) for page ranges (e.g., 15–25) instead of hyphens (-).
                2. Punctuation MUST come before the footnote number (e.g., ."¹ or ,²).
                3. Spell out numbers 0-100 (e.g., 'forty-two' not '42') unless they are part of a date or decimal.
                4. Possessives for names ending in 's' (e.g., Jones's not Jones').
                5. Block quote formatting for quotes over 100 words.

                Text to analyze:
                {text[:8000]} 

                Format your response as a clear table with three columns: 
                'Original Text' | 'Suggested Fix' | 'Why (CMS 17 Rule)'
                """
                
                response = model.generate_content(prompt)
                st.markdown("### 📋 Correction List")
                st.write(response.text)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
              st.divider()
st.subheader("💡 Quick Tool: Footnote ↔ Bibliography")
cite_input = st.text_input("Paste a citation here:")
if cite_input:
    cite_prompt = f"Convert this into both a Chicago 17 Footnote and a Bibliography entry: {cite_input}"
    cite_res = model.generate_content(cite_prompt)
    st.write(cite_res.text)
