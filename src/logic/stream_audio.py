import os
from dotenv import load_dotenv
from elevenlabs import generate, play
load_dotenv()

Labs_Key = os.getenv("LABS")

# Generate audio from text
audio = generate(text="Hello, this is a test", voice="Rachel")

# Play the audio
play(audio)
