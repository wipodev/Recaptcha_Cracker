from selenium.common.exceptions import TimeoutException, NoSuchElementException
from seleniumbase import Driver
from recaptcha_cracker.audio_manager import AudioManager
import time

class RecaptchaCracker:
  def __init__(self, driver: Driver, attempts: int = 3):
    self.driver = driver
    self.attempts = attempts

  def click_recaptcha(self, selector: str):
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
      print(f"Error al resolver el captcha: {e}")
      return False

  def _handle_audio_recaptcha(self):
        try:
            iframe_captcha_audio = self.driver.wait_for_element('xpath', '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]')
            self.driver.switch_to.frame(iframe_captcha_audio)
            self.driver.click('#recaptcha-audio-button')
            return self._solve_audio_recaptcha()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error al manejar el captcha de audio: {e}")
            return False
        finally:
            self.driver.switch_to.parent_frame()

  def _solve_audio_recaptcha(self):
    for _ in range(self.attempts):
      try:
        url = self._get_attribute('.rc-audiochallenge-tdownload-link', 'href')
        if url == '':
          return False
        recognized_text = AudioManager(url).get_audio_transcript()
        self.driver.press_keys('#audio-response', f'{recognized_text}\n')
        if self.driver.is_element_visible('.rc-audiochallenge-error-message'):
          print("Error detectado, intentando de nuevo...")
        else:
          return True
      except Exception as e:
        print(f"Error al resolver el captcha de audio: {e}")
        return False
    print(f"No se pudo resolver el captcha de audio después de {self.attempts} intentos.")
    return False

  def _check_recaptcha(self):
    try:
      time.sleep(1)
      return self._get_attribute('#recaptcha-anchor', 'aria-checked') == 'true'
    except (TimeoutException, NoSuchElementException) as e:
      print(f"Error al chequear el captcha: {e}")
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
      print(f"Error al obtener el atributo: {e}")
      return ""