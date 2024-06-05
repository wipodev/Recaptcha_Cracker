import pytest
from seleniumbase import Driver
from recaptcha_cracker import RecaptchaV2
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture
def driver():
    driver = Driver(uc=True)
    yield driver
    driver.quit()

def test_integration_cracker(driver):
    recaptcha = RecaptchaV2(driver)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    try:
        driver.wait_for_element_visible('//*[@id="recaptcha-demo"]/div/div/iframe')
        result = recaptcha.cracker('//*[@id="recaptcha-demo"]/div/div/iframe')
        assert result is True, "reCAPTCHA should be solved successfully"
    except TimeoutException as e:
        pytest.fail(f"Timeout exception occurred: {e}")
    except NoSuchElementException as e:
        pytest.fail(f"No such element exception occurred: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected exception occurred: {e}")
