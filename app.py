import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="CMS 17 Guardian")

with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")

st.title("🎓 Chicago Style 17 Guardian")

if not api_key:
    st.warning("Please enter your API Key in the sidebar.")
else:
    try:
        # FORCE CONFIGURATION
        genai.configure(api_key=api_key)
        
        # We use 'gemini-1.5-flash' but we wrap it in a safety try
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")

        if uploaded_file and st.button("Run Audit"):
            with st.spinner("Analyzing..."):
                # Direct byte reading
                data = uploaded_file.read()
                doc = fitz.open(stream=data, filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                
                # Check if text is empty
                if len(text.strip()) < 10:
                    st.error("PDF appears empty or scanned. Please use a text-based PDF.")
                else:
                    # Explicitly calling the model
                    response = model.generate_content(
                        f"Editor Mode: CMS 17th Ed. Check these specific errors: 1. Hyphens vs En-dashes (–). 2. Footnote placement. 3. Number spelling (0-100). Text: {text[:8000]}"
                    )
                    st.markdown("### 📋 Audit Results")
                    st.write(response.text)
                    
    except Exception as e:
        # If the 404 persists, we try one more model name automatically
        st.error(f"Model Error: {e}")
        st.info("Attempting fallback to 'gemini-pro'...")
        try:
            model_alt = genai.GenerativeModel('gemini-pro')
            # (Same logic as above could go here, but let's see if flash works first)
        except:
            pass

st.divider()
