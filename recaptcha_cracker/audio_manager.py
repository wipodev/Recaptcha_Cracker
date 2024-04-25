import requests
from pydub import AudioSegment
from io import BytesIO
import speech_recognition as sr

class AudioManager:
    def __init__(self, url):
        self.url = url

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
                print(f"Archivo WAV guardado: {output_file}")

                recognized_text = None
                while not recognized_text:
                    try:
                        recognized_text = self.recognize_speech(output_file)
                        if recognized_text:
                            print(f"Texto reconocido: {recognized_text}")
                        else:
                            print("No se pudo entender el audio. Intentando de nuevo...")
                    except Exception as e:
                        print(f"Error: {str(e)}. Intentando de nuevo...")
                return recognized_text
            else:
                print("No se pudo convertir el archivo a WAV.")
        else:
            print("Error al descargar el archivo de audio.")

# Ejemplo de uso
if __name__ == "__main__":
    url = "URL_DEL_AUDIO_AQUÍ"

    print(AudioManager(url).get_audio_transcript())
