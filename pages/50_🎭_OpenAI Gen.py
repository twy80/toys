"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Mar. 2023)
"""

import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
# import clipboard


openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = st.text_input(
#    label="$\\hspace{0.25em}\\texttt{Your OpenAI API Key}$",
#    on_change=reset_conversation
# )
# st.write("(You can obtain an API key from https://beta.openai.com.)")

# initial prompt for gpt3.5
initial_prompt = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def openai_create_text(user_prompt, temperature=0.7):
    """
    This function generates text based on user input.
    Args:
        user_prompt (string): User input
        temperature (float): Value between 0 and 1. Defaults to 0.7.

    The results are stored in st.session_state variables.
    """

    if user_prompt == "" or st.session_state.ignore_this:
        return None

    # Add the user input to the prompt
    st.session_state.prompt.append(
        {"role": "user", "content": user_prompt}
    )

    try:
        with st.spinner("AI is thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.prompt,
                temperature=temperature,
                # max_tokens=4096,
                # top_p=1,
                # frequency_penalty=0,
                # presence_penalty=0.6,
            )
        generated_text = response.choices[0].message.content
    except openai.error.OpenAIError as e:
        generated_text = None
        st.error(f"An error occurred: {e}", icon="🚨")

    if generated_text:
        # Add the generated output to the prompt
        st.session_state.prompt.append(
            {"role": "assistant", "content": generated_text}
        )
        st.session_state.generated_text = generated_text

    return None


def openai_create_image(description):
    """
    This function generates image based on user description.
    Args:
        description (string): User description

    The resulting image is plotted.
    """

    if description.strip() == "":
        return None

    try:
        with st.spinner("AI is generating..."):
            response = openai.Image.create(
                prompt=description,
                n=1,
                size="1024x1024"
            )
        image_url = response['data'][0]['url']
        st.image(
            image=image_url,
            use_column_width=True
        )
    except openai.error.OpenAIError as e:
        st.error(f"An error occurred: {e}", icon="🚨")

    return None


def reset_conversation():
    # to_clipboard = ""
    # for (human, ai) in zip(st.session_state.human_enq, st.session_state.ai_resp):
    #    to_clipboard += "\nHuman: " + human + "\n"
    #    to_clipboard += "\nAI: " + ai + "\n"
    # clipboard.copy(to_clipboard)

    st.session_state.ignore_this = True
    st.session_state.generated_text = None
    st.session_state.prompt = initial_prompt
    st.session_state.human_enq = []
    st.session_state.ai_resp = []
    st.session_state.initial_temp = 0.7


def reset_initial_temp():
    st.session_state.initial_temp = st.session_state.temp_value


def ignore_this():
    st.session_state.ignore_this = True


def create_text():
    """
    This function geneates text based on user input
    by calling openai_create_text().
    """

    # from streamlit_chat import message
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = None

    if "prompt" not in st.session_state:
        st.session_state.prompt = initial_prompt

    if "human_enq" not in st.session_state:
        st.session_state.human_enq = []

    if "ai_resp" not in st.session_state:
        st.session_state.ai_resp = []

    # Prevent the previous prompt from going into the new prompt while updating the screen
    if "ignore_this" not in st.session_state:
        st.session_state.ignore_this = True

    if "initial_temp" not in st.session_state:
        st.session_state.initial_temp = 0.7

    if "pre_audio_bytes" not in st.session_state:
        st.session_state.pre_audio_bytes = None

    left, _ = st.columns([5, 6])
    st.session_state.temp_value = left.slider(
        label="$\\hspace{0.08em}\\texttt{Temperature}\,$ (higher $\Rightarrow$ more random)",
        min_value=0.0, max_value=1.0, value=st.session_state.initial_temp,
        step=0.1, format="%.1f",
        on_change=ignore_this
    )

    st.write("##### Conversation with AI")

    for (human, ai) in zip(st.session_state.human_enq, st.session_state.ai_resp):
        st.write("**Human:** " + human)
        st.write("**AI:** " + ai)

    # Get the text description from the user
    user_input = st.text_area(
        label="$\\hspace{0.08em}\\texttt{Human}$",
        value="",
        label_visibility="visible"
    )
    user_input_stripped = user_input.strip()

    left, right = st.columns(2) # To show the results below the button
    left.button(
        label="Send",
        on_click=openai_create_text(user_input_stripped, temperature=st.session_state.temp_value)
    )
    right.button(
        label="Reset",
        on_click=reset_conversation
    )

    # Use your microphone
    audio_bytes = audio_recorder(
        pause_threshold=2.0,
        # sample_rate=sr,
        text="Speak",
        recording_color="#e8b62c",
        neutral_color="#6aa36f",
        # icon_name="user",
        icon_size="2x",
    )
    if audio_bytes != st.session_state.pre_audio_bytes:
        try:
            audio_file = "files/recorded_audio.wav"
            with open(audio_file, "wb") as recorded_file:
                recorded_file.write(audio_bytes)
            audio_data = open(audio_file, "rb")

            transcript = openai.Audio.transcribe("whisper-1", audio_data)

            user_input_stripped = transcript['text']
            st.write("**Human:** " + user_input_stripped)
            openai_create_text(
                user_input_stripped, temperature=st.session_state.temp_value
            )
        except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")

        st.session_state.pre_audio_bytes = audio_bytes

    if not st.session_state.ignore_this and user_input_stripped != "":
        st.write("**AI:** " + st.session_state.generated_text)
        st.session_state.human_enq.append(user_input_stripped)
        st.session_state.ai_resp.append(st.session_state.generated_text)
        # clipboard.copy(st.session_state.generated_text)

        # for i in range(len(st.session_state.ai_resp)-1, -1, -1):
        #    message(st.session_state.ai_resp[i].strip(), key=str(i))
        #    message(st.session_state.human_enq[i], is_user=True, key=str(i) + '_user')

    st.session_state.ignore_this = False


def create_image():
    """
    This function geneates image based on user description
    by calling openai_create_image().
    """

    # Get the image description from the user
    # st.write(f"##### Description for your image (in English)")
    description = st.text_area(
        label="$\\hspace{0.1em}\\texttt{Description for your image}\,$ (in $\,$English)",
        # value="",
        label_visibility="visible"
    )

    left, _ = st.columns(2) # To show the results below the button
    left.button(
        label="Generate",
        on_click=openai_create_image(description)
    )


def openai_create():
    """
    This main function generates text or image by calling
    openai_create_text() or openai_create_image(), respectively.
    """
    st.write("## 🎭 OpenAI Generator")

    stored_pin = st.secrets["USER_PIN"]

    st.write("")
    st.write("##### Enter $\,$Password")

    left, _ = st.columns([5, 6])
    user_pin = left.text_input(
        label="Enter password", type="password", label_visibility="collapsed"
    )

    if user_pin == stored_pin:
        st.write("")
        st.write("##### What to Generate")
        option = st.radio(
            "$\\hspace{0.25em}\\texttt{What to generate$",
            ('Text (GPT3.5)', 'Image (DALL·E)'),
            label_visibility="collapsed",
            horizontal=True,
            on_change=reset_initial_temp
        )

        if option == 'Text (GPT3.5)':
            create_text()
        else:
            create_image()
    else:
        left.error("Incorrect password. Please try again.", icon="🚨")


if __name__ == "__main__":
    openai_create()
