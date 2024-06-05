import pytest
from unittest.mock import patch, mock_open, MagicMock
import base64
import requests
import cv2
from recaptcha_cracker import TextCaptcha

@pytest.fixture
def captcha():
    return TextCaptcha(image_path='test_captcha.png', processing=True, kernel=(2, 2), verbose=False)

def test_download_and_read_image(captcha, mocker):
    mock_get = mocker.patch('requests.get')
    mockOpen = mocker.patch('builtins.open', mock_open())
    mock_read_image = mocker.patch.object(TextCaptcha, '_read_image')

    mock_get.return_value.content = b'image data'
    mock_read_image.return_value = 'sample_text'
    
    result = captcha.download_and_read_image('http://example.com/captcha.png')
    
    mock_get.assert_called_once_with('http://example.com/captcha.png')
    mockOpen.assert_called_once_with('test_captcha.png', 'wb')
    assert result == 'sample_text'

def test_decode_and_read_image(captcha, mocker):
    mock_b64decode = mocker.patch('base64.b64decode')
    mockOpen = mocker.patch('builtins.open', mock_open())
    mock_read_image = mocker.patch.object(TextCaptcha, '_read_image')

    base64_image = 'data:image/png;base64,somebase64data'
    mock_b64decode.return_value = b'image data'
    mock_read_image.return_value = 'sample_text'

    result = captcha.decode_and_read_image(base64_image)

    mock_b64decode.assert_called_once_with('somebase64data')
    mockOpen.assert_called_once_with('test_captcha.png', 'wb')
    assert result == 'sample_text'

def test_capture_and_read_image(captcha, mocker):
    mock_read_image = mocker.patch.object(TextCaptcha, '_read_image')
    mock_driver = MagicMock()
    mock_element = MagicMock()
    mock_driver.wait_for_element.return_value = mock_element
    mock_read_image.return_value = 'sample_text'

    result = captcha.capture_and_read_image(mock_driver, "//img[@id='captcha']")

    mock_driver.wait_for_element.assert_called_once_with("//img[@id='captcha']", "xpath")
    mock_element.screenshot.assert_called_once_with('test_captcha.png')
    assert result == 'sample_text'

def test_process_image(captcha, mocker):
    mock_imread = mocker.patch('cv2.imread')
    mock_cvtColor = mocker.patch('cv2.cvtColor')
    mock_threshold = mocker.patch('cv2.threshold')
    mock_morphologyEx = mocker.patch('cv2.morphologyEx')
    mock_imwrite = mocker.patch('cv2.imwrite')

    mock_imread.return_value = MagicMock()
    mock_cvtColor.return_value = MagicMock()
    mock_threshold.side_effect = [(None, MagicMock()), (None, MagicMock())]
    mock_morphologyEx.return_value = MagicMock()
    mock_imwrite.return_value = True

    result = captcha._process_image('test_captcha.png')

    mock_imread.assert_called_once_with('test_captcha.png')
    mock_cvtColor.assert_called_once()
    assert mock_threshold.called
    mock_morphologyEx.assert_called_once()
    mock_imwrite.assert_called_once()
    assert result == 'test_captcha_processed.png'

def test_read_image_easyocr(captcha, mocker):
    mock_readtext = mocker.patch('easyocr.Reader.readtext')
    
    mock_readtext.return_value = [(None, 'sample_text')]
    
    result = captcha._read_image_easyocr('test_captcha.png')

    mock_readtext.assert_called_once_with('test_captcha.png')
    assert result == 'sampletext'

def test_clean_alphanumeric_text(captcha):
    raw_text = 'This is a test! 1234'
    expected_result = 'Thisisatest1234'

    result = captcha._clean_alphanumeric_text(raw_text)

    assert result == expected_result
