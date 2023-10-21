"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Mar. 2023)
"""

def redirect_to_chatgpt_calle_app():
    # Redirects the user to the ChatGPT DALL·E application.
    import streamlit as st

    url = "https://chatgpt-dalle.streamlit.app/"
    # time.sleep(2)  # Optional delay for visualization purposes
 
    st.markdown(
        f'<meta http-equiv="refresh" content="0;URL={url}">',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    redirect_to_chatgpt_calle_app()
