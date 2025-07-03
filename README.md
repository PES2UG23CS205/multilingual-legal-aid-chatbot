Generated markdown

      
# 🇮🇳 Multilingual Legal Aid Chatbot for Underrepresented Communities

[![GitHub stars](https://img.shields.io/github/stars/PES2UG23CS205/multilingual-legal-aid-chatbot?style=social)](https://github.com/PES2UG23CS205/multilingual-legal-aid-chatbot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/PES2UG23CS205/multilingual-legal-aid-chatbot?style=social)](https://github.com/PES2UG23CS205/multilingual-legal-aid-chatbot/fork)

A socially impactful AI-powered chatbot designed to break down language barriers and make legal information accessible to everyone, especially in rural and non-English speaking communities in India.

  <!-- TODO: Create a short GIF of your app and replace this link! -->

---

## 🧠 The Problem: Bridging the Justice Gap

In India, a vast number of people, particularly in rural areas or those who are not fluent in English, face significant hurdles in understanding their legal rights. Complex legal documents, jargon-filled language, and a lack of awareness create a daunting barrier to justice. This "justice gap" means many are unable to access basic legal help for critical issues like land rights, accessing government schemes (like RTI), or understanding protections against domestic violence.

## 💡 The Solution: An AI-Powered Legal Navigator

This project aims to solve this problem by leveraging Generative AI to act as a friendly, multilingual legal assistant. It's built to be a first point of contact for anyone needing to understand their rights, providing clear, simple, and actionable information.

**What this project does:**
*   **Simplifies Complexity:** Converts dense legal jargon from official documents into simple, easy-to-understand explanations in local languages (Kannada, Telugu, Hindi, Tamil, and more).
*   **Answers Questions:** Users can ask questions in their native language about specific laws, and the chatbot provides accurate answers grounded in official legal documents.
*   **Ensures Accessibility:** Integrates voice input and output, making the tool usable even for individuals with low literacy levels.
*   **Connects to Help:** Optionally recommends nearby free legal aid centers or NGOs for users who need further human assistance.

---

## 🚀 Key Features

*   **Multilingual Support:** Ask questions and receive answers in multiple Indian languages.
*   **Voice-Enabled:** Use your voice to ask questions and listen to the answers—no typing required!
*   **Retrieval-Augmented Generation (RAG):** Answers are not hallucinated; they are generated based on information retrieved from actual government legal documents, ensuring accuracy and reliability.
*   **Beginner-Friendly UI:** A simple and intuitive chat interface built with Streamlit.
*   **Open-Source Core:** Built with powerful, open-source models like Mistral and frameworks like LangChain.

---

## 🛠️ Technology Stack

This project combines a modern stack of AI and web development tools:

*   **Large Language Model (LLM):** **Mistral 7B** (running locally via [Ollama](https://ollama.com/)) for generating human-like, simple explanations.
*   **RAG Framework:** **LangChain** to orchestrate the entire process of retrieving information and generating answers.
*   **Embeddings:** **Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`)** to convert text into numerical vectors for similarity search.
*   **Vector Store:** **ChromaDB** to store and efficiently query the vectorized legal documents.
*   **Translation:** **Google Translate API** (via the `deep-translator` library) for robust multilingual capabilities.
*   **Speech-to-Text:** **OpenAI Whisper** (local model) to accurately transcribe voice inputs from any language.
*   **Text-to-Speech:** **gTTS (Google Text-to-Speech)** to convert the text answers back into audible speech.
*   **Backend API:** **Python** with **FastAPI** for a high-performance, scalable server.
*   **Frontend:** **Streamlit** for rapid development of an interactive and user-friendly web interface.

---

## 📖 How It Works: My Approach

I built this project following a structured, phased approach to ensure a robust and scalable architecture.

1.  **Foundation (The "Brain"):** The core of the project is the RAG pipeline.
    *   **Data Ingestion:** I wrote a script (`scripts/ingest_data_ocr.py`) that can process both text-based and scanned PDF documents. It uses Optical Character Recognition (OCR) with Tesseract to handle scanned files, ensuring that even old government documents can be used.
    *   **Chunking & Embedding:** The script splits the documents into smaller, manageable chunks. Each chunk is then converted into a numerical vector (an "embedding") using a sentence-transformer model.
    *   **Vector Storage:** These embeddings are stored in a ChromaDB vector database. This allows for incredibly fast and efficient searching for relevant information.

2.  **Interaction (The "Mouth and Ears"):**
    *   When a user asks a question (in any language, via text or voice), the following happens:
        1.  **Transcribe (if voice):** Whisper converts the audio to text.
        2.  **Translate to English:** The user's query is translated to English, as the core RAG system is optimized for it.
        3.  **Retrieve:** The system searches the ChromaDB database to find the most relevant text chunks from the original legal document.
        4.  **Augment & Generate:** The user's question and the retrieved chunks are passed to the Mistral LLM with a specific prompt, instructing it to answer simply and without jargon.
        5.  **Translate Back:** The generated English answer is translated back to the user's original language.
        6.  **Synthesize (for voice output):** gTTS converts the final text answer into speech.

3.  **Interface (The "Face"):**
    *   A **FastAPI backend** serves the entire logic through a clean API.
    *   A **Streamlit frontend** provides the chat interface, language selection, and buttons for voice input/output, making it easy for anyone to use.

---

## 🎯 Challenges I Overcame

Building this project involved solving several real-world challenges:

*   **Handling Scanned PDFs:** Many government documents are old, scanned images, not text. `PyPDFLoader` failed on these. I solved this by building a robust ingestion pipeline using **PyMuPDF** to extract pages as images and **Tesseract OCR** to recognize the text, making the system compatible with almost any PDF.
*   **Ensuring Factual Accuracy:** LLMs can "hallucinate" or make up facts. I implemented the **RAG** pattern to ground the model's responses in actual text from legal documents, dramatically improving the reliability of the answers.
*   **Low-Resource Languages:** I designed the system to be language-agnostic. By translating user input to a high-resource language (English) for the core processing and then translating the output back, I could effectively support multiple Indian languages without needing separate models for each.
*   **Real-time Performance:** The full pipeline (STT -> Translate -> RAG -> Translate -> TTS) can be slow. I chose lightweight local models like Whisper's `base` model and fast frameworks like FastAPI to keep the response time as low as possible.

---

## ⚙️ How to Run This Project Locally

Follow these steps to get the chatbot running on your own machine.

### Prerequisites

*   Python 3.9+
*   [Git](https://git-scm.com/)
*   [Ollama](https://ollama.com/) installed and running.
*   Tesseract-OCR Engine installed on your system (see instructions [here](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)).

### 1. Clone the Repository

```bash
git clone https://github.com/PES2UG23CS205/multilingual-legal-aid-chatbot.git
cd multilingual-legal-aid-chatbot

    

IGNORE_WHEN_COPYING_START
Use code with caution. Markdown
IGNORE_WHEN_COPYING_END
2. Set Up a Virtual Environment

It's highly recommended to use a virtual environment.
Generated bash

      
# Create the environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END
3. Install Dependencies

Install all the required Python packages.
Generated bash

      
pip install -r requirements.txt

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END
4. Download the LLM

Pull the Mistral model using Ollama. This will download the model to your machine.
Generated bash

      
ollama pull mistral

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END
5. Ingest Your Data

Place your legal PDF document(s) inside the data/ folder. Then, run the ingestion script to process them and create the vector store.
Generated bash

      
python scripts/ingest_data_ocr.py

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

This might take a few minutes depending on the size of your document. You only need to do this once per document.
6. Run the Application

You need to run the backend and frontend in two separate terminals.

Terminal 1: Start the FastAPI Backend
Generated bash

      
uvicorn app.main:app --reload

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Terminal 2: Start the Streamlit Frontend
Generated bash

      
streamlit run frontend/app.py

    

IGNORE_WHEN_COPYING_START
Use code with caution. Bash
IGNORE_WHEN_COPYING_END

Now, open your web browser and go to http://localhost:8501. You should see the chatbot interface live!
📬 Contact

I'm passionate about using technology for social good and am always open to connecting with like-minded people. If you have any questions, feedback, or want to collaborate, please feel free to reach out!

    Name: [Your Name]

    Email: [your.email@example.com]

    LinkedIn: [https://linkedin.com/in/yourprofile]

    GitHub: [https://github.com/PES2UG23CS205]
