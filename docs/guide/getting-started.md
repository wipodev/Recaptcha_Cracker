# Getting Started

Welcome to the Recaptcha Cracker documentation! This guide will help you get up and running with Recaptcha Cracker, a tool designed to automate the resolution of reCAPTCHA v2 and text captchas on web pages.

## Installation

To install Recaptcha Cracker, you'll need Python 3.10+ and pip. You can install the package via pip with the following command:

```bash
pip install recaptcha-cracker
```

## Requirements

Make sure you have the following dependencies installed:

- Seleniumbase
- Pydub
- SpeechRecognition
- EasyOCR
- OpenCV
- Requests
- verbose-terminal

:::warning IMPORTANT
If you're getting an error related to FFmpeg not being installed or in your PATH, get it here: [FFmpeg Download](https://ffmpeg.org/download.html).
if the error persists, Ensure FFmpeg is properly installed for your OS and in your PATH.
:::

## Usage

### Resolving reCAPTCHA V2

1. Import the necessary class to your Python script:

```python
from recaptcha_cracker import RecaptchaV2
```

2. Initialize a RecaptchaV2 object with a SeleniumBase Driver object:

```python
from seleniumbase import Driver

# Inicializa el objeto Driver
driver = Driver()

# Carga la página web
driver.get("https://www.google.com/recaptcha/api2/demo")

# Inicializa el objeto RecaptchaV2
recaptcha = RecaptchaV2(driver)

```

3. Use the cracker() method to resolve a reCAPTCHA on a web page:

```python
checked_status = recaptcha.cracker(selector='//*[@id="recaptcha-demo"]/div/div/iframe')
```

4. If the reCAPTCHA is successfully resolved, the method will return True. Otherwise, it will return False.

### Resolving text captchas

1. Import the necessary class to your Python script:

```python
from recaptcha_cracker import TextCaptcha
```

2. Initialize a TextCaptcha object:

```python
text_captcha = TextCaptcha(image_path='captcha.png', processing=True, kernel=(2, 2), verbose=True)
```

3. Use the `download_and_read_image` method to download and read a captcha image from a URL:

```python
captcha_text = text_captcha.download_and_read_image(url='https://example.com/captcha.png')
```

4. Use the `decode_and_read_image` method to decode and read a base64 encoded captcha image:

```python
base64_image = 'data:image/png;base64,...'
captcha_text = text_captcha.decode_and_read_image(base64_image=base64_image)
```

5. Use the `capture_and_read_image` method to capture and read a captcha image from a web page element:

```python
captcha_text = text_captcha.capture_and_read_image(driver, element='//img[@id="captcha_image"]')
```

6. The methods return the decoded captcha text if successful, or None if there was an error.

## Next Steps

Explore the API Reference for detailed information on all available methods and classes.

If you encounter any issues or have questions, feel free to open an issue on GitHub or consult the Contributing Guide for ways to get involved with the project.

Happy captcha cracking!
