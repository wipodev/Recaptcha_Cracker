# Recaptcha Cracker

[![Github release](https://img.shields.io/github/v/release/wipodev/Recaptcha_Cracker?color=0172ad&logo=github&logoColor=white)](https://github.com/wipodev/Recaptcha_Cracker/releases/latest)
[![PyPI - Version](https://img.shields.io/pypi/v/Recaptcha_Cracker?label=pypi%20release&color=0172ad)](https://pypi.org/project/Recaptcha_Cracker/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/Recaptcha_Cracker?color=0172ad&label=pypi%20downloads)](https://pypi.org/project/Recaptcha_Cracker/)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/wipodev/Recaptcha_Cracker/total?color=0172ad&label=github%20downloads)](https://github.com/wipodev/Recaptcha_Cracker)
[![License](https://img.shields.io/badge/license-MIT-%230172ad)](https://github.com/wipodev/Recaptcha_Cracker/blob/master/LICENSE)

## Description

RecaptchaCracker is a tool designed to automate the resolution of Captchas on web pages using Seleniumbase.
It allows you to solve "reCaptcha v2" captchas using audio transcription, making it easy to integrate into web automation workflows.

## Features

- Automated resolution of reCAPTCHA V2 captchas on web pages.
- Flexible configuration of the number of attempts to solve audio captchas.
- Easy integration into web automation workflows.

## Requirements

- Python 3.10+
- Seleniumbase
- Pydub
- SpeechRecognition
- verbose-terminal

If you're getting an error related to FFmpeg not being installed or in your PATH, get it here: https://ffmpeg.org/download.html
If the error persists, make sure FFmpeg is properly installed for your OS and in your PATH.

## Installation

```bash
pip install recaptcha-cracker
```

## Usage

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

## Contributions

If you'd like to contribute, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is under the MIT License. See the [LICENSE](https://github.com/wipodev/Recaptcha_Cracker/blob/main/LICENSE) file for more details.

## Inspiration

This project was inspired by the project https://github.com/thicccat688/selenium-recaptcha-solver, created by user "thicccat688". The original library provides a robust solution to solve reCAPTCHA v2 challenges using Selenium and speech recognition services. By studying its implementation and design, I was able to better understand how to address captcha resolution challenges in web automation environments.

I thank the team behind selenium-recaptcha-solver for their excellent work and contributions to the open source community.

---
