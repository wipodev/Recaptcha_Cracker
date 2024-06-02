from verbose_terminal import console
import easyocr
import requests
import cv2
import re

class TextCaptcha():

  def __init__(self, image_path: str = 'captcha.png', kernel: tuple = (2, 2), verbose: bool = True):
    self.image_path = image_path
    self._kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    self.verbose = verbose

  def read_download_image(url: str):
      try:
        response = requests.get(url)
        with open(self.image_path, 'wb') as f:
            f.write(response.content)
        console.success(f"Image downloaded successfully: {self.image_path}", self.verbose)
        return self._read_image()
      except Exception as e:
        console.error(f"Error downloading image: {e}")
        return False

  def read_screenshot(self, driver, element: str):
    console.info(f'Getting image element: {element}', self.verbose)
    try:
      image = driver.wait_for_element(element, "xpath")
      console.info('Capturing image...', self.verbose)
      image.screenshot(self.image_path)
    except Exception as e:
      console.error(f'Error capturing image: {e}')
      return False
    console.success(f'Captured image saved at: {self.image_path}', self.verbose)
    return self._read_image()

  def _read_image(self) -> str:
      route = self._Process_image(self.image_path)
      if route:
        read_text = self._read_image_easyocr()
        if read_text:
          return read_text
        else:
          return None
      else:
        return None

  def _Process_image(self, img: str) -> str:
      try:
        console.info(f'Processing image: {img}', self.verbose)
        image = cv2.imread(img)
        if image is None: console.error(f"FileNotFoundError: Could not read the image {img}")
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, tozero_image = cv2.threshold(image_gray, 127, 255, cv2.THRESH_TOZERO)
        _, binary_image = cv2.threshold(tozero_image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, self._kernel)
        file_output = img.replace('.png', f'_processed.png')
        cv2.imwrite(file_output, processed_image)
        console.success(f'Processed image saved at: {file_output}', self.verbose)
        return file_output
      except Exception as e:
        console.error(f'Error processing image: {e}')
        return None

  def _read_image_easyocr(self, img: str) -> str:
    reader = easyocr.Reader(['en', 'es'], gpu=False)
    try:
      results = reader.readtext(img)
      raw_text = results[0][1]
      return self._clean_alphanumeric_text(raw_text)
    except Exception as e:
      console.error(f'Error reading image: {e}')
      return None

  def _clean_alphanumeric_text(self, raw_text: str, verbose: bool = True) -> str:
      console.info(f'formatting text: {raw_text}', verbose)
      formatted_text = re.sub(r'[^a-zA-Z0-9]', '', raw_text)    
      console.success(f'Formatted text: {formatted_text}', verbose)
      return formatted_text