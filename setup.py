from setuptools import setup, find_packages


setup(
    name='recaptcha-cracker',
    version='0.0.1',
    license='MIT',
    author='Wipodev',
    author_email='ajwipo@gmail.com',
    packages=find_packages(exclude=('tests*', 'testing*')),
    keywords='python, captcha, speech recognition, selenium, web automation',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'seleniumbase'
    ],
)