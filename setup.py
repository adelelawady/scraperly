from setuptools import setup, find_packages

setup(
    name="scraperly",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium',
        'gtts',
        'pydub',
        'moviepy',
        'pillow',
        'numpy'
    ],
    author="Adel Elawady",
    author_email="adel50ali50@gmail.com",
    description="A package for scraping and processing content with AI integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adelelawady/scraperly",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 