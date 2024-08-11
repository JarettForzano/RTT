from deep_translator import GoogleTranslator

def translate_text(text, target_language='ja'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(text)
    return translation