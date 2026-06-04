from langdetect import detect
from deep_translator import GoogleTranslator

def translate_text(text, source_lang, target_lang):
    try:
        translated = GoogleTranslator(
            source=source_lang,
            target=target_lang
        ).translate(text)

        return translated

    except Exception as e:
        return f"Error: {str(e)}"

def detect_language(text):
    try:
        return detect(text)
    except:
        return None