"""
Chatting with GPT using openai API (by T.-W. Yoon, Jan. 2023)
"""

import openai
import streamlit as st


initial_prompt = """
The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.

**Human:** Hello, who are you?

**AI:** I am an AI created by OpenAI. How can I help you today?
"""


def openai_create(restart_sequence, user_prompt, temperature=0.8, max_token=200):
    if user_prompt == "" or st.session_state.new_conversation:
        return None

    human_enq = restart_sequence + user_prompt
    try:
        with st.spinner("AI is thinking..."):
            response = openai.Completion.create(
                model="text-davinci-003",
                # model="text-curie-001",
                prompt=initial_prompt + st.session_state.prompt + human_enq,
                temperature=temperature,
                max_tokens=max_token,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[" **Human:**", " **AI:**"]
            )
        generated_text = response.choices[0].text+"\n"
    except openai.error.OpenAIError as e:
        generated_text = None
        st.error(f"An error occurred: {e}", icon="🚨")

    if generated_text:
        st.session_state.prompt += human_enq + generated_text
        st.session_state.generated_text = generated_text

    return None


def reset_conversation():
    # import clipboard
    # clipboard.copy(f"{st.session_state.prompt}\n")

    st.session_state.new_conversation = True
    st.session_state.generated_text = None
    st.session_state.prompt = ""
    st.session_state.human_enq = []
    st.session_state.ai_resp = []


def chat_gpt():
    # import os
    # from streamlit_chat import message

    st.write("## :computer: OpenAI Chat")
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.api_key = st.text_input(
    #    label="$\\hspace{0.25em}\\texttt{Your OpenAI API Key}$",
    #    on_change=reset_conversation
    # )
    # st.write("(You can obtain an API key from https://beta.openai.com.)")

    # start_sequence = "\n**AI:** "
    restart_sequence = "\n**Human:** "

    if "generated_text" not in st.session_state:
        st.session_state.generated_text = None

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    if "human_enq" not in st.session_state:
        st.session_state.human_enq = []

    if "ai_resp" not in st.session_state:
        st.session_state.ai_resp = []

    st.write("#### Conversation with AI")

    for (human, ai) in zip(st.session_state.human_enq, st.session_state.ai_resp):
        st.write(human)
        st.write(ai)

    # Get the code description from the user
    user_input = st.text_area(
        label="$\\hspace{0.08em}\\texttt{Human}$",
        value="",
        label_visibility="visible"
    )

    user_input_stripped = user_input.strip()

    left, right = st.columns(2) # To show the results below the button
    left.button(
        label="Send",
        on_click=openai_create(restart_sequence, user_input_stripped),
    )
    right.button(
        label="Reset",
        on_click=reset_conversation
    )

    if st.session_state.generated_text and user_input_stripped != "":
        st.write(st.session_state.generated_text)
        st.session_state.human_enq.append(restart_sequence + user_input_stripped)
        st.session_state.ai_resp.append(st.session_state.generated_text)

        # for i in range(len(st.session_state.ai_resp)-1, -1, -1):
        #    message(st.session_state.ai_resp[i].strip(), key=str(i))
        #    message(st.session_state.human_enq[i], is_user=True, key=str(i) + '_user')

    st.session_state.new_conversation = False


if __name__ == "__main__":
    chat_gpt()
