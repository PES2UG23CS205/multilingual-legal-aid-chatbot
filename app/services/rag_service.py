# app/services/rag_service.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, LLMChain

# --- CONFIGURATION ---
VECTOR_STORE_PATH = "vector_store"
# ---> CHANGE 2: Using the same superior embedding model for consistency <---
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "mistral"

# --- LOAD MODELS AND VECTOR STORE ---
print("🧠 RAG Service: Loading models...")
try:
    print(f"   - Embedding Model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    print(f"   - Vector Store: {VECTOR_STORE_PATH}")
    vector_store = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
    
    print(f"   - LLM: {LLM_MODEL}")
    llm = Ollama(model=LLM_MODEL)
    print(f"✅ RAG Service: Models loaded successfully.")
except Exception as e:
    print(f"❌ RAG Service: Critical error loading models: {e}")
    raise


# --- PROMPT ENGINEERING ---

# ---> CHANGE 3: New, extremely strict RAG prompt to prevent hallucinations <---
RAG_PROMPT_TEMPLATE = """
[INST]
**Your Core Directives:**
1.  **You are a factual legal assistant. Your ONLY task is to answer the user's question based *exclusively* on the Legal Text provided below.**
2.  **CRITICAL RULE: Your entire response MUST be derived from the Legal Text. DO NOT use any outside knowledge. DO NOT make assumptions. DO NOT add any information not present in the text.**
3.  If the answer to the question is not found in the Legal Text, you MUST respond with the exact phrase: "I cannot find the answer to that question in the provided document." You are not allowed to say anything else in that case.
4.  Present the answer in simple, clear terms.

**Legal Text:**
---
{context}
---

**User's Question:**
{question}
[/INST]
Answer based ONLY on the Legal Text:
"""
RAG_PROMPT = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


# This General Chat prompt remains the same from our previous fix.
GENERAL_PROMPT_TEMPLATE = """
[INST]
You are a friendly and helpful conversational AI assistant named 'Sahayak'.

**Your Core Rules:**
1.  **Be Natural:** Behave like a kind, natural person. Do not be overly robotic or formal. Keep your answers concise.
2.  **Handle Greetings:** If the user's message is a greeting (like "hello", "hi", "good morning", "good evening", etc.), you MUST respond with a simple, friendly greeting in return. DO NOT immediately ask what you can do for them. First, return the greeting.
3.  **Answer Questions:** If the user's message is a question, answer it directly and helpfully.

**Examples of Correct Behavior:**
User: good morning
Sahayak: Good morning to you too! How can I help?

User: hello there
Sahayak: Hello! What can I do for you today?

User: who are you?
Sahayak: I am Sahayak, an AI assistant designed to help with legal information and general questions.

**Now, apply these rules to the user's actual message:**
User: {question}
[/INST]
Sahayak:
"""
GENERAL_PROMPT = PromptTemplate.from_template(GENERAL_PROMPT_TEMPLATE)

# --- CREATE THE CHAINS ---
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
    chain_type_kwargs={"prompt": RAG_PROMPT}
)
general_chain = LLMChain(llm=llm, prompt=GENERAL_PROMPT)

def get_response(query: str, mode: str):
    """
    Gets a response from the appropriate chain based on the selected mode.
    """
    print(f"🔍 Querying in '{mode}' mode with LLM '{LLM_MODEL}'. Query: '{query}'")
    try:
        if mode == "Legal Aid (RAG)":
            response = rag_chain.invoke({"query": query})
            return {"answer": response.get("result", "No answer found.")}
        else: # General Chat
            response = general_chain.invoke({"question": query})
            return {"answer": response.get("text", "I am not sure how to respond.")}
    except Exception as e:
        print(f"❌ Error during chain invocation: {e}")
        return {"error": str(e)}