"""
Image Compression using SVD by T.-W. Yoon, Jan. 2023
"""


import numpy as np
import streamlit as st


def svd_image(input_image, output_rank, new_image=True):
    """
    This function performs the SVD of an image, and compresses it.

    :param input_image: 2 or 3 dimensional image matrix
    :param output_rank: rank of the compressed image
    :param new_image:   True  => computing the SVD of the image
                        False => reusing the SVD previously computed
    :return:            2 or 3 dimensional compressed image matrix
    """

    from skimage.util import img_as_float, img_as_ubyte

    input_image = img_as_float(input_image)
    image_shape = input_image.shape

    if len(image_shape) == 2:  # 2-dimensional grayscale images are reshaped to be
        image_shape = (*image_shape, 1)  # 3-dimensional images with a single color
        input_image = input_image.reshape(*image_shape)

    output_image = np.zeros(image_shape)
    rows, columns, channels = image_shape

    if new_image is True:  # Compute SVD for a new image
        ns = min(rows, columns)  # Upper bound on the rank of input image

        st.session_state.u = np.zeros((rows, ns, channels))
        st.session_state.vt = np.zeros((ns, columns, channels))
        st.session_state.s = np.zeros((ns, channels))

        for i in range(channels):  # SVD of each channel
            st.session_state.u[:,:,i], st.session_state.s[:,i], st.session_state.vt[:,:,i] \
              = np.linalg.svd(input_image[:,:,i], full_matrices=False)

    for i in range(channels):  # Compress the image using SVD
        output_image[:,:,i] = (
            st.session_state.u[:,:output_rank,i] * st.session_state.s[:output_rank,i]
        ) @ st.session_state.vt[:output_rank,:,i]

        if channels == 1:  # grayscale images are reshaped back to be 2-dimensional images
            output_image = output_image.reshape(rows, columns)

    return img_as_ubyte(np.clip(output_image, 0, 1))


def reset_new_image():
    st.session_state.new_image = True


def svd_plot(output_rank):
    """
    This function calls svd_image() and plot the results.
    """

    with st.spinner("Performing SVD"):
        output_image = svd_image(
            st.session_state.input_image, output_rank, st.session_state.new_image
        )                           # Compress the image by SVD
        st.session_state.new_image = False

        # Plot the resulting image

        left, right = st.columns(2)
        left.image(
            image=output_image,
            caption=f"Rank-{output_rank} image",
            use_column_width=True
        )
        right.image(
            image=st.session_state.input_image,
            caption=f"Original rank-{st.session_state.rank} image",
            use_column_width=True
        )


def reset_initial_rank():
    st.session_state.pre_output_rank = st.session_state.output_rank


def run_svd_image():
    """
    This function selects an image file and computes its rank.
    The resulting image and rank value are stored
    as streamlit session state variables.
    
    This is the main function calling svd_plot().
    """

    from PIL import Image, UnidentifiedImageError

    st.write("## 🎨 Image Compression by SVD")

    st.write("")
    st.write(
        """
        As discussed in [📖 SVD and PCA](./SVD_and_PCA), SVD
        (Singular Value Decomposition) can be used to approximate a matrix
        by reducing the rank. An image is a set of matrices, and
        therefore a lower rank image can be obtained by performing SVD.
        This leads to some of image compression.
        """
    )
    st.write("")

    # Upload an image file
    st.write("##### Upload an image")
    image_file = st.file_uploader(
        label="High resolution images will be resized.",
        type=["jpg", "jpeg", "png", "bmp"],
        accept_multiple_files=False,
        on_change=reset_new_image,
        label_visibility="visible"
    )

    if image_file is not None:
        if st.session_state.new_image:
            # Process the uploaded image file
            try:
                image = Image.open(image_file)
            except UnidentifiedImageError as e:
                st.error(f"An error occurred: {e}", icon="🚨")
                return None

            st.session_state.pre_output_rank = 1

            if max(image.width, image.height) > 1024:
                if image.width > image.height:
                    new_width, new_height = 1024, image.height * 1024 // image.width
                else:
                    new_width, new_height = image.width * 1024 // image.height, 1024

                image = image.resize((new_width, new_height))

            original_image = np.array(image)
            image_shape = original_image.shape

            # If the image is grayscale, channels = 1
            channels = 1 if len(image_shape) == 2 else 3

            rank = 1
            with st.spinner("Computing the rank of the uploaded image"):
                for i in range(channels):  # Compute the rank of each channel
                    if channels == 1:
                        rank = np.linalg.matrix_rank(original_image)
                    else:
                        rank = max(rank, np.linalg.matrix_rank(original_image[:, :, i]))

            # Store the image together with the rank and dimension
            st.session_state.input_image = original_image
            st.session_state.image_dim = image.size
            st.session_state.rank = rank

        # Write the information of the uploaded image
        st.write(
            "Uploaded (resized) image:",
            st.session_state.image_dim[0], "x", st.session_state.image_dim[1],
            "pixels of rank", st.session_state.rank,            
        )
        st.write("---")

        # Input the rank of the compressed image
        left, _, right = st.columns([5, 1, 5])
        option = left.radio(
            "$\\hspace{0.07em}\\texttt{How to set the rank}$",
            ("Slider", "Textbox"),
            horizontal=True,
            on_change=reset_initial_rank
        )

        input_method = right.slider if option == "Slider" else right.number_input
        st.session_state.output_rank = input_method(
            label="$\\hspace{0.07em}\\texttt{Rank of the compressed image}$",
            min_value=1,
            max_value=int(st.session_state.rank),
            value=st.session_state.pre_output_rank,
            step=1,
            label_visibility="visible"
        )

        # Compress the image by SVD
        svd_plot(st.session_state.output_rank)

    return None


if __name__ == "__main__":
    run_svd_image()
