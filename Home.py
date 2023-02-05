import streamlit as st


def main():
    page_title = "TWY's Toys"
    page_icon = "📚"

    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered"
    )

    st.write(f"## {page_icon} {page_title}")

    st.write(
        """
        ### What this site is for
        
        * This site is for my students, and currently talks about the following
          toy examples.

          - Simulation of a dynamical system described by a differential
            equation
        
          - SVD (Sinular Value Decomposition) together with a relation
            with PCA (Principal Component Analsys)
          
          - SVD of an image file, which results in some sort of image compression
          
          - Fourier transform (of sound waves), which is an essential concept
            in signals and systems
 
          - Use of OpenAI APIs, which familiarize students with natural
            language models as in ChatGPT.
                  
        ### How this site is written
          
        * All the pages and scripts are written in python using the streamlit
          framework.
    
        #### What TWY does
    
        * TWY teaches engineering mathematics, signals and systems,
          technical writing, etc at Korea University.
        
        * Lecture videos (in Korean)
        
          - [Linear Algebra](https://youtube.com/playlist?list=PLIzv0-ErbDpwNdtK1OZ7Ew54s3tlXzX4Q)
          - [Signals and Systems](https://youtube.com/playlist?list=PLIzv0-ErbDpxvwnZ3yFBLKuYP0fhDECov)
          - [Complex Functions](https://youtube.com/playlist?list=PLIzv0-ErbDpyqRVlmnLsGeC_mLmu-dU-L)
          - [Mathematical Thinking and Writing](https://youtu.be/eqHsIbwvvrk)
          - [Science, Technology, and Gender Diversity](https://youtu.be/xUJ9e_hESG8)
        """
    )
    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info('**[Email](mailto:yoon.tw@gmail.com)**', icon="✉️")
    with c2:
        st.info('**[GitHub](https://github.com/twy80)**', icon="💻")
    with c3:
        st.info('**[Youtube](https://www.youtube.com/@twy80)**', icon="📺")


if __name__ == "__main__":
    main()
