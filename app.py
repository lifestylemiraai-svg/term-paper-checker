import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="CMS 17 Guardian", layout="centered")

with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at aistudio.google.com")

st.title("🎓 Chicago Style 17 Guardian")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
else:
    try:
        genai.configure(api_key=api_key)
        # CHANGED: Added 'models/' prefix which is more stable
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("Upload your PDF paper", type="pdf")

        if uploaded_file:
            if st.button("Run 10x Audit"):
                with st.spinner("Analyzing..."):
                    # Extract text
                    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                        text = "".join([page.get_text() for page in doc])
                    
                    # Limit text to avoid 'token' errors for long papers
                    short_text = text[:8000] 
                    
                    prompt = f"Act as a CMS 17 editor. Find: 1. Hyphens instead of En-dashes (–) in ranges. 2. Footnote numbers before punctuation. 3. Numbers 0-100 not spelled out. Text: {short_text}"
                    
                    response = model.generate_content(prompt)
                    st.markdown("### 📋 Results")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Connection Error: {e}")

st.divider()
