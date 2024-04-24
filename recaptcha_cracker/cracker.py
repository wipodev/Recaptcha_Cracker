from seleniumbase import Driver
from .audio_converter import AudioConverter

class RecaptchaCracker:
  def __init__(self, driver: Driver):
    self.driver = driver

  def click_recaptcha(self, selector: str):
    iframe_captcha = self.driver.wait_for_element('xpath', selector)
    self.driver.switch_to.frame(iframe_captcha)
    
    self.driver.click('#recaptcha-anchor-label')

    if self._get_attribute('#recaptcha-anchor', 'aria-checked') == 'true':
      self.driver.switch_to.default_content()
      return
    
    self.driver.switch_to.parent_frame()
    iframe_captcha_audio = self.driver.wait_for_element('xpath', '//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]')
    self.driver.switch_to.frame(iframe_captcha_audio)

    self.driver.click('#recaptcha-audio-button')
    self._solve_audio_captcha()

  def _solve_audio_captcha(self):
    while True:
      try:
        url = self._get_attribute('.rc-audiochallenge-tdownload-link', 'href')
        converter = AudioConverter(url)
        recognized_text = converter.process()
        self.driver.press_keys('#audio-response', f'{recognized_text}\n')
        e = self.driver.wait_for_element('.rc-audiochallenge-error-message')
        if e:
          print("Error detectado, intentando de nuevo...")
        else:
          break
      except Exception as e:
        print(e)

  def _get_attribute(self, selector: str, attribute: str, type: str = None) -> str:
    if type == None:
      return self.driver.wait_for_element(selector).get_attribute(attribute)
    else:
      return self.driver.wait_for_element(type, selector).get_attribute(attribute)