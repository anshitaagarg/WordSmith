from gtts import gTTS
import io


def text_to_speech(text, lang="en"):

    audio_buffer = io.BytesIO()

    speech = gTTS(
        text=text,
        lang=lang
    )

    speech.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    return audio_buffer