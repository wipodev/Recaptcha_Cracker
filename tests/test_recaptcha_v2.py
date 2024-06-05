import pytest
from unittest.mock import MagicMock, patch
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from recaptcha_cracker import RecaptchaV2
from verbose_terminal import console

@pytest.fixture
def setup_recaptcha():
    mock_driver = MagicMock()
    recaptcha = RecaptchaV2(mock_driver)
    return recaptcha, mock_driver

###################################################################################################

def test_cracker_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_driver.wait_for_element.return_value = mock_element
    mock_driver.switch_to.frame.return_value = None
    mock_driver.click.return_value = None
    with patch.object(recaptcha, '_check_recaptcha', side_effect=[False, True]) as mock_check_recaptcha, \
         patch.object(recaptcha, '_handle_audio_recaptcha', return_value=True) as mock_handle_audio:
        result = recaptcha.cracker('xpath_selector')
        assert result is True
        mock_driver.wait_for_element.assert_called_once_with('xpath', 'xpath_selector')
        mock_driver.switch_to.frame.assert_any_call(mock_element)
        mock_driver.click.assert_called_once_with('#recaptcha-anchor-label')
        mock_check_recaptcha.assert_called_with()
        mock_handle_audio.assert_called_once()

def test_cracker_handle_audio_failure(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_driver.wait_for_element.return_value = mock_element
    mock_driver.switch_to.frame.return_value = None
    mock_driver.click.return_value = None
    with patch.object(recaptcha, '_check_recaptcha', return_value=False) as mock_check_recaptcha, \
         patch.object(recaptcha, '_handle_audio_recaptcha', return_value=False) as mock_handle_audio:
        result = recaptcha.cracker('xpath_selector')
        assert result is False
        mock_driver.wait_for_element.assert_called_once_with('xpath', 'xpath_selector')
        mock_driver.switch_to.frame.assert_any_call(mock_element)
        mock_driver.click.assert_called_once_with('#recaptcha-anchor-label')
        mock_check_recaptcha.assert_called_with()
        mock_handle_audio.assert_called_once()

def test_cracker_timeout_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = TimeoutException('Timeout waiting for element')
    result = recaptcha.cracker('xpath_selector')
    assert result is False
    captured = capsys.readouterr()
    assert 'Error solving captcha: Message: Timeout waiting for element' in captured.out

def test_cracker_no_such_element_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = NoSuchElementException('Element not found')
    result = recaptcha.cracker('xpath_selector')
    assert result is False
    captured = capsys.readouterr()
    assert 'Error solving captcha: Message: Element not found' in captured.out

###################################################################################################

def test_handle_audio_recaptcha_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_driver.wait_for_element.return_value = mock_element
    mock_driver.switch_to.frame.return_value = None
    with patch.object(recaptcha, '_solve_audio_recaptcha', return_value=True) as mock_solve_audio:
        result = recaptcha._handle_audio_recaptcha()
        assert result is True
        mock_driver.wait_for_element.assert_called_once_with('xpath', '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]')
        mock_driver.switch_to.frame.assert_called_once_with(mock_element)
        mock_driver.click.assert_called_once_with('#recaptcha-audio-button')
        mock_solve_audio.assert_called_once()
        mock_driver.switch_to.parent_frame.assert_called_once()

def test_handle_audio_recaptcha_timeout_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = TimeoutException('Timeout waiting for element')
    result = recaptcha._handle_audio_recaptcha()
    assert result is False
    captured = capsys.readouterr()
    assert 'Error when handling the audio captcha: Message: Timeout waiting for element' in captured.out
    mock_driver.switch_to.parent_frame.assert_called_once()

def test_handle_audio_recaptcha_no_such_element_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = NoSuchElementException('Element not found')
    result = recaptcha._handle_audio_recaptcha()
    assert result is False
    captured = capsys.readouterr()
    assert 'Error when handling the audio captcha: Message: Element not found' in captured.out
    mock_driver.switch_to.parent_frame.assert_called_once()

def test_handle_audio_recaptcha_solve_audio_failure(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_driver.wait_for_element.return_value = mock_element
    mock_driver.switch_to.frame.return_value = None
    with patch.object(recaptcha, '_solve_audio_recaptcha', return_value=False) as mock_solve_audio:
        result = recaptcha._handle_audio_recaptcha()
        assert result is False
        mock_driver.wait_for_element.assert_called_once_with('xpath', '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]')
        mock_driver.switch_to.frame.assert_called_once_with(mock_element)
        mock_driver.click.assert_called_once_with('#recaptcha-audio-button')
        mock_solve_audio.assert_called_once()
        mock_driver.switch_to.parent_frame.assert_called_once()

###################################################################################################

def test_solve_audio_recaptcha_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.return_value = 'audio_url'
    mock_driver.is_element_visible.side_effect = [False]
    with patch('recaptcha_cracker.utils.AudioManager.get_audio_transcript', return_value='transcript') as mock_transcript:
        result = recaptcha._solve_audio_recaptcha()
        assert result is True
        mock_driver.wait_for_element.assert_called_with('.rc-audiochallenge-tdownload-link')
        mock_driver.press_keys.assert_called_with('#audio-response', 'transcript\n')
        mock_transcript.assert_called_once_with()

def test_solve_audio_recaptcha_fail_no_url(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.return_value = None
    result = recaptcha._solve_audio_recaptcha()
    assert result is False
    mock_driver.wait_for_element.assert_called_with('.rc-audiochallenge-tdownload-link')

def test_solve_audio_recaptcha_error_message(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.return_value = 'audio_url'
    mock_driver.is_element_visible.side_effect = [True, True, True]
    with patch('recaptcha_cracker.utils.AudioManager.get_audio_transcript', return_value='transcript'):
        result = recaptcha._solve_audio_recaptcha()
        assert result is False
        captured = capsys.readouterr()
        assert "Error detected, trying again..." in captured.out
        assert "Could not resolve audio captcha after 3 attempts." in captured.out
        assert mock_driver.press_keys.call_count == 3
        assert mock_driver.is_element_visible.call_count == 3

def test_solve_audio_recaptcha_exception_handling(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.side_effect = Exception('Test exception')
    result = recaptcha._solve_audio_recaptcha()
    assert result is False
    captured = capsys.readouterr()
    assert "Error solving audio captcha: Test exception" in captured.out
    assert mock_driver.press_keys.call_count == 0

def test_solve_audio_recaptcha_partial_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.return_value = 'audio_url'
    mock_driver.is_element_visible.side_effect = [True, False]
    with patch('recaptcha_cracker.utils.AudioManager.get_audio_transcript', return_value='transcript') as mock_transcript:
        result = recaptcha._solve_audio_recaptcha()
        assert result is True
        assert mock_driver.press_keys.call_count == 2
        assert mock_driver.is_element_visible.call_count == 2
        mock_transcript.assert_called_with()

def test_solve_audio_recaptcha_no_transcript(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.return_value.get_attribute.return_value = 'audio_url'
    with patch('recaptcha_cracker.utils.AudioManager.get_audio_transcript', side_effect=Exception('Transcript error')):
        result = recaptcha._solve_audio_recaptcha()
        assert result is False
        captured = capsys.readouterr()
        assert "Error solving audio captcha: Transcript error" in captured.out

###################################################################################################

def test_check_recaptcha_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_element.get_attribute.return_value = 'true'
    mock_driver.wait_for_element.return_value = mock_element
    result = recaptcha._check_recaptcha()
    assert result is True
    mock_driver.wait_for_element.assert_called_once_with('#recaptcha-anchor')
    mock_element.get_attribute.assert_called_once_with('aria-checked')
    mock_driver.switch_to.parent_frame.assert_called_once()

def test_check_recaptcha_failure(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_element.get_attribute.return_value = 'false'
    mock_driver.wait_for_element.return_value = mock_element
    result = recaptcha._check_recaptcha()
    assert result is False
    captured = capsys.readouterr()
    assert 'Error checking the captcha: Could not verify recaptcha state.' in captured.out
    mock_driver.wait_for_element.assert_called_once_with('#recaptcha-anchor')
    mock_element.get_attribute.assert_called_once_with('aria-checked')
    mock_driver.switch_to.parent_frame.assert_called_once()

def test_check_recaptcha_attribute_error(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = TimeoutException('Timeout waiting for element')
    result = recaptcha._check_recaptcha()
    assert result is False
    captured = capsys.readouterr()
    assert 'Error checking the captcha: Could not verify recaptcha state.' in captured.out
    mock_driver.switch_to.parent_frame.assert_called_once()

############################################################################################

def test_get_attribute_success(setup_recaptcha):
    recaptcha, mock_driver = setup_recaptcha
    mock_element = MagicMock()
    mock_element.get_attribute.return_value = 'attribute_value'
    mock_driver.wait_for_element.return_value = mock_element
    attribute_value = recaptcha._get_attribute('.selector', 'attribute')
    assert attribute_value == 'attribute_value'
    mock_driver.wait_for_element.assert_called_once_with('.selector')
    mock_element.get_attribute.assert_called_once_with('attribute')

def test_get_attribute_timeout_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = TimeoutException('Timeout waiting for element')
    attribute_value = recaptcha._get_attribute('.selector', 'attribute')
    assert attribute_value is None
    captured = capsys.readouterr()
    assert 'Error getting attribute: Message: Timeout waiting for element' in captured.out

def test_get_attribute_no_such_element_exception(setup_recaptcha, capsys):
    recaptcha, mock_driver = setup_recaptcha
    mock_driver.wait_for_element.side_effect = NoSuchElementException('Element not found')
    attribute_value = recaptcha._get_attribute('.selector', 'attribute')
    assert attribute_value is None
    captured = capsys.readouterr()
    assert 'Error getting attribute: Message: Element not found' in captured.out
