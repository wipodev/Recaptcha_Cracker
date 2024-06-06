# Reference

Welcome to the API Reference for Recaptcha Cracker. This section provides detailed information about the classes and methods available in the Recaptcha Cracker library.

## RecaptchaV2

### Class: `RecaptchaV2`

A class designed to handle the resolution of reCAPTCHA v2 challenges using audio transcription.

#### Initialization

```python
RecaptchaV2(driver)
```

- `driver` (SeleniumBase Driver): A SeleniumBase Driver object used to interact with the web page.

### Methods

`cracker(selector: str, max_attempts: int = 3) -> bool`

Attempts to resolve a reCAPTCHA v2 challenge on the web page.

- `selector` (str): The XPath selector for the reCAPTCHA iframe element.

- `max_attempts` (int, optional): The maximum number of attempts to solve the captcha. Default is 3.

Returns: `bool` - `True` if the reCAPTCHA is successfully resolved, otherwise `False`.

### Example Usage

```python
from seleniumbase import Driver
from recaptcha_cracker import RecaptchaV2

driver = Driver()
driver.get("https://www.google.com/recaptcha/api2/demo")
recaptcha = RecaptchaV2(driver)
is_solved = recaptcha.cracker(selector='//*[@id="recaptcha-demo"]/div/div/iframe')
```

## TextCaptcha

### Class: `TextCaptcha`

A class designed to handle the resolution of text captchas using EasyOCR and OpenCV.

#### Initialization

```python
TextCaptcha(image_path: str = 'captcha.png', processing: bool = True, kernel: tuple = (2, 2), verbose: bool = True)
```

- `image_path` (str, optional): The path to the captcha image. Default is 'captcha.png'.

- `processing` (bool, optional): Whether to perform image processing on the captcha image. Default is True.

- `kernel` (tuple, optional): The kernel size for image processing. Default is (2, 2).

- `verbose` (bool, optional): Whether to print verbose output. Default is True.

### Methods

`download_and_read_image(url: str) -> Optional[str]`

Downloads a captcha image from a URL and reads its text.

- `url` (str): The URL of the captcha image.

Returns: `Optional[str]` - The decoded text from the captcha image or `None` if an error occurs.

`decode_and_read_image(base64_image: str) -> Optional[str]`

Decodes a base64 encoded captcha image and reads its text.

`base64_image` (str): The base64 encoded captcha image.

Returns: `Optional[str] `- The decoded text from the captcha image or `None` if an error occurs.

`capture_and_read_image(driver, element: str) -> Optional[str]`

Captures a captcha image from a web page element and reads its text.

- `driver` (SeleniumBase Driver): A SeleniumBase Driver object used to interact with the web page.

`element` (str): The XPath selector for the captcha image element.

Returns: `Optional[str]` - The decoded text from the captcha image or None if an error occurs.

### Example Usage

```python
from seleniumbase import Driver
from recaptcha_cracker import TextCaptcha

driver = Driver()
driver.get("https://example.com")

text_captcha = TextCaptcha()
captcha_text = text_captcha.capture_and_read_image(driver, element='//img[@id="captcha_image"]')
```

---

This reference covers the core functionalities of Recaptcha Cracker, providing detailed descriptions of the classes and methods available. For more examples and advanced usage, please refer to the Guides section.
