import requests
from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr
from verbose_terminal import console

class AudioManager:
    def __init__(self, url, verbose: bool = True):
        self.url = url
        self.verbose = verbose

    def download_audio(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            return None

    def convert_to_wav(self, audio_bytes):
        audio = AudioSegment.from_file(audio_bytes)
        if audio:
            wav_audio = audio.set_frame_rate(44100).set_channels(1)
            return wav_audio
        else:
            return None

    def save_audio(self, audio, output_file):
        audio.export(output_file, format="wav")

    def recognize_speech(self, audio_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="en-US")
                return text
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None

    def get_audio_transcript(self, output_file="output.wav"):
        audio_bytes = self.download_audio()
        if audio_bytes:
            wav_audio = self.convert_to_wav(audio_bytes)
            if wav_audio:
                self.save_audio(wav_audio, output_file)
                console.info(f"Saved WAV file: {output_file}", self.verbose)

                recognized_text = None
                try:
                    recognized_text = self.recognize_speech(output_file)
                    if recognized_text:
                        console.success(f"Recognized text: {recognized_text}", self.verbose)
                    else:
                        console.error("Could not understand the audio.")
                except Exception as e:
                    console.critical(f"Error: {str(e)}.")
                finally:
                    return recognized_text
            else:
                console.error("Could not convert file to WAV.")
        else:
            console.error("Error downloading the audio file.")
