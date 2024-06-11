# Changelog

## [0.0.1] - 2024-04-25

### added

- Initial release of `Recaptcha_cracker`.
- Added functionality for solving reCAPTCHA v2.

## [0.1.0] - 2024-05-30

### added

- Added `verbose-terminal` package.

### changed

- restructured the entire package

### bugfixes

- Fixed the infinite loop that occurred in the "get_audio_transcript" method

## [0.2.0] - 2024-06-05

### added

- added TextCaptcha module.
- added vitepress package.
- added gh-pages package.
- added tests for TextCaptcha module.

### changed

- modified recaptchav2 unit tests

## [0.2.1] - 2024-06-11

### added

- Support for Custom Session in TextCaptcha:
  - TextCaptcha now accepts an existing session object, ensuring consistent sharing of cookies and headers across different parts of the application.
  - This enhancement improves the integration of TextCaptcha with other modules that rely on session-based interactions.

### Fixed

- Captcha Validation Consistency:
  - Ensured that the same session is used for downloading and reading captcha images, resolving issues with incorrect captcha validation due to session inconsistencies.

### Instructions to Update

```bash
pip install -U recaptcha-cracker
```
