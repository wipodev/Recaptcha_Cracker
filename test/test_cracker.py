from recaptcha_cracker import RecaptchaCracker
from seleniumbase import Driver
import pytest

def test_click_recaptcha():
  try:
    driver = Driver(uc=True)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    cracker = RecaptchaCracker(driver=driver)
    checked_status = cracker.click_recaptcha(selector='//*[@id="recaptcha-demo"]/div/div/iframe')

    assert checked_status == True
  except Exception:
    pytest.fail('Failed to automatically resolve ReCAPTCHA.')