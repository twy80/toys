"""
Code∙text∙image generation using openai API (by T.-W. Yoon, Jan. 2023)
"""

import openai
import streamlit as st
# import clipboard


def openai_create_text(description, temperature=0.6):
    if description.strip() == "":
        output_message = ""
    else:
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                # model="text-curie-001",
                prompt=description,
                temperature=temperature,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                # stop=["\n"]
            )
            output_message = response.choices[0].text
            # clipboard.copy(output_message)
        except openai.error.OpenAIError as e:
            output_message = f"An error occurred: {e}"

    st.write(output_message)


def openai_create_code(description, temperature=0):
    if description.strip() == '':
        output_code = ""
    else:
        try:
            response = openai.Completion.create(
                # model="code-davinci-002",
                model="text-davinci-003",
                prompt=description,
                temperature=temperature,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                # stop=["\n"]
            )
            output_code = response.choices[0].text
            # clipboard.copy(output_code)
        except openai.error.OpenAIError as e:
            output_code = f"An error occurred: {e}"

    st.code(output_code)


def openai_create_image(description, returning=False):
    if description.strip() == "":
        output_message = ""
    else:
        try:
            response = openai.Image.create(
                prompt=description,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            output_message = "Success"
        except openai.error.OpenAIError as e:
            output_message = f"An error occurred: {e}"

    if output_message == "Success":
        if returning:
            return image_url
        else:
            st.image(
                image=image_url,
                use_column_width=True
            )
    else:
        if returning:
            return output_message
        else:
            st.write(output_message)


def openai_create():
    # import os

    st.write("## :computer: OpenAI Generator")
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    # openai.api_key = st.text_input(
    #    label="$\\hspace{0.25em}\\texttt{Your OpenAI API Key}$"
    # )
    # st.write("(You can obtain an API key from https://beta.openai.com.)")

    option = st.selectbox(
        "$\\hspace{0.25em}\\texttt{What would you like to generate? Code, Text, or Image?}$",
        ('Code', 'Text', 'Image')
    )

    code_message = "$\\hspace{0.25em}\\texttt{Give a description in the comment style of your language}$"
    text_message = "$\\hspace{0.25em}\\texttt{Give a prompt message for your query}$"
    image_message = "$\\hspace{0.25em}\\texttt{Give a description for your image}$"    
    
    options = {
        "Code": (openai_create_code, code_message),
        "Text": (openai_create_text, text_message),
        "Image": (openai_create_image, image_message)
    }
    
    # Get the code description from the user
    description = st.text_area(
        label=options[option][1],
        # value="",
        label_visibility="visible"
    )

    left, _ = st.columns(2) # To show the results below the button
    left.button(
        label="Generate",
        on_click=options[option][0](description)
    )


if __name__ == "__main__":
    openai_create()
