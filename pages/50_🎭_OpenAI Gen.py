def openai_generate():
    """
    Calling two apps using OpenAI's APIs
    """

    import streamlit as st

    st.write("## 🎭 OpenAI Generators")
    st.write("")

    st.write(
        """
        ##### Two apps using OpenAI's large language models are presented as follows:

        - [ChatGPT & DALL·E](https://chatgpt-dalle.streamlit.app/),
          which implements ChatGPT (with images), RAG (Retrieval Augmented
          Generation), and DALL·E using OpenAI and langchain functions.

        - [OpenAI Assistants](https://assistants.streamlit.app/),
          which enables users to create their own custom
          chatbots using the Assistants API; such tools as
          retrieval and code interpreter can be used.
        """
    )


if __name__ == "__main__":
    openai_generate()
