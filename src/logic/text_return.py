import asyncio
import time
import os
from dotenv import load_dotenv 
load_dotenv() 

Deepgram_key = os.getenv("DEEPGRAM_API_KEY")

from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
    DeepgramClientOptions,
)

class TranscriptCollector:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.reset()

    def reset(self):
        self.transcript_parts = []
        self.start_time = None
        self.end_time = None

    def add_part(self, part):
        if not self.start_time:  
            self.start_time = time.time()
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        self.end_time = time.time()
        return ' '.join(self.transcript_parts)

transcript_collector = TranscriptCollector()

async def voice_to_text(api_key):
    try:
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram: DeepgramClient = DeepgramClient(api_key, config)
        dg_connection = deepgram.listen.asyncwebsocket.v("1")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            
            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                duration = transcript_collector.end_time - transcript_collector.start_time

                print(f"speaker: [{duration}] {full_sentence}")
                transcript_collector.reset()



        async def on_error(self, error, **kwargs):
            print(f"Handled Error: {error}")

        async def on_unhandled(self, unhandled, **kwargs):
            print(f"Unhandled Websocket Message: {unhandled}")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        # options needed for best quality
        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            smart_format=True,
            channels=1,
            sample_rate=16000,
            endpointing=True
        )

        addons = {
            "no_delay": "true"
        }

        await dg_connection.start(options, addons=addons)

        microphone = Microphone(dg_connection.send)

        microphone.start()

        while True:
            if not microphone.is_active():
                break
            await asyncio.sleep(1)

        microphone.finish()

        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return
