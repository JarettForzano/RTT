from deep_translator import GoogleTranslator

def translate_text(text, target_language='ja'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(text)
    return translation

def correction(text, client):
    translated = translate_text(text)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are going to receive a message in japanese, correct any grammar mistakes and make it sound more casual.\n\nDo not add any more information other then the casual japanese."
            },
            {
                "role": "user",
                "content": translated
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
