from verbose_terminal import console
from typing import Optional
import easyocr
import requests
import base64
import cv2
import re

class TextCaptcha:

  def __init__(self, image_path: str = 'captcha.png', session = None, processing: bool = True, kernel: tuple = (2, 2), verbose: bool = True):
    self.image_path = image_path
    self.session = session or requests.session()
    self.processing = processing
    self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    self.verbose = verbose

  def download_and_read_image(self, url: str) -> Optional[str]:
      try:
        response = self.session.get(url)
        with open(self.image_path, 'wb') as f:
            f.write(response.content)
        console.success(f"Image downloaded successfully: {self.image_path}", self.verbose)
        return self._read_image()
      except Exception as e:
        console.error(f"Error downloading image: {e}")
        return None

  def decode_and_read_image(self, base64_image: str) -> Optional[str]:
    try:
      image_bytes = base64.b64decode(base64_image.split('base64,')[1])
      with open(self.image_path, 'wb') as f:
        f.write(image_bytes)
      console.success(f"Image decoded successfully: {self.image_path}", self.verbose)
      return self._read_image()
    except Exception as e:
      console.error(f"Error decoding image: {e}")
      return None

  def capture_and_read_image(self, driver, element: str) -> Optional[str]:
    console.info(f'Getting image element: {element}', self.verbose)
    try:
      image = driver.wait_for_element(element, "xpath")
      console.info('Capturing image...', self.verbose)
      image.screenshot(self.image_path)
      console.success(f'Captured image saved at: {self.image_path}', self.verbose)
      return self._read_image()
    except Exception as e:
      console.error(f'Error capturing image: {e}')
      return None

  def _read_image(self) -> Optional[str]:
      image_path = self._process_image(self.image_path) if self.processing else self.image_path
      if image_path:
        return self._read_image_easyocr(image_path)
      return None

  def _process_image(self, img: str) -> Optional[str]:
      try:
        console.info(f'Processing image: {img}', self.verbose)
        image = cv2.imread(img)
        if image is None: 
          console.error(f"FileNotFoundError: Could not read the image {img}")
          return None
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, tozero_image = cv2.threshold(image_gray, 127, 255, cv2.THRESH_TOZERO)
        _, binary_image = cv2.threshold(tozero_image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, self._kernel)
        file_output = img.replace('.png', '_processed.png')
        cv2.imwrite(file_output, processed_image)
        console.success(f'Processed image saved at: {file_output}', self.verbose)
        return file_output
      except Exception as e:
        console.error(f'Error processing image: {e}')
        return None

  def _read_image_easyocr(self, img: str) -> Optional[str]:
    reader = easyocr.Reader(['en', 'es'], gpu=False)
    try:
      results = reader.readtext(img)
      if results:
        raw_text = results[0][1]
        return self._clean_alphanumeric_text(raw_text)
      return None
    except Exception as e:
      console.error(f'Error reading image: {e}')
      return None

  def _clean_alphanumeric_text(self, raw_text: str) -> str:
      console.info(f'formatting text: {raw_text}', self.verbose)
      formatted_text = re.sub(r'[^a-zA-Z0-9]', '', raw_text)    
      console.success(f'Formatted text: {formatted_text}', self.verbose)
      return formatted_text