from setuptools import setup, find_packages


setup(
    name='recaptcha-cracker',
    version='0.0.1',
    author='Wipodev',
    author_email='ajwipo@gmail.com',
    description='RecaptchaCracker is a tool designed to automate reCAPTCHA v2 resolution on web pages using Selenium. Allows you to resolve audio captchas, making it easy to integrate into web automation workflows.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wipodev/Recaptcha_Cracker',
    project_urls={
        'Documentation': 'https://github.com/wipodev/Recaptcha_Cracker/blob/main/README.md',
        'Source': 'https://github.com/wipodev/Recaptcha_Cracker',
        'Bug Tracker': 'https://github.com/wipodev/Recaptcha_Cracker/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='MIT',
    keywords='python, captcha, speech recognition, selenium, web automation',
    packages=find_packages(exclude=('tests*', 'testing*', 'test*')),
    install_requires=[
        'seleniumbase=4.25.4',
        'pydub=0.25.1',
        'SpeechRecognition=3.10.3',
    ],
)