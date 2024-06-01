from verbose_terminal import console
import cv2

class ImageManager():

  def __init__(self, kernel: tuple = (2, 2), verbose: bool = True):
    self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    self.verbose = verbose

  def screenshot(self, driver, element: str, image_path: str = "image.png") -> bool:
    console.info(f'Getting image element: {element}', self.verbose)
    try:
      image = driver.wait_for_element(element, "xpath")
      console.info('Capturing image...', self.verbose)
      image.screenshot(image_path)
    except Exception as e:
      console.error(f'Error capturing image: {e}')
      return False
    console.success(f'Captured image saved at: {image_path}', self.verbose)
    return True

  def Process_image(self, img: str) -> str:
      try:
        console.info(f'Processing image: {img}', self.verbose)
        image = cv2.imread(img)
        if image is None: console.error(f"FileNotFoundError: Could not read the image {img}")
        image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        _, tozero_image = cv2.threshold(image_gray, 127, 255, cv2.THRESH_TOZERO)
        _, binary_image = cv2.threshold(tozero_image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        processed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, self.kernel)
        file_output = img.replace('.png', f'_processed.png')
        cv2.imwrite(file_output, processed_image)
        console.success(f'Processed image saved at: {file_output}', self.verbose)
        return file_output
      except Exception as e:
        console.error(f'Error processing image: {e}')
        return None

if __name__ == "__main__":
    original = "captcha.png"
    image_manager = ImageManager()
    image_manager.Process_image(original)
