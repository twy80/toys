def generative_ai():
    """
    Calling two apps using OpenAI's APIs
    """

    import streamlit as st

    st.write("## 🎭 Generative AI")
    st.write("")

    st.write(
        """
        ##### Three apps using large language models (LLMs) such as GPT-4o and Gemini-flash are presented as follows:

        - [LangChain LLM Agent](https://langchain-llm-agent.streamlit.app/),
          which implements agents using LangChain. GPT models from OpenAI or Gemini models
          from Google can be used together with tools.

        - [OpenAI Assistants](https://assistants.streamlit.app/),
          which enables users to create their own custom
          chatbots using the Assistants API from OpenAI.

        - [Multi-Agent Debate](https://multi-agent-debate.streamlit.app/),
          which enables two agents to debate on a given topic. GPT-4o from OpenAI
          is employed using LangChain.

        In these apps, tools such as searching the internet, ArXiv, Wikipedia,
        or uploaded documents (retrieval) can be used. Python REPL is also
        supported.
        """
    )


if __name__ == "__main__":
    generative_ai()
