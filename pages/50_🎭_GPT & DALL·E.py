"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Mar. 2023)
"""

def redirect_to_chatgpt_dalle_app():
    # Redirects the user to the ChatGPT DALL·E application.
    import streamlit as st

    st.set_option('server.max_redirects', 1)
    url = "https://chatgpt-dalle.streamlit.app/"
    html_script = f"""
        <script type="text/javascript">
            window.open('{url}', '_blank').focus();
        </script>
    """
    st.html(html_script)


if __name__ == "__main__":
    redirect_to_chatgpt_dalle_app()
