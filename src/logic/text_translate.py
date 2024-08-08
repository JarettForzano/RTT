from googletrans import Translator

def translate_text(text, target_language='ja'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text