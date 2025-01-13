from dotenv import load_dotenv
_ = load_dotenv()

# load data from pdf
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from vector_database.index_qdrant import add_to_qdrant
from utils.pdf import PyPDFLoaderCustom

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

loader = PyPDFLoaderCustom(
    "2101.03961v3.pdf",
    extract_images=True,
)
documents = loader.load()
print(documents)
text_splitter = SemanticChunker(embeddings, min_chunk_size = 100)
# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=1000, 
#         chunk_overlap=200, 
#         model_name="gpt-3.5"
#     )
texts = text_splitter.split_documents(documents)
print(texts)
add_to_qdrant(texts, "langchain", embedding_model=embeddings)
