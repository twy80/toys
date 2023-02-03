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


def svd_pca():
    st.write("## 📖 SVD and PCA")

    st.write(
        """
        ### SVD of a matrix

        Consider an $m\!\\times\!n$ matrix, $A$, of real entries. The SVD
        (Singular Value Decomposition) of $\,A\,$ is described by

        $$
        \\begin{equation*}
            A = U \Sigma V^T \,~or~\, AV = U \Sigma
        \\end{equation*}
        $$
        
        where $\,\Sigma\,$ is ($m\!\\times\!n$) diagonal with nonnegative
        singular values, $\sigma_k$'s, of $A\,$ arranged in decending order,
        and $\,U$ and $V$ are orthogonal, i.e.
        
        $$
        \\begin{equation*}
            U^T U = U U^T = I_m,~\, V^T V = V V^T = I_n.
        \\end{equation*}
        $$
        
        Note that the singular values $\sigma_k$'s are the square roots of
        the eigenvalues from $A A^T$ and $A^T A$, and the columns of $\,U$
        and $\,V$ are orthonormal eigenvectors of $A A^T$ and $A^T A$,
        respectively. As $Av_k = \sigma_k u_k$, this SVD can also be
        written as

        $$
        \\begin{equation}
            A = \sum_{k=1}^{r} \sigma_k u_k v_k^T = \sum_{k=1}^r (A v_k)\, v_k^T
        \\end{equation}
        $$

        where $r \le \min(m,n)$ is the rank of $A$, and $u_k$ and
        $v_k$ the $k$-th columns of $\,U$ and $V\!$. The vector $Av_k$ in (1)
        can be interpreted as the $v_k^{(T)}$ axis components of $A$.

        ### Row-rank approximation by SVD

        The rank-$r$ matrix $A$ can be approximated to the following rank-$d$
        matrix:

        $$
        \\begin{equation}
            \hat{A} = \sum_{k=1}^{d} \sigma_k u_k v_k^T
                    = \sum_{k=1}^d (A v_k)\, v_k^T
        \\end{equation}
        $$

        where $\,d \le r$. In other words, $\,\hat{A}\,$ is a reduced rank
        approximation of $\,A$, which results from considering only the first
        $\,d\,$ components while ignoring the remaining $r\!-\!d$ components.

        #### • Image compression by SVD
        
        If $A$ contains pixels of an image, $\hat{A}$ is a compressed image
        with a reduced amount of memory. This is what is meant by image
        compression using SVD. If a color image is given, the SVD can be
        performed to each of the three channels (e.g. red, green & blue).
        To see how this works, try [🎨 SVD Image](./SVD_Image).
            
        ### SVD and PCA (Principal Component Analysis)
        
        PCA is closely related to SVD. Let us assume that the rows of $A$
        contain the features of your data for machine learning, and
        the number of columns equals that of the measurements. PCA is based
        on the spectral decomposition of a matrix proportional to the covariance
        of $A$. If all the mean values of the columns are zero, this is
        equivalent to the SVD of $A$. If there are non-zero mean values,
        we rewrite $A$ as
        
        $$
        \\begin{equation*}
            A = A_0 + A_\Delta
        \\end{equation*}
        $$        
        
        where the $k$-th column of $A_0$ contains the same element that is
        equal to the mean value of the $k$-th feature ($k$-th column of $A$),
        and $\,A_\Delta\,$ have zero-mean columns. We then consider the SVD
        of $\,A_\Delta\,$ as follows:
        
        $$
        \\begin{equation*}
            A_\Delta = \sum_{k=1}^{r} \\tilde{\sigma}_k \\tilde{u}_k \\tilde{v}_k^T
                     = \sum_{k=1}^r (A_\Delta\\tilde{v}_k)\, \\tilde{v}_k^T
        \\end{equation*}
        $$

        where the singular values and vectors of $\,A_\Delta\,$ are different
        from those of $\,A$. PCA is then tantamount to reducing the $n$-dimensional
        feature space to a $d$-dimensional subspace for $\,A_\Delta\,$ (not for
        $A$). As a result, $A$ can be approximated to $\,\\tilde{A}\,$ that is
        given by

        $$
        \\begin{equation}
            \\tilde{A}
            = A_0 + \sum_{k=1}^d \\tilde{\sigma}_k \\tilde{u}_k \\tilde{v}_k^T
            = A_0 + \sum_{k=1}^d (A_\Delta \\tilde{v}_i)\, \\tilde{v}_i^T
        \\end{equation}
        $$

        where $\,\\tilde{A}v_k$ ($\,k = 1, \cdots, d\,$) represent the principal
        components, and $\,d\,$ is the number of principal components.
        
        So, there are two approximations of $\,A\,$ in (1): $\,\hat{A}\,$ in (2)
        resulting from applying SVD directly to $\,A$, and $\,\\tilde{A}\,$ in
        (3) resulting from applying SVD to the zero-mean version, $\,\Delta A$,
        of $\,A$. PCA is the latter, and we refer to the former as an SVD
        approximation for convenience. Let us compare the two below.

        #### • A numerical example
        
        We consider a $5\!\\times\!3$ matrix, i.e., 5 measurements in a
        3-dimensional feature space. In order not to have a matrix of mean zero
        leading to the equivalence of SVD and PCA, we initialize each entry with
        a random number between -1 and 4 as follows:
        """
    )

    rows, columns = 5, 3
    min_value, max_value = -1.0, 4.0

    st.write("")
    a_matrix = input_matrix(rows, columns, min_value, max_value)
    st.write("")

    left, _ = st.columns([4, 3])
    left.write("Reduced rank $\,d\,$ (number of principal components in PCA)")
    n_comp = left.selectbox(
        "Number of principal components",
        options=(1, 2, 3),
        index=2,
        label_visibility="collapsed"
    )
    
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

    # SVD of A matrix
    u_svd, s_svd, vt_svd = np.linalg.svd(a_matrix, full_matrices=False)
    a_reduced_svd = a_matrix @ vt_svd[:n_comp, :].T
    a_rec_svd = a_reduced_svd @ vt_svd[:n_comp,:]

    # SVD of A_Delta matrix
    u_pca, s_pca, vt_pca = np.linalg.svd(a_delta, full_matrices=False)
    a_reduced_pca = a_delta @ vt_pca[:n_comp, :].T
    a_rec_pca = a_reduced_pca @ vt_pca[:n_comp,:] + a_mean

    # PCA of A matrix
    pca = PCA(n_components=n_comp)
    pca.fit(a_matrix)
    a_reduced_PCA = pca.transform(a_matrix)
    a_rec_PCA = pca.inverse_transform(a_reduced_PCA)

    s_PCA = pca.singular_values_
    vt_PCA = pca.components_

    methods = ("svd", "pca", "PCA")
    cols = (c1, c2, c3)

    for (col, method) in zip(cols, methods):
        col.write(f"**$~~~ ${method}**")
        col.write("Singular values:")
        col.write(eval("s_" + method).reshape(1, -1))
        col.write("Right singular vectors $\,v_k$:")
        col.write(eval("vt_" + method).T)
        col.write("Reduced matrix:")
        col.write(eval("a_reduced_" + method))
        col.write("Approxmated matrix:")
        col.write(eval("a_rec_" + method))
        col.write(
            "Approx. error: $~${:.2e}".format(
                np.linalg.norm(a_matrix - eval("a_rec_" + method))
            )
        )

    left, right = st.columns(2)
    with left:
        st.write(
            "Do **svd** & **pca** lead to the same results?",
            np.allclose(a_rec_svd, a_rec_pca)
        )
    with right:
        st.write(
            "Do **pca** & **PCA** lead to the same results?",
            np.allclose(a_rec_pca, a_rec_PCA)
        )
    
    st.write("")
    st.write(
        """In the above, **svd** and **pca** denote the methods of applying
        SVD to $\,A\,$ and $\,A_{\Delta}\,$ leading to the approximations $\hat{A}$
        and $\\tilde{A}$, respectively. **PCA** shows the results obtained from
        sklearn.decomposition.PCA in the 'scikit-learn' package, and displays
        only $d$ singular values and vectors instead of $n$. As expected,
        **pca** and **PCA** are always equivalent (with some negligible
        numercal differences), although the three including **svd** produce the
        same results only when $\,d = n$. When $\,d < (r \le)\, n$, **pca** seems
        to produce a bit more accurate results than **svd**. You could try to
        explain why.
        """
    )


if __name__ == "__main__":
    svd_pca()
