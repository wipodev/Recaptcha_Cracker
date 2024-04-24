from recaptcha_cracker import RecaptchaCracker
from seleniumbase import Driver

def test_click_recaptcha():
    driver = Driver(uc=True)
    driver.get("https://www.google.com/recaptcha/api2/demo")
    cracker = RecaptchaCracker(driver=driver)
    cracker.click_recaptcha(selector='//*[@id="recaptcha-demo"]/div/div/iframe')
    input("Press Enter to continue...")