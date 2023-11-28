"""
ChatGPT & DALL·E using openai API (by T.-W. Yoon, Aug. 2023)
"""

import streamlit as st
import openai
from audio_recorder_streamlit import audio_recorder
import os, io, base64
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


# This is for streaming on Streamlit
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def chat_complete(user_prompt, model="gpt-3.5-turbo", temperature=0.7):
    """
    This function generates text based on user input.

    Args:
        user_prompt (string): User input
        temperature (float): Value between 0 and 1. Defaults to 0.7
        model (string): "gpt-3.5-turbo" or "gpt-4".

    Return:
        generated text

    All the conversations are stored in st.session_state variables.
    """

    openai_llm = ChatOpenAI(
        openai_api_key=st.session_state.openai_api_key,
        temperature=temperature,
        model_name=model,
        streaming=True,
        callbacks=[StreamHandler(st.empty())]
    )

    # Add the user input to the messages
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    try:
        response = openai_llm(st.session_state.messages)
        generated_text = response.content
    except Exception as e:
        generated_text = None
        st.error(f"An error occurred: {e}", icon="🚨")

    if generated_text is not None:
        # Add the generated output to the messages
        st.session_state.messages.append(response)

    return generated_text


def openai_create_image(description, size="1024x1024"):
    """
    This function generates image based on user description.

    Args:
        description (string): User description
        size (string): Pixel size of the generated image

    The resulting image is plotted.
    """

    if description:
        try:
            with st.spinner("AI is generating..."):
                response = st.session_state.openai.images.generate(
                    model="dall-e-3",
                    prompt=description,
                    size=size,
                    quality="standard",
                    n=1,
                )
            image_url = response.data[0].url
            st.image(image=image_url, use_column_width=True)
        except Exception as e:
            st.error(f"An error occurred: {e}", icon="🚨")

    return None


def get_vector_store(uploaded_file):
    """
    This function takes an UploadedFile object as input,
    and returns a FAISS vector store.
    """

    uploaded_document = "files/uploaded_document"

    if uploaded_file is None:
        return None
    else:
        file_bytes = io.BytesIO(uploaded_file.read())
        with open(uploaded_document, "wb") as f:
            f.write(file_bytes.read())

        # Determine the loader based on the file extension.
        if uploaded_file.name.lower().endswith(".pdf"):
            loader = PyPDFLoader(uploaded_document)
        elif uploaded_file.name.lower().endswith(".txt"):
            loader = TextLoader(uploaded_document)
        elif uploaded_file.name.lower().endswith(".docx"):
            loader = Docx2txtLoader(uploaded_document)
        else:
            st.error("Please load a file in pdf or txt", icon="🚨")
            return None

        # Load the document using the selected loader.
        document = loader.load()

        try:
            with st.spinner("Vector store in preparation..."):
                # Split the loaded text into smaller chunks for processing.
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    # separators=["\n", "\n\n", "(?<=\. )", "", " "],
                )

                doc = text_splitter.split_documents(document)

                # Create a FAISS vector database.
                embeddings = OpenAIEmbeddings(
                    openai_api_key=st.session_state.openai_api_key
                )
                vector_store = FAISS.from_documents(doc, embeddings)
        except Exception as e:
            vector_store = None
            st.error(f"An error occurred: {e}", icon="🚨")

        return vector_store


def document_qna(query, vector_store, model="gpt-3.5-turbo"):
    """
    This function takes a user prompt, a vector store and a GPT model,
    and returns a response on the uploaded document along with sources.
    """

    if vector_store is not None:
        if st.session_state.memory is None:
            st.session_state.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )

        openai_llm = ChatOpenAI(
            openai_api_key=st.session_state.openai_api_key,
            temperature=0,
            model_name=model,
            streaming=True,
            callbacks=[StreamHandler(st.empty())]
        )
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=openai_llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(),
            # retriever=vector_store.as_retriever(search_type="mmr"),
            memory=st.session_state.memory,
            return_source_documents=True
        )

        try:
            # response to the query is given in the form
            # {"question": ..., "chat_history": [...], "answer": ...}.
            response = conversation_chain({"question": query})
            generated_text = response["answer"]
            source_documents = response["source_documents"]

        except Exception as e:
            generated_text, source_documents = None, None
            st.error(f"An error occurred: {e}", icon="🚨")
    else:
        generated_text, source_documents = None, None

    return generated_text, source_documents


def read_audio(audio_bytes):
    """
    This function reads audio bytes and returns the corresponding text.
    """
    try:
        audio_data = io.BytesIO(audio_bytes)
        audio_data.name = "recorded_audio.wav"  # dummy name

        transcript = st.session_state.openai.audio.transcriptions.create(
            model="whisper-1", file=audio_data
        )
        text = transcript.text
    except Exception:
        text = None

    return text


def perform_tts(text):
    """
    This function takes text as input, performs text-to-speech (TTS),
    and returns an audio_response.
    """

    try:
        with st.spinner("TTS in progress..."):
            audio_response = st.session_state.openai.audio.speech.create(
                model="tts-1",
                voice="shimmer",
                input=text,
            )
    except Exception:
        audio_response = None

    return audio_response


def autoplay_audio(file_path):
    """
    This function takes an audio file as input,
    and automatically plays the audio file.
    """

    # Get the file extension from the file path
    _, ext = os.path.splitext(file_path)

    # Determine the MIME type based on the file extension
    mime_type = f"audio/{ext.lower()[1:]}"  # Remove the leading dot from the extension

    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

        md = f"""
            <audio controls autoplay style="width: 100%;">
            <source src="data:{mime_type};base64,{b64}" type="{mime_type}">
            </audio>
            """

        st.markdown(md, unsafe_allow_html=True)


def reset_conversation():
    st.session_state.messages = [
        SystemMessage(content=st.session_state.prev_ai_role)
    ]
    st.session_state.prompt_exists = False
    st.session_state.human_enq = []
    st.session_state.ai_resp = []
    st.session_state.initial_temp = st.session_state.temp_value
    st.session_state.play_audio = False
    st.session_state.vector_store = None
    st.session_state.sources = None
    st.session_state.memory = None


def switch_between_apps():
    if "temp_value" not in st.session_state:
        st.session_state.temp_value = 0.7
    st.session_state.initial_temp = st.session_state.temp_value


def enable_user_input():
    st.session_state.prompt_exists = True


def create_text(model):
    """
    This function geneates text based on user input
    by calling chat_complete().

    model is set to "gpt-3.5-turbo" or "gpt-4".
    """

    # Audio file for TTS
    text_audio_file = "files/output_text.wav"

    # initial system prompts
    general_role = "You are a helpful assistant."
    english_teacher = "You are an English teacher who analyzes texts and corrects any grammatical issues if necessary."
    translator = "You are a translator who translates English into Korean and Korean into English."
    coding_adviser = "You are an expert in coding who provides advice on good coding styles."
    doc_analyzer = "You are an assistant analyzing the document uploaded."
    roles = (general_role, english_teacher, translator, coding_adviser, doc_analyzer)

    if "prev_ai_role" not in st.session_state:
        st.session_state.prev_ai_role = general_role

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=st.session_state.prev_ai_role)
        ]

    if "prompt_exists" not in st.session_state:
        st.session_state.prompt_exists = False

    if "human_enq" not in st.session_state:
        st.session_state.human_enq = []

    if "ai_resp" not in st.session_state:
        st.session_state.ai_resp = []

    if "initial_temp" not in st.session_state:
        st.session_state.initial_temp = 0.7

    if "mic_used" not in st.session_state:
        st.session_state.mic_used = False

    if "play_audio" not in st.session_state:
        st.session_state.play_audio = False

    # session_state variables for RAG
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    if "sources" not in st.session_state:
        st.session_state.sources = None

    if "memory" not in st.session_state:
        st.session_state.memory = None

    with st.sidebar:
        st.write("")
        st.write("**Text to Speech**")
        st.session_state.tts = st.radio(
            label="$\\hspace{0.08em}\\texttt{TTS}$",
            options=("Enabled", "Disabled", "Auto"),
            # horizontal=True,
            index=2,
            label_visibility="collapsed",
        )
        st.write("")
        st.write("**Temperature**")
        st.session_state.temp_value = st.slider(
            label="$\\hspace{0.08em}\\texttt{Temperature}\,$ (higher $\Rightarrow$ more random)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.initial_temp,
            step=0.1,
            format="%.1f",
            label_visibility="collapsed",
        )
        st.write("(Higher $\Rightarrow$ More random)")

    st.write("")
    st.write("##### Message to AI")
    ai_role = st.selectbox(
        label="AI's role",
        options=roles,
        index=roles.index(st.session_state.prev_ai_role),
        label_visibility="collapsed",
    )

    if ai_role != st.session_state.prev_ai_role:
        st.session_state.prev_ai_role = ai_role
        reset_conversation()

    if ai_role == doc_analyzer:
        st.write("")
        left, right = st.columns([4, 7])
        left.write("##### Document to ask about")
        right.write("Temperature is set to 0.")
        uploaded_file = st.file_uploader(
            label="Upload an article",
            type=["txt", "pdf", "docx"],
            accept_multiple_files=False,
            on_change=reset_conversation,
            label_visibility="collapsed",
        )
        if st.session_state.vector_store is None:
            # Create the vector store.
            st.session_state.vector_store = get_vector_store(uploaded_file)

            if st.session_state.vector_store is not None:
                st.write(f"Vector store for :blue[[{uploaded_file.name}]] is ready!")

    st.write("")
    left, right = st.columns([4, 7])
    left.write("##### Conversation with AI")
    right.write("Click on the mic icon and speak, or type text below.")

    # Print conversations
    for human, ai in zip(st.session_state.human_enq, st.session_state.ai_resp):
        with st.chat_message("human"):
            st.write(human)
        with st.chat_message("ai"):
            st.write(ai)

    if ai_role == doc_analyzer and st.session_state.sources is not None:
        with st.expander("Sources"):
            for index in range(len(st.session_state.sources)):
                st.markdown(
                    # st.session_state.sources[index].metadata["source"],
                    "Uploaded document",
                    help=st.session_state.sources[index].page_content
            )

    # Play TTS
    if st.session_state.play_audio:
        autoplay_audio(text_audio_file)
        st.session_state.play_audio = False

    # Reset the conversation
    st.button(label="Reset the conversation", on_click=reset_conversation)

    # Use your keyboard
    user_input = st.chat_input(
        placeholder="Enter your query",
        on_submit=enable_user_input,
        disabled=not uploaded_file if ai_role == doc_analyzer else False,
    )

    # Use your microphone
    audio_bytes = audio_recorder(
        pause_threshold=3.0, text="Speak", icon_size="2x",
        recording_color="#e87070", neutral_color="#6aa36f"        
    )

    if audio_bytes != st.session_state.prev_audio_bytes:
        user_prompt = read_audio(audio_bytes)
        if user_prompt is not None:
            st.session_state.prompt_exists = True
            st.session_state.mic_used = True
        st.session_state.prev_audio_bytes = audio_bytes
    elif user_input and st.session_state.prompt_exists:
        user_prompt = user_input.strip()

    if st.session_state.prompt_exists:
        with st.chat_message("human"):
            st.write(user_prompt)

        with st.chat_message("ai"):
            if ai_role == doc_analyzer:  # RAG (when there is a document uploaded)
                generated_text, st.session_state.sources = document_qna(
                    user_prompt,
                    vector_store=st.session_state.vector_store,
                    model=model
                )
            else:  # General chatting
                generated_text = chat_complete(
                    user_prompt,
                    temperature=st.session_state.temp_value,
                    model=model
                )

        if generated_text is not None:
            # TTS under two conditions
            cond1 = st.session_state.tts == "Enabled"
            cond2 = st.session_state.tts == "Auto" and st.session_state.mic_used
            if cond1 or cond2:
                audio_response = perform_tts(generated_text)
                if audio_response is not None:
                    audio_response.stream_to_file(text_audio_file)
                    st.session_state.play_audio = True

            st.session_state.mic_used = False
            st.session_state.human_enq.append(user_prompt)
            st.session_state.ai_resp.append(generated_text)

        st.session_state.prompt_exists = False

        if generated_text is not None:
            st.rerun()


def create_image():
    """
    This function geneates image based on user description
    by calling openai_create_image().
    """

    def show_text_image(description, image_size):
        st.write(f":blue[{description}]")
        openai_create_image(description, image_size)

    # Set the image size
    with st.sidebar:
        st.write("")
        st.write("**Pixel size**")
        image_size = st.radio(
            label="$\\hspace{0.1em}\\texttt{Pixel size}$",
            options=("1024x1024", "1792x1024", "1024x1792"),
            # horizontal=True,
            index=0,
            label_visibility="collapsed",
        )

    st.write("")
    st.write("##### Description for your image")

    # Get an image description using the microphone
    audio_bytes = audio_recorder(
        pause_threshold=3.0, text="Speak", icon_size="2x",
        recording_color="#e87070", neutral_color="#6aa36f"        
    )
    if audio_bytes != st.session_state.prev_audio_bytes:
        audio_input = read_audio(audio_bytes)
        if audio_input is not None:
            show_text_image(audio_input, image_size)
        st.session_state.prev_audio_bytes = audio_bytes

    # Get an image description using the keyboard
    text_input = st.chat_input(
        placeholder="Enter a description for your image",
    )
    if text_input:
        show_text_image(text_input, image_size)


def create_text_image():
    """
    This main function generates text or image by calling
    openai_create_text() or openai_create_image(), respectively.
    """

    if "openai" not in st.session_state:
        st.session_state.openai = None

    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""

    if "prev_audio_bytes" not in st.session_state:
        st.session_state.prev_audio_bytes = None

    st.write("## 🎭 ChatGPT (RAG)$\,$ &$\,$ DALL·E")

    with st.sidebar:
        # st.write("")
        st.write("**API Key Selection**")
        choice_api = st.sidebar.radio(
            label="$\\hspace{0.25em}\\texttt{Choic of API}$",
            options=("Your key", "My key"),
            label_visibility="collapsed",
            horizontal=True,
        )

        if choice_api == "Your key":
            st.write("**Your API Key**")
            st.session_state.openai_api_key = st.text_input(
                label="$\\hspace{0.25em}\\texttt{Your OpenAI API Key}$",
                type="password",
                label_visibility="collapsed",
            )
            authen = False if st.session_state.openai_api_key == "" else True
        else:
            st.session_state.openai_api_key = st.secrets["openai_api_key"]
            stored_pin = st.secrets["user_PIN"]
            st.write("**Password**")
            user_pin = st.text_input(
                label="Enter password", type="password", label_visibility="collapsed"
            )
            authen = user_pin == stored_pin

        st.session_state.openai = openai.OpenAI(
            api_key=st.session_state.openai_api_key
        )

        st.write("")
        st.write("**What to Generate**")
        option = st.sidebar.radio(
            label="$\\hspace{0.25em}\\texttt{What to generate}$",
            options=("Text (GPT 3.5)", "Text (GPT 4)", "Image (DALL·E 3)"),
            label_visibility="collapsed",
            # horizontal=True,
            on_change=switch_between_apps,
        )

    if authen:
        if option == "Text (GPT 3.5)":
            create_text("gpt-3.5-turbo")
        elif option == "Text (GPT 4)":
            create_text("gpt-4")
        else:
            create_image()
    else:
        st.write("")
        if choice_api == "Your key":
            st.info("**Enter your OpenAI API key in the sidebar**")
        else:
            st.info("**Enter the correct password in the sidebar**")


if __name__ == "__main__":
    create_text_image()
