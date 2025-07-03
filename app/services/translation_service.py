# app/services/translation_service.py
from deep_translator import GoogleTranslator

def translate_text(text: str, target_lang: str, source_lang: str = 'auto'):
    """Translates text using Google Translate."""
    if not text:
        return ""
    try:
        # For some languages, Google uses different codes (e.g., Kannada is kn)
        if target_lang == "kn": 
            target_lang = "kn"
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text # Return original text on error