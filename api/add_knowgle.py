from fastapi import APIRouter, UploadFile, File
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
import os
import shutil
import tempfile
import uvicorn
from utils.pdf import PyPDFLoaderCustom
from vector_database.index_qdrant import add_to_qdrant

from dotenv import load_dotenv
_ = load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
router  = APIRouter()
@router .post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Create temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, file.filename)
        
        # Save uploaded file temporarily
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Load document based on file type
        if file.filename.endswith('.txt'):
            loader = TextLoader(temp_path)
        elif file.filename.endswith('.pdf'):
            loader = PyPDFLoaderCustom(temp_path, extract_images=True)
        elif file.filename.endswith('.docx'):
            loader = Docx2txtLoader(temp_path)
        else:
            return {"error": "Unsupported file format"}
        
        # Load and split the document
        documents = loader.load()
        text_splitter = SemanticChunker(embeddings, min_chunk_size = 100)
        texts = text_splitter.split_documents(documents)
        add_to_qdrant(texts, "langchain", embedding_model=embeddings)
        return {
            "message": "Document embedded successfully",
            "filename": file.filename,
            "chunks": len(texts)
        }
