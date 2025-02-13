# Scraperly 🎬 

<p align="center">
  <img src="https://github.com/user-attachments/assets/d2acb889-33a8-4eed-9c24-18b4693e5cfc" alt="Logo" width="200">
</p>

<p align="center">
  <a href="https://pypi.org/project/scraperly/">
    <img src="https://img.shields.io/pypi/v/scraperly.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/scraperly/">
    <img src="https://img.shields.io/pypi/pyversions/scraperly.svg" alt="Python versions">
  </a>
  <a href="https://github.com/adelelawady/scraperly/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/adelelawady/scraperly.svg" alt="License">
  </a>
  <a href="https://github.com/adelelawady/scraperly/stargazers">
    <img src="https://img.shields.io/github/stars/adelelawady/scraperly.svg" alt="GitHub stars">
  </a>
  <a href="https://github.com/adelelawady/scraperly/issues">
    <img src="https://img.shields.io/github/issues/adelelawady/scraperly.svg" alt="GitHub issues">
  </a>
  <a href="https://pepy.tech/project/scraperly">
    <img src="https://static.pepy.tech/badge/scraperly" alt="Downloads">
  </a>
</p>

> Transform your text into captivating AI-narrated videos with matching visuals! 🚀

Scraperly is your all-in-one Python toolkit for creating engaging AI-powered videos. It seamlessly combines web scraping, AI content processing, and video generation to turn your text into professional-looking videos with minimal effort.

## 📚 Table of Contents
- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Installation](#️-installation)
- [🎯 Use Cases](#-use-cases)
- [🛠️ Advanced Usage](#️-advanced-usage)
- [🤖 AI Providers](#-ai-providers)
- [🔧 Troubleshooting](#-troubleshooting)
- [👥 Contributing](#-contributing)
- [📝 License](#-license)

## ✨ Features

- 🎥 **One-Click Video Creation**: Transform text into professional videos
- 🤖 **Multiple AI Providers**: Choose from OpenAI, Anthropic, Hyperbolic, or Ollama
- 🖼️ **Smart Image Scraping**: Automatic image sourcing from Lexica.art
- 🗣️ **Natural Narration**: High-quality text-to-speech conversion
- ⚡ **Fast Processing**: Efficient content segmentation and processing
- 🎨 **Customizable Output**: Control image count and video parameters

## 🚀 Quick Start

```python
from scraperly import scraperly
import os

# Create your first AI video in just 3 lines!
result = scraperly(
    content="Your story or content here",
    provider_name="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4"
)
```

## ⚙️ Installation

### 📦 Using pip (Recommended)
```bash
# Basic installation
pip install scraperly

# With AI provider support
pip install "scraperly[ai]"

# Set up your API keys (recommended)
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 🔧 From Source
```bash
# Clone and install
git clone https://github.com/adelelawady/scraperly.git
cd scraperly
pip install -e ".[ai]"
```

## 🎯 Use Cases

### 1. Story Visualization
```python
from scraperly import scraperly
import os

# Turn a story into an engaging video
story = """
The ancient castle stood silently against the twilight sky,
its weathered stones holding centuries of secrets...
"""

result = scraperly(
    content=story,
    provider_name="anthropic",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-sonnet",
    max_images_per_segment=3
)
```

### 2. Educational Content
```python
from scraperly import scraperly
import os

# Create educational videos
lesson = """
The Solar System consists of eight planets orbiting around the Sun.
Each planet has unique characteristics...
"""

result = scraperly(
    content=lesson,
    provider_name="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4-turbo",
    max_images_per_segment=2,
    output_video_path="solar_system.mp4"
)
```

## 🤖 AI Providers

| Provider | Default Model | Available Models | Features |
|----------|--------------|------------------|-----------|
| OpenAI | `gpt-4` | All OpenAI chat models (e.g., `gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`, etc.) | Best for creative content |
| Anthropic | `claude-3-sonnet` | All Claude models (e.g., `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`, etc.) | Excellent analysis |
| Hyperbolic | `deepseek-v3` | All Deepseek models (e.g., `deepseek-v3`, `deepseek-v2`, etc.) | Fast processing |
| Ollama | `llama2` | All Ollama models (e.g., `llama2`, `mistral`, `codellama`, etc.) | Local execution |

## 🔧 Troubleshooting

<details>
<summary>🚫 Chrome Driver Issues</summary>

- ✅ Update Chrome to latest version
- ✅ Verify matching chromedriver version
- ✅ Check system PATH configuration
</details>

<details>
<summary>❌ AI Provider Errors</summary>

- ✅ Verify API key validity
- ✅ Check provider status
- ✅ Confirm model availability
</details>

<details>
<summary>⚠️ Video Processing Issues</summary>

- ✅ Install/update FFmpeg
- ✅ Check disk space
- ✅ Verify file permissions
</details>

## 🤝 Contributing

We love your input! To contribute:

1. 🍴 Fork the repo
2. 🌿 Create your branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 Push to branch (`git push origin feature/AmazingFeature`)
5. 🎁 Open a Pull Request

## 📝 License

Released under MIT License. See [LICENSE](LICENSE) for details.

## 👤 Author

Created with 💖 by [adelelawady](mailto:adel50ali5@gmail.com)

---

<p align="center">
  Made with ❤️ for the AI community
</p>


