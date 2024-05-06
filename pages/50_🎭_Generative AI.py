def openai_generate():
    """
    Calling two apps using OpenAI's APIs
    """

    import streamlit as st

    st.write("## 🎭 OpenAI Generators")
    st.write("")

    st.write(
        """
        ##### Three apps using OpenAI's large language models are presented as follows:

        - [LangChain LLM Agent](https://langchain-llm-agent.streamlit.app/),
          which implements ChatGPT (with images), RAG (Retrieval Augmented
          Generation), and DALL·E using OpenAI and LangChain functions.

        - [OpenAI Assistants](https://assistants.streamlit.app/),
          which enables users to create their own custom
          chatbots using the Assistants API.

        - [Multi-Agent Debate](https://multi-agent-debate.streamlit.app/),
          which enables two agents to on a given topic. LangChain and OpenAI
          functions are employed.

        In these apps, tools such as searching the internet, ArXiv, Wikipedia,
        or uploaded documents (retrieval) can be used. Python REPL is also
        supported.
        """
    )


if __name__ == "__main__":
    openai_generate()
