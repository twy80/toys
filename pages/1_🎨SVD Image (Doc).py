def svd_image_doc():
    import streamlit as st

    st.write("## 🎨 Image Compression by SVD (Doc)")

    st.write(
        """
        ### SVD of a matrix

        The SVD (Singular Value Decomposition) of a matrix $A$ is the factorization of $A$
        into the product of three matrices $A = UDV^T$, where the columns of $U$ and $V$ are
        orthonormal and the matrix $D$ is diagonal with nonnegative real entries. This
        decomposition can also be written as

        $$
        \\begin{equation*}
            A = \sum_{k=1}^{r} \sigma_k u_k v_k^T
        \\end{equation*}
        $$

        where $r$ is the rank of $A$, the singular value $\sigma_k$ is the $k$-th element of $D$
        arranged in decending order, and $u_k$ and $v_k$ are the $k$-th columns of $U$ and $V$.

        ### Reducing the rank (approximation)

        The approximation of $A$ can be obtained as follows:

        $$
        \\begin{equation*}
            \\tilde{A} = \sum_{k=1}^{n} \sigma_k u_k v_k^T
        \\end{equation*}
        $$

        where $n (\le r)$ is the rank of the compressed matrix $\\tilde{A}$.

        ### Image compression by SVD

        If $A$ contains pixels of an image, $\\tilde{A}$ is a compressed image using a reduced
        amount of memory. This is what is meant by image compression using SVD. If a color image
        is given, the SVD can be performed to each of the three channels (e.g. red, green & blue).
        """
    )


if __name__ == "__main__":
    svd_image_doc()
