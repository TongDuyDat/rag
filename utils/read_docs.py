import os
import tempfile
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

_ = load_dotenv()

# load data from pdf
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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

# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# loader = PyPDFLoaderCustom(
#     "2101.03961v3.pdf",
#     extract_images=True,
# )
# documents = loader.load()
# print(documents)
# text_splitter = SemanticChunker(embeddings, min_chunk_size = 100)
# # text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
# #         chunk_size=1000,
# #         chunk_overlap=200,
# #         model_name="gpt-3.5"
# #     )
# texts = text_splitter.split_documents(documents)
# print(texts)
# add_to_qdrant(texts, "langchain", embedding_model=embeddings)


def process_file(uploaded_file, st):
    embeddings  = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
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
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        # is_separator_regex=False,
        separators=[
            "\n\n",
            "\n",
            " ",
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
    texts = text_splitter.split_documents(documents)
    add_to_qdrant(texts, "langchain", embedding_model=embeddings)
    st.success(
        f"Document '{uploaded_file.name}' embedded successfully with {len(texts)} chunks."
    )
