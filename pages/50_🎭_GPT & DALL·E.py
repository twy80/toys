"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Mar. 2023)
"""

def redirect_to_chatgpt_dalle_app():
    # Redirects the user to the ChatGPT DALL·E application.
    import streamlit as st

    url = "https://chatgpt-dalle.streamlit.app/"
    # webbrowser.open_new_tab(url)

    page = f"""
        <meta http-equiv="refresh" content="0;URL='{url}'" />
    """
    st.markdown(page, unsafe_allow_html=True)


if __name__ㄴ== "__main__":
    redirect_to_chatgpt_dalle_app()
