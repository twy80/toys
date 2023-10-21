"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Mar. 2023)
"""

def redirect_to_chatgpt_dalle_app():
    # Redirects the user to the ChatGPT DALL·E application.
    import streamlit as st
    import time

    url = "https://chatgpt-dalle.streamlit.app/"
    time.sleep(1)  # Optional delay for visualization purposes
 
    st.markdown(
        f'<meta http-equiv="refresh" content="0;URL={url}">',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    redirect_to_chatgpt_dalle_app()
