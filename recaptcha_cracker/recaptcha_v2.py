from selenium.common.exceptions import TimeoutException, NoSuchElementException
from seleniumbase import Driver
from .utils import AudioManager
import time
from verbose_terminal import console

class RecaptchaV2:
  def __init__(self, driver: Driver, attempts: int = 3):
    self.driver = driver
    self.attempts = attempts

  def cracker(self, selector: str):
    try:
      iframe_captcha = self.driver.wait_for_element('xpath', selector)
      self.driver.switch_to.frame(iframe_captcha)
      self.driver.click('#recaptcha-anchor-label')
      if self._check_recaptcha():
        return True
      if not self._handle_audio_recaptcha():
        return False
      self.driver.switch_to.frame(iframe_captcha)
      return self._check_recaptcha()
    except (TimeoutException, NoSuchElementException) as e:
      console.error(f"Error solving captcha: {e}")
      return False

  def _handle_audio_recaptcha(self):
        try:
            iframe_captcha_audio = self.driver.wait_for_element('xpath', '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]')
            self.driver.switch_to.frame(iframe_captcha_audio)
            self.driver.click('#recaptcha-audio-button')
            return self._solve_audio_recaptcha()
        except (TimeoutException, NoSuchElementException) as e:
            console.error(f"Error when handling the audio captcha: {e}")
            return False
        finally:
            self.driver.switch_to.parent_frame()

  def _solve_audio_recaptcha(self):
    for _ in range(self.attempts):
      try:
        url = self._get_attribute('.rc-audiochallenge-tdownload-link', 'href')
        if url is None:
          return False
        recognized_text = AudioManager(url).get_audio_transcript()
        self.driver.press_keys('#audio-response', f'{recognized_text}\n')
        if self.driver.is_element_visible('.rc-audiochallenge-error-message'):
          console.error("Error detected, trying again...")
        else:
          return True
      except Exception as e:
        console.error(f"Error solving audio captcha: {e}")
        return False
    console.error(f"Could not resolve audio captcha after {self.attempts} attempts.")
    return False

  def _check_recaptcha(self):
    try:
      time.sleep(1)
      return self._get_attribute('#recaptcha-anchor', 'aria-checked') == 'true'
    except (TimeoutException, NoSuchElementException) as e:
      console.error(f"Error checking the captcha: {e}")
      return False
    finally:
      self.driver.switch_to.parent_frame()

  def _get_attribute(self, selector: str, attribute: str, type: str = None) -> str:
    try:
      if type is None:
        return self.driver.wait_for_element(selector).get_attribute(attribute)
      else:
        return self.driver.wait_for_element(type, selector).get_attribute(attribute)
    except (TimeoutException, NoSuchElementException) as e:
      console.error(f"Error getting attribute: {e}")
      return None