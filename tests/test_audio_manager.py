import pytest
from recaptcha_cracker.utils import AudioManager
from unittest.mock import patch, Mock

@pytest.fixture
def audio_manager():
    url = "http://example.com/audio.mp3"
    return AudioManager(url)

def test_download_audio(audio_manager):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'audio data'
        mock_get.return_value = mock_response

        audio_bytes = audio_manager.download_audio()
        assert audio_bytes is not None

def test_convert_to_wav(audio_manager):
    with patch('pydub.AudioSegment.from_file') as mock_from_file:
        mock_audio_segment = Mock()
        mock_audio_segment.set_frame_rate.return_value = mock_audio_segment
        mock_audio_segment.set_channels.return_value = mock_audio_segment
        mock_from_file.return_value = mock_audio_segment

        audio_bytes = b'audio data'
        wav_audio = audio_manager.convert_to_wav(audio_bytes)
        assert wav_audio is not None

def test_save_audio(audio_manager):
    with patch('pydub.AudioSegment') as mock_audio_segment:
        mock_audio = Mock()
        mock_audio.export.return_value = None

        audio_manager.save_audio(mock_audio, "output.wav")
        mock_audio.export.assert_called_with("output.wav", format="wav")

def test_recognize_speech(audio_manager):
    with patch('speech_recognition.Recognizer') as MockRecognizer:
        mock_recognizer = MockRecognizer.return_value
        mock_recognizer.record.return_value = "audio data"
        mock_recognizer.recognize_google.return_value = "recognized text"

        audio_file = "output.wav"
        recognized_text = audio_manager.recognize_speech(audio_file)
        assert recognized_text == "recognized text"

def test_get_audio_transcript(audio_manager):
    with patch.object(audio_manager, 'download_audio', return_value=b'audio data'), \
         patch('pydub.AudioSegment.from_file') as mock_from_file, \
         patch.object(audio_manager, 'save_audio', return_value=None), \
         patch.object(audio_manager, 'recognize_speech', return_value="recognized text"):
        
        mock_audio_segment = Mock()
        mock_audio_segment.set_frame_rate.return_value = mock_audio_segment
        mock_audio_segment.set_channels.return_value = mock_audio_segment
        mock_from_file.return_value = mock_audio_segment

        recognized_text = audio_manager.get_audio_transcript()
        assert recognized_text == "recognized text"
