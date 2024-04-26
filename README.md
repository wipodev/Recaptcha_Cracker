# Recaptcha Cracker [![Python](https://img.shields.io/pypi/v/recaptcha-cracker.svg)](https://pypi.org/project/recaptcha-cracker/)

## Description

RecaptchaCracker is a tool designed to automate reCAPTCHA v2 resolution on web pages using Selenium.
Allows you to resolve audio captchas, making it easy to integrate into web automation workflows.

## Features

- Automated resolution of reCAPTCHA captchas on web pages.
- Flexible configuration of the number of attempts for solving audio captchas.
- Easy integration into web automation workflows.

## Requirements

- Python 3.10+
- Seleniumbase
- Pydub
- SpeechRecognition

If you're getting an error related to FFmpeg not being installed or in your PATH, get it here: https://ffmpeg.org/download.html
If the error persists, make sure FFmpeg is properly installed for your OS and in your PATH.

## Installation

```bash
pip install recaptcha-cracker
```

## Usage

1. Import the RecaptchaCracker class into your Python script:

```python
from recaptcha_cracker import RecaptchaCracker
```

2. Initialize a RecaptchaCracker object with a SeleniumBase Driver object:

```python
from seleniumbase import Driver

# Inicializa el objeto Driver
driver = Driver()

# Carga la página web
driver.get("https://www.google.com/recaptcha/api2/demo")

# Inicializa el objeto RecaptchaCracker
cracker = RecaptchaCracker(driver)

```

3. Use the click_recaptcha() method to resolve a reCAPTCHA on a web page:

```python
checked_status = cracker.click_recaptcha(selector='//*[@id="recaptcha-demo"]/div/div/iframe')
```

4. If the reCAPTCHA is successfully resolved, the method will return True. Otherwise, it will return False.

## Contributions

If you'd like to contribute, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is under the MIT License. See the [LICENSE](https://github.com/wipodev/Recaptcha_Cracker/blob/main/LICENSE) file for more details.

## Inspiration

This project was inspired by the project https://github.com/thicccat688/selenium-recaptcha-solver, created by user "thicccat688". The original library provides a robust solution to solve reCAPTCHA v2 challenges using Selenium and speech recognition services. By studying its implementation and design, I was able to better understand how to address captcha resolution challenges in web automation environments.

I thank the team behind selenium-recaptcha-solver for their excellent work and contributions to the open source community.

---
