import pytest
from seleniumbase import Driver
from recaptcha_cracker import TextCaptcha
import requests
import os

IMAGE_TEST_URL = 'https://www.wipodev.com/Recaptcha_Cracker'

@pytest.fixture
def driver():
    driver = Driver(uc=True)
    yield driver
    driver.quit()

def test_integration_download_and_read_image():
    captcha = TextCaptcha(verbose=False)
    try:
        result = captcha.download_and_read_image(f'{IMAGE_TEST_URL}/assets/test_image.PslyHsGX.png')
        assert result is not None, "The image should be processed and read successfully."
        assert len(result) == 6, "The decoded image should contain 6 characters."
        assert result == '66532f', "The decoded image should contain the '66532f'."
    except Exception as e:
        pytest.fail(f"An unexpected exception occurred: {e}")

def test_integration_decode_and_read_image():
    captcha = TextCaptcha(processing=False)
    response = requests.get(f'{IMAGE_TEST_URL}/assets/test_image1.json')
    base64_image = response.json()['d']
    try:
        result = captcha.decode_and_read_image(base64_image)
        assert result is not None, "The image should be decoded and read successfully."
        #assert len(result) == 6, "The decoded image should contain 6 characters."
        #assert result == '658600', "The decoded image should be '658600'."
    except Exception as e:
        pytest.fail(f"An unexpected exception occurred: {e}")

def test_integration_capture_and_read_image(driver):
    captcha = TextCaptcha(verbose=False)
    driver.get(f"{IMAGE_TEST_URL}/tests")
    element_xpath = '//*[@id="VPContent"]/div/div/div[2]/div/main/div/div/p[3]/img'
    try:
        result = captcha.capture_and_read_image(driver, element_xpath)
        assert result is not None, "The image should be captured and read successfully."
        assert len(result) == 6, "The decoded image should contain 6 characters."
        #assert result == 'phv83e', "The decoded image should be 'phv83e'."
    except Exception as e:
        pytest.fail(f"An unexpected exception occurred: {e}")