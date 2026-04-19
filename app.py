import streamlit as st
import fitz
import google.generativeai as genai

st.set_page_config(page_title="CMS 17 Guardian", layout="centered")

with st.sidebar:
    st.title("Settings")
    # Tell them exactly where to get the key
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get a free key at aistudio.google.com")

st.title("🎓 Chicago Style 17 Guardian")

if not api_key:
    st.warning("Please enter your API Key in the sidebar to begin.")
else:
    try:
        # This configuration is more robust
        genai.configure(api_key=api_key)
        
        # We are using the most basic name to avoid 404s
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("Upload your PDF paper", type="pdf")

        if uploaded_file:
            if st.button("Run 10x Audit"):
                with st.spinner("Checking minute details..."):
                    # Mobile-optimized byte reading
                    file_bytes = uploaded_file.read()
                    doc = fitz.open(stream=file_bytes, filetype="pdf")
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    
                    if not text.strip():
                        st.error("Could not read text from PDF. Is it an image scan?")
                    else:
                        # Only send the first 10,000 characters to ensure it stays free/fast
                        short_text = text[:10000] 
                        
                        prompt = f"""
                        Act as a strict Chicago Manual of Style (17th Ed.) editor. 
                        Provide a table of errors found in this text regarding:
                        1. En-dashes (–) vs Hyphens (-) for page/date ranges.
                        2. Footnote numbers (must follow punctuation).
                        3. Numbers 0-100 (must be spelled out).
                        4. Punctuation in Bibliography vs Footnotes.
                        
                        Text: {short_text}
                        """
                        
                        response = model.generate_content(prompt)
                        st.markdown("### 📋 CMS 17 Audit Results")
                        st.write(response.text)
                    
    except Exception as e:
        st.error(f"Setup Error: {e}")
        st.info("Check if your API Key is correct and 'Generative Language API' is enabled in AI Studio.")

st.divider()
                    st.markdown("### 📋 Results")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Connection Error: {e}")

st.divider()
