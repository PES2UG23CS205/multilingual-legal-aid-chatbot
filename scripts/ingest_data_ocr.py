# scripts/ingest.py
import os
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.docstore.document import Document

# --- CONFIGURATION ---
DATA_PATH = "data/rti_act_2005.pdf"
VECTOR_STORE_PATH = "vector_store"
# ---> CHANGE 1: Switched to a superior embedding model for better retrieval accuracy <---
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

def process_pdf_with_ocr(file_path: str) -> list[Document]:
    """
    Processes a PDF, attempting to extract text directly first,
    and falling back to OCR if the text is sparse.
    """
    print(f"🧠 Processing PDF: {file_path}")
    doc = fitz.open(file_path)
    all_documents = []

    for page_num in tqdm(range(len(doc)), desc="Processing PDF pages"):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        page_content = ""
        is_scanned = False
        
        # If direct text extraction yields little text, use OCR.
        if len(text.strip()) < 150:
            is_scanned = True
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            try:
                page_content = pytesseract.image_to_string(img, lang='eng')
            except Exception as e:
                print(f"⚠️ Warning: Tesseract error on page {page_num+1}. Skipping. Error: {e}")
                continue
        else:
            page_content = text

        if page_content:
            metadata = {
                "source": os.path.basename(file_path),
                "page": page_num + 1,
                "is_scanned": is_scanned
            }
            all_documents.append(Document(page_content=page_content, metadata=metadata))
            
    doc.close()
    return all_documents

def main():
    print("🚀 Starting data ingestion process...")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ FATAL ERROR: Document not found at '{DATA_PATH}'. Please add it.")
        return

    documents = process_pdf_with_ocr(DATA_PATH)
    if not documents:
        print(f"❌ No text could be extracted from the document. Halting.")
        return
    print(f"✅ Extracted {len(documents)} pages from the document.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Split document into {len(chunks)} chunks.")

    print(f"🧠 Loading new embedding model: {EMBEDDING_MODEL} (this may download on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print(f"💾 Creating and persisting new, smarter vector store at '{VECTOR_STORE_PATH}'...")
    # This will overwrite the old vector store if it exists
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    
    print("\n🎉 Ingestion with new embedding model complete! The vector store is ready.")

if __name__ == "__main__":
    main()