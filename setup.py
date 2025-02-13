from setuptools import setup, find_packages
import io

# Update the README reading part
with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="scraperly",
    version="2.0.1",
    packages=find_packages(),
    install_requires=[
        # Core dependencies
        "requests>=2.31.0",
        "urllib3>=2.0.0",
        
        # Web Scraping
        "selenium>=4.15.2",
        "beautifulsoup4>=4.12.0",
        
        # Audio/Video Processing
        "numpy>=1.24.3",
        "Pillow>=9.5.0,<11.0",
        "decorator>=4.4.2",
        "imageio>=2.31.1",
        "imageio-ffmpeg>=0.4.8",
        "proglog>=0.1.10",
        "tqdm>=4.65.0",
        "moviepy>=2.0.0.dev2",
        "gTTS>=2.3.1",
        "pydub>=0.25.1",
    ],
    extras_require={
        'ai': [
            "openai>=1.0.0",
            "anthropic>=0.3.0",
        ],
    },
    python_requires=">=3.9",
    author="adelelawady",
    author_email="adel50ali5@gmail.com",
    description="A tool for processing content into AI-generated videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ai, video, content, processing",
    url="https://github.com/adelelawady/scraperly",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
) 