import os
import tempfile
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

_ = load_dotenv()

# load data from pdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from vector_database.index_qdrant import add_to_qdrant
from utils.pdf import PyPDFLoaderCustom
from langchain_community.document_loaders import (
    Docx2txtLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
MARKDOWN_SEPARATORS = [
        "\n#{1,6} ",
        "```\n",
        "\n\\*\\*\\*+\n",
        "\n---+\n",
        "\n___+\n",
        "\n\n",
        "\n",
        " ",
        "",
    ]

def process_file(uploaded_file, st, embeddings):
    temp_dir = "D:/NCKH/LLM/Langchain/upload_file"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as buffer:
        buffer.write(uploaded_file.getvalue())

    if uploaded_file.name.endswith(".txt"):
        loader = TextLoader(temp_path)
    elif uploaded_file.name.endswith(".pdf"):
        loader = PyPDFLoaderCustom(temp_path, extract_images=False)
    elif uploaded_file.name.endswith(".docx"):
        loader = Docx2txtLoader(temp_path)
    elif uploaded_file.name.endswith(".doc"):
        loader = UnstructuredWordDocumentLoader(temp_path)
    else:
        st.error("Unsupported file format")
        return
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        # is_separator_regex=False,
        separators=[
            "\n\n",
            "\n",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
        # Existing args
    )
    # text_splitter = SemanticChunker(
    #     embeddings=embeddings,
    #     breakpoint_threshold_type="gradient",
    #     min_chunk_size= 200,
    # )
    texts = text_splitter.split_documents(documents)
    add_to_qdrant(texts, "langchain", embedding_model=embeddings)
    st.success(
        f"Document '{uploaded_file.name}' embedded successfully with {len(texts)} chunks."
    )
