import streamlit as st


def main():
    import os

    page_title = "TWY's Toys"
    page_icon = "📚"

    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered"
    )

    st.write(f"## {page_icon} {page_title}")

    # with st.sidebar:
    #    st.success("Select a page above.")
    #    if st.button("Finish"):
    #        os._exit(0)

    st.write(
        """
        ### What this page is for
        
        * This page is for my students, and currently talks about three types
          of toy examples.
        
          - SVD (Singular Value Decomposition) of an image file, which results in
            some sort of image compression
 
          - Simulation of a dynamical system described by a differential
            equation
        
          - Use of OpenAI APIs, which enables students to gain a grasp of how things
            like ChatGPT work.
          
        * This pages is not going to be maintained seriously, but will be
          updated every now and then.
        
        ### How this page is written
          
        * All the pages and scripts are written in python using the streamlit
          framework.
        """
    )
    st.write("")
    st.write(
        """
        TWY teaches engineering mathematics, signals and systems, and
        technical writing at Korea University.
        """
    )
    st.write("")

    # if st.button("Finish"):
    #    os._exit(0)


if __name__ == "__main__":
    main()
