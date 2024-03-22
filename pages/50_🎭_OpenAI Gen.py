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

        - [LangChain OpenAI Agent](https://langchain-openai-agent.streamlit.app/),
          which implements ChatGPT (with images), RAG (Retrieval Augmented
          Generation), and DALL·E using OpenAI and LangChain functions.
          Internet search is also supported by Tavily Sesrch.

        - [OpenAI Assistants](https://assistants.streamlit.app/),
          which enables users to create their own custom
          chatbots using the Assistants API; such tools as
          retrieval, code interpreter, and Tavily Search can be used.
        """
    )


if __name__ == "__main__":
    openai_generate()
