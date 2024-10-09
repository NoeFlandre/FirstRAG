# Streamlit App with Retrieval-Augmented Generation (RAG)

This repository contains a **Streamlit application** that demonstrates a Retrieval-Augmented Generation (RAG) workflow. This guide will walk you through the steps to set up your environment, install the required packages, and run the app.

## Prerequisites

Before you begin, make sure you have the following installed on your system:
- **Python 3.8+**
- **pip** (Python package installer)

For **Windows** users, ensure you have [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed if you're working with packages that require C++ compilation (e.g., `chromadb`).

## Setting Up the Environment

It’s best to use a **virtual environment** to keep your dependencies isolated. Follow these steps to create and activate the environment:

### 1. Clone the Repository

```bash
git clone https://github.com/NoeFlandre/FirstRAG.git
cd FirstRAG
```

### 2. Create a Virtual Environment

#### For Windows:
```bash
python -m venv myenv
```

#### For macOS/Linux:
```bash
python3 -m venv myenv
```

### 3. Activate the Virtual Environment

#### For Windows:
```bash
myenv\Scripts\activate
```

#### For macOS/Linux:
```bash
source myenv/bin/activate
```

Once activated, you should see the environment name (`myenv`) in your terminal prompt.

## Installing Requirements

After activating the virtual environment, install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If you encounter any issues with the installation (especially on Windows), you may need to install the [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## Running the Streamlit App

To run the Streamlit app, use the following command:

```bash
streamlit run app.py
```

This will start a local development server. Open the provided URL (usually `http://localhost:8501`) in your browser to view the app.

## Troubleshooting

- **Missing C++ Build Tools (Windows)**: If you encounter errors during installation related to building wheels (like `chroma-hnswlib`), ensure that you have installed [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
- **Vector Store Issues**: If the project relies on a vector store (e.g., `chroma` or `faiss`), ensure that it’s either included or regenerated as described in the project documentation. Large data files should be excluded from GitHub and can be generated or downloaded as needed.

## Deactivating the Virtual Environment

Once you're done, you can deactivate the virtual environment with:

```bash
deactivate
```