"""
Classification algorithms (by T.-W. Yoon, Mar. 2023)
"""

import streamlit as st
import numpy as np

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

import torch
import torch.nn as nn
import torch.optim as optim


def get_dataset(name):
    if name == 'Iris':
        data = datasets.load_iris()
    elif name == 'Wine':
        data = datasets.load_wine()
    else:
        data = datasets.load_breast_cancer()
    X = data.data
    y = data.target
    return X, y


class LogisticRegression(nn.Module):
    def __init__(self, input_size, num_classes):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(input_size, num_classes)

    def forward(self, x):
        out = self.linear(x)
        return out


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_sizes, num_classes):
        super(NeuralNetwork, self).__init__()
        self.hidden_layers = nn.ModuleList()
        self.hidden_layers.append(nn.Linear(input_size, hidden_sizes[0]))
        for i in range(1, len(hidden_sizes)):
            self.hidden_layers.append(nn.Linear(hidden_sizes[i-1], hidden_sizes[i]))
        self.output_layer = nn.Linear(hidden_sizes[-1], num_classes)

    def forward(self, x):
        for layer in self.hidden_layers:
            x = torch.relu(layer(x))
        out = self.output_layer(x)
        return out


def classifier():
    st.write("## 🔍 Classification Algorithms")

    dataset_name = st.sidebar.radio(
        '$\\texttt{Select Dataset}$',
        ('Iris', 'Breast Cancer', 'Wine')
    )

    st.write(f"#### Dataset: :green[{dataset_name}]")

    if dataset_name == 'Iris':
        st.write(
            """
            The `Iris` dataset contains information about the physical attributes
            of three different species of iris flowers: Setosa, Versicolor, and
            Virginica. It includes measurements of sepal length, sepal width,
            petal length, and petal width for 150 iris flowers, with 50 flowers
            from each species.
            """
        )
    elif dataset_name == 'Breast Cancer':
        st.write(
            """
            The `Breast Cancer` dataset contains information about
            the characteristics of breast cancer tumors. It includes
            measurements of the size of the tumor, the smoothness of its texture,
            the compactness of its cells, and other features for 569 tumors.
            The dataset is labeled with a binary classification indicating
            whether each tumor is malignant or benign.
            """
        )
    else:
        st.write(
            """
            The `Wine` dataset contains information about the chemical composition
            of wines from three different cultivars in the same region in Italy.
            It includes measurements of 13 different chemical properties for 178
            wines, with 59 wines from cultivar 1, 71 wines from cultivar 2, and
            48 wines from cultivar 3.
            """
        )

    X, y = get_dataset(dataset_name)

    num_classes = len(set(y))
    num_samples, num_features = X.shape
    st.write('- Number of features:', num_features)
    st.write('- Number of classes:', num_classes)
    st.write('- Number of samples:', num_samples)

    #### CLASSIFICATION ####
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1234
    )

    clf_name = st.sidebar.radio(
        '$\\texttt{Select classifier}$',
        ('K-Nearest Neighbors', 'Support Vector Machine', 'Random Forest',
         'Logistic Regression', 'Neural Network'),
    )

    st.write(f"#### Classifier: :green[{clf_name}]")

    plt.rcParams.update({'font.size': 7})
    st.write("- Tuning parameter(s)")
    _, right = st.columns([1, 30])
    _, r1, _, r2 = st.columns([1, 13, 1, 13])

    if clf_name in {'Logistic Regression', 'Neural Network'}:
        learning_rate = r1.slider(
            "Learning rate", 0.001, 0.1, step=0.001, format="%.3f"
        )
        num_epochs = r2.slider("Number of epochs", 50, 500)
        if clf_name == 'Neural Network':
            num_hidden_layers = r1.slider('Number of hidden layers', 1, 10, 1, 1)
            hidden_layer_sizes = []
            for i in range(num_hidden_layers):
                if i <= num_hidden_layers/2 - 1:
                    size = r1.slider(
                        f'Number of units in hidden layer {i+1}', 1, 100, 10, 1
                    )
                else:
                    size = r2.slider(
                        f'Number of units in hidden layer {i+1}', 1, 100, 10, 1
                    )
                hidden_layer_sizes.append(size)

            model = NeuralNetwork(num_features, hidden_layer_sizes, num_classes)
        else:
            model = LogisticRegression(num_features, num_classes)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=learning_rate)

        losses = []
        for epoch in range(num_epochs):
            # Convert inputs to PyTorch tensors
            inputs = torch.from_numpy(X_train).float()
            targets = torch.from_numpy(y_train).long()

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Save loss for plotting
            losses.append(loss.item())

        with torch.no_grad():
            inputs = torch.from_numpy(X_test).float()
            targets = torch.from_numpy(y_test).long()
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            accuracy = (predicted == targets).sum().item() / targets.size(0)

        st.write("- Loss versus epoch")
        fig1 = plt.figure()
        plt.plot(losses)
        plt.xlabel("Epoch")
        plt.ylabel("Loss")

        st.pyplot(fig1)

    else:  # SVM, K-Nearest Neighbors, or Random Forest
        if clf_name == 'Support Vector Machine':
            c_value = right.slider('C', 0.01, 10.0, step=0.01)
            clf = SVC(C=c_value)
        elif clf_name == 'K-Nearest Neighbors':
            k_value = right.slider('K', 1, 10)
            clf = KNeighborsClassifier(n_neighbors=k_value)
        else:
            max_depth = r1.slider('Maximum depth', 2, 10)
            n_estimators = r2.slider(
                'Numbeor of estimators', 1, 100
            )
            clf = RandomForestClassifier(
                n_estimators=n_estimators, max_depth=max_depth, random_state=1234
            )

        clf.fit(X_train, y_train)
        predicted = clf.predict(X_test)

        accuracy = clf.score(X_test, y_test)

    st.write("- Accuracy = ", accuracy)

    #### PLOT DATASET ####
    # Project the data onto the 2 primary principal components

    st.write("- Two primary principal components of test data")

    pca = PCA(2)
    X_projected = pca.fit_transform(X_test)
    x1 = X_projected[:, 0]
    x2 = X_projected[:, 1]

    fig2, ax = plt.subplots(1, 2)

    for index, y in enumerate([y_test, predicted]):
        im = ax[index].scatter(
            x1, x2, c=y, alpha=0.8, cmap='viridis'
        )
        # fig2.colorbar(im, ax=ax[index])

    ax[0].set_xlabel('Actual classes')
    ax[1].set_xlabel('Predicted classes')
    st.pyplot(fig2)


if __name__ == "__main__":
    classifier()
