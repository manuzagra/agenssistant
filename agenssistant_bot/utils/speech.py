import io

import speech_recognition as sr
from pydub import AudioSegment

# Initialize the recognizer
recognizer = sr.Recognizer()


async def convert_voice_to_text(voice_bytes_ogg: bytearray) -> str:
    """This functions convert the audio from a voice message to text.

    Args:
        voice_bytes_ogg (bytearray): voice file stored in a bytearray in ogg format.

    Returns:
        str: The transcription of the audio.
    """
    with io.BytesIO(voice_bytes_ogg) as audio_stream:
        audio = AudioSegment.from_file(audio_stream, format="ogg")

        wav_stream = io.BytesIO()
        audio.export(wav_stream, format="wav")
        wav_stream.seek(0)

        with sr.AudioFile(wav_stream) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

    return text
