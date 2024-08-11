import pyaudio
import requests
from dotenv import load_dotenv

load_dotenv()

def stream_audio_labs(text, api_key, voice="en_us_male", rate=16000, virtual_mic_name="BlackHole 2ch"):
    # Set up the PyAudio instance
    p = pyaudio.PyAudio()

    # Find the device index for BlackHole
    device_index = find_device_index(p, virtual_mic_name)

    # Prepare the request to 11labs API
    url = "https://api.11labs.io/v1/text-to-speech"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "voice": voice,
        "rate": rate,
        "text": text
    }

    # Request the audio data from 11labs
    response = requests.post(url, json=payload, headers=headers)
    audio_data = response.content

    # Open the BlackHole stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    output=True,
                    output_device_index=device_index)

    # Stream the audio to the virtual mic
    stream.write(audio_data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

def find_device_index(p, device_name):
    """Find the index of a device by its name"""
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        if device_name in dev_info['name']:
            return i
    raise ValueError(f"Device {device_name} not found")
