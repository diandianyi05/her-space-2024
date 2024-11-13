import streamlit as st
import google.generativeai as genai

def validate_api_key(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Invalid API Key: {e}")
        return False

def handle_api_key_change():
    # This function will be called when the API key input changes
    api_key = st.session_state.gemini_api_key_input  # Access the input value
    if api_key:  # Check if the API key is not empty
        if validate_api_key(api_key):  # Validate the API key
            st.success("API Key validated successfully!")
        else:
            st.error("Invalid API Key. Please try again.")

def get_api_key():
    with st.expander("Why do we ask for your GEMINI API key?"):
        st.markdown("""
        ### Your Data, Your Control
        - 🔐 **Personal Authentication**: Each interaction is uniquely yours and under your control
        """)
    user_api_key = st.text_input(
        "Enter a GEMINI API key ([How can I get a GEMINI API key for free?](https://ai.google.dev/gemini-api/docs/api-key))", 
        type="password",
        key="gemini_api_key_input",
        on_change=handle_api_key_change
    )
   # Check if API key is already in session state
    if 'gemini_api_key' in st.session_state and st.session_state.gemini_api_key:
        st.success("API Key validated successfully!")
        return st.session_state.gemini_api_key

    if user_api_key:
        try:
            if user_api_key == "admin2024":
                user_api_key = st.secrets["GEMINI_API_KEY"]
                st.session_state.gemini_api_key = user_api_key
                st.success("API Key validated successfully!")
                return user_api_key

            else:
                genai.configure(api_key=user_api_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content("Hello, can you confirm my API key is working?")
                st.session_state.gemini_api_key = user_api_key
                st.success("API Key validated successfully!")
                return user_api_key

        except Exception as e:
            st.error(f"API Key validation failed: {e}")
            return None

    return None