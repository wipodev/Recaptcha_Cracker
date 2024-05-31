import pytest
from seleniumbase import Driver
from recaptcha_cracker import RecaptchaV2

@pytest.fixture
def driver():
    driver = Driver(uc=True)
    yield driver
    driver.quit()

def test_recaptcha_cracker(driver):
    recaptcha = RecaptchaV2(driver=driver)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    assert recaptcha.cracker('//*[@id="recaptcha-demo"]/div/div/iframe') == True
