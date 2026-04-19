import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="CMS 17 Guardian")

with st.sidebar:
    st.title("Settings")
    api_key = st.secrets["GEMINI_KEY"]
st.title("🎓 Chicago Style 17 Guardian")

if not api_key:
    st.warning("Please enter your API Key in the sidebar.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")

        if uploaded_file and st.button("Run Audit"):
            with st.spinner("Analyzing..."):
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = "".join([page.get_text() for page in doc])
                
                prompt = f"Strict Chicago 17th Ed. Audit. Find: 1. Hyphens in page ranges (should be en-dashes). 2. Footnotes before punctuation. 3. Numbers 0-100 not spelled out. Text: {text[:8000]}"
                
                response = model.generate_content(prompt)
                st.markdown("### 📋 Results")
                st.write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
