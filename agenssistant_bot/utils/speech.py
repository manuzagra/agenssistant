import io
import logging

import speech_recognition as sr
from pydub import AudioSegment

logger = logging.getLogger(__name__)

# Initialize the recognizer
_recognizer = sr.Recognizer()


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
            try:
                audio_data = _recognizer.record(source)
                text = _recognizer.recognize_google(audio_data)
            except sr.UnknownValueError:
                logger.error("Speech Recognition could not understand the audio")
                return None
            except Exception as e:
                logger.error(f"Speech Recognition raised the following error: {e}")
                raise e

    return text
