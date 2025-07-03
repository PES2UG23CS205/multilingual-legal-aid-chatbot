# app/main.py
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import JSONResponse
from typing import Optional
import json
import base64

from .services import rag_service, translation_service, audio_service, location_service

# ---> THIS IS THE "app" OBJECT THAT THE ERROR WAS MISSING <---
app = FastAPI(
    title="Full-Featured Legal Aid Chatbot API",
    version="2.0.0"
)

@app.post("/v2/chat")
async def chat_endpoint(
    text_query: Optional[str] = Form(None),
    language: str = Form("en"),
    mode: str = Form("General Chat"),
    audio_file: Optional[UploadFile] = File(None)
):
    """
    Handles text and audio queries, translation, and dual-mode chat.
    """
    query_text = text_query
    
    if audio_file:
        audio_bytes = await audio_file.read()
        if audio_bytes:
            query_text = audio_service.transcribe_audio(audio_bytes)
    
    if not query_text:
        raise HTTPException(status_code=400, detail="No query provided.")
        
    english_query = query_text
    if language != "en":
        english_query = translation_service.translate_text(query_text, 'en', language)

    llm_response = rag_service.get_response(english_query, mode)
    if "error" in llm_response:
        raise HTTPException(status_code=500, detail=llm_response["error"])

    english_answer = llm_response.get("answer", "")
    
    final_answer = english_answer
    if language != "en":
        final_answer = translation_service.translate_text(english_answer, language, 'en')

    audio_response_bytes = audio_service.text_to_speech(final_answer, language)
    audio_response_base64 = base64.b64encode(audio_response_bytes).decode('utf-8')

    return JSONResponse(content={
        "text_answer": final_answer,
        "audio_answer_base64": audio_response_base64
    })


@app.get("/find_aid_centers")
def find_aid_centers(city: str):
    """Endpoint to find legal aid centers by city."""
    centers = location_service.find_centers(city)
    if not centers:
        return {"message": f"No legal aid centers found for {city}."}
    return centers

@app.get("/health")
def health_check():
    """A simple endpoint to confirm the server is running."""
    return {"status": "ok", "version": "2.0.0"}