"""
Title (by T.-W. Yoon, Jan. 2023)
"""

import numpy as np
import streamlit as st
from sklearn.decomposition import PCA


def input_matrix(rows, columns, min_value, max_value):
    """
    This function inputs a matrix and return it

    Parameters:
    rows (int): the number of rows of the matrix
    columns (int): the number of columns of the matrix
    min_value (float): the minimum value of each entry
    max_value (float): the maximum value of each entry
    
    Returns:
        np.array: matrix
    """

    if "initial_matrix" not in st.session_state:
        st.session_state.initial_matrix = np.random.uniform(
            min_value,
            max_value,
            size=(rows, columns)
        )

    matrix = np.zeros((rows, columns))
    step = (max_value - min_value) / 10.

    cols = st.columns(columns)
    for i in range(rows):
        for j, col in enumerate(cols):
            matrix[i,j] = col.number_input(
                f"({i+1},{j+1})-th element in [{min_value}, {max_value}]",
                value=st.session_state.initial_matrix[i,j],
                min_value=min_value, max_value=max_value, step=step
            )

    return matrix


def main():
    st.write("## 📖 SVD & PCA")

    st.write(
        """
        ### SVD of a matrix

        The SVD (Singular Value Decomposition) of an $m\!\\times\!n$ matrix $A$ of real entries
        is described by

        $$
        \\begin{equation*}
            A = U \Sigma V^T \,~or~\, AV = U \Sigma
        \\end{equation*}
        $$
        
        where $\,\Sigma\,$ is an $m\!\\times\!n$ diagonal matrix with nonnegative singular values of $A$,
        and $U$ and $V$ are orthogonal matrices, i.e.
        
        $$
        \\begin{equation*}
            U^T U = U U^T = I_m,~\, V^T V = V V^T = I_n.
        \\end{equation*}
        $$
        
        Note that the singular values, $\sigma_i$'s, of $A$ are the eigenvalues of $A A^T$ and $A^T A$, and
        the columns of $U$ and $V$ are orthonormal eigenvectors of $A A^T$ and $A^T A$, respectively.
        This SVD can also be written as

        $$
        \\begin{equation}
            A = \sum_{k=1}^{r} \sigma_k u_k v_k^T = \sum_{k=1}^r (A v_k)\, v_k^T
        \\end{equation}
        $$

        where $r$ is the rank of $A$, $\sigma_k$ the $k$-th element of $\,\Sigma\,$
        arranged in decending order, and $u_k$ and $v_k$ the $k$-th columns of $\,U$ and $V\!$.
        The vector $Av_k$ in (1) can be interpreted as the $v_k^{(T)}$ axis components of $A$.

        ### Row-rank approximation by SVD

        The rank-$r$ matrix $A$ can be approximated to the following rank-$d$ matrix:

        $$
        \\begin{equation}
            \hat{A} = \sum_{k=1}^{d} \sigma_k u_k v_k^T = \sum_{k=1}^d (A v_k)\, v_k^T
        \\end{equation}
        $$

        where $\,d \le r$. In other words, $\,\hat{A}\,$ is a reduced rank approximation of $\,A$.

        #### $\:\!$ • Image compression by SVD
        
        > If $A$ contains pixels of an image, $\hat{A}$ is a compressed image with a reduced
        > amount of memory. This is what is meant by image compression using SVD. If a color image
        > is given, the SVD can be performed to each of the three channels (e.g. red, green & blue).
        > To see how this works, try [🎨 SVD Image](./SVD_Image).
            
        ### SVD and PCA (Principal Component Analysis)
        
        PCA is closely related to SVD. Let us assume that the rows of $A$ contain the features of
        your data and the number of columns equals that of the measurements. PCA is based on the
        spectral decomposition of $A$, which is proportional to the covariance of $A$.
        If all the mean values of the columns of $A$ are zero, this is equivalent to the SVD of $A$.
        If there are non-zero mean values, we rewrite $A$ as
        
        $$
        \\begin{equation*}
            A = A_0 + A_\Delta,
        \\end{equation*}
        $$        
        
        where the $i$-th column of $A_0$ contains the same element that is equal to the mean value of
        the $i$-th feature ($i$-th column of $A$), and $\,A_\Delta\,$ have mean zero columns. We then
        consider the SVD of $\,A_\Delta\,$ as follows:
        
        $$
        \\begin{equation*}
            A_\Delta = \sum_{k=1}^{r} \\tilde{\sigma}_k \\tilde{u}_k \\tilde{v}_k^T =
            \sum_{k=1}^r (A_\Delta\\tilde{v}_k)\, \\tilde{v}_k^T
        \\end{equation*}
        $$

        where the singular values and vectors of $\,A_\Delta\,$ are different from those of $\,A$.
        PCA is then tantamount to reducing the $r$-dimensional feature space to a $d$-dimensional
        subspace. As a result, $A$ can be approximated to $\,\\tilde{A}\,$ given by

        $$
        \\begin{equation}
            \\tilde{A} = A_0 + \sum_{k=1}^d \\tilde{\sigma}_k \\tilde{u}_k \\tilde{v}_k^T =
            A_0 + \sum_{k=1}^d (A_\Delta \\tilde{v}_i)\, \\tilde{v}_i^T
        \\end{equation}
        $$

        where $\,d\,$ is the number of principal components, and $\,\\tilde{A}v_k$
        ($\,k = 1, \cdots, d\,$) represent the principal components.
        
        So, there are two approximations of $\,A\,$ in (1): $\,\hat{A}\,$ in (2) resulting from
        applying SVD directly to $\,A$, and $\,\\tilde{A}\,$ in (3) resulting from applying
        SVD to the zero mean version, $\,\Delta A$, of $\,A$. The latter is what is referred to as
        PCA. For convenience, we call the former as an SVD approximation. Let us compare the two
        below.

        #### $\:\!$ • A numerical example
        
        > We consider a $5\!\\times\!3$ matrix, i.e., 5 measurements in a 3 dimensional feature space.
        > In order not to have a matrix of mean zero leading to the equivalence of SVD
        > and PCA, we initialize each entry with a random number between $-1$ and $3$ as follows:

        """
    )

    rows, columns = 5, 3
    min_value, max_value = -1.0, 3.0

    st.write("")
    a_matrix = input_matrix(rows, columns, min_value, max_value)
    
    a_mean = a_matrix.mean(axis=0)
    a_0 = np.tile(a_mean, (rows, 1)) # This is only for printing
    a_delta = a_matrix - a_mean

    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.write("$~~~ A$")
    c1.write(a_matrix)
    c2.write("$~~~ A_0$")
    c2.write(a_0)
    c3.write("$~~~ A_\Delta$")
    c3.write(a_delta)
    st.write("")
    st.write("")
    
    n_comp = c1.selectbox(
        "$\\hspace{0.25em}\\texttt{Number of principal components}$",
        options=(1, 2, 3),
        index=2
    )

    # SVD of A matrix
    u_svd1, s_svd1, vt_svd1 = np.linalg.svd(a_matrix, full_matrices=False)
    a_reduced_svd1 = a_matrix @ vt_svd1[:n_comp, :].T
    a_rec_svd1 = a_reduced_svd1 @ vt_svd1[:n_comp,:]

    # SVD of A_Delta matrix
    u_svd2, s_svd2, vt_svd2 = np.linalg.svd(a_delta, full_matrices=False)
    a_reduced_svd2 = a_delta @ vt_svd2[:n_comp, :].T
    a_rec_svd2 = a_reduced_svd2 @ vt_svd2[:n_comp,:] + a_mean

    # PCA of X
    pca = PCA(n_components=n_comp)
    pca.fit(a_matrix)
    a_reduced_pca = pca.transform(a_matrix)
    a_rec_pca = pca.inverse_transform(a_reduced_pca)

    s_pca = pca.singular_values_
    vt_pca = pca.components_

    Methods = ["svd1", "svd2", "pca"]

    for method in Methods:
        st.write("[" + method + "]", "Squared singular values:")
        st.write(eval("s_" + method) ** 2)
        st.write("[" + method + "]", "Right singular vectors:")
        st.write(eval("vt_" + method))
        st.write("")
        st.write(
            "[" + method + "]",
            "Reduced & reconstructed matrices and norm of the reconstruction error:"
        )
        st.write(eval("a_reduced_" + method))
        st.write("")
        st.write(eval("a_rec_" + method))

        st.write(np.linalg.norm(a_matrix - eval("a_rec_" + method)))

    st.write(
        "Do SVD1 & PCA lead to the same results?",
        np.allclose(a_rec_svd1, a_rec_pca)
    )
    st.write(
        "Do SVD2 & PCA lead to the same results?",
        np.allclose(a_rec_svd2, a_rec_pca)
    )


if __name__ == "__main__":
    main()
