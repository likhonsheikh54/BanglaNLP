from setuptools import setup, find_packages

setup(
    name="bangla-nlp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt", encoding="utf-8").readlines()
    ],
    entry_points={
        'console_scripts': [
            'bangla-scrape=main:main',
        ],
    }
)
