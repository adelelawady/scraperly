# Scraperly

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
  <a href="https://github.com/adelelawady/scraperly/blob/main/LICENSE">
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

Scraperly is a Python package that combines web scraping capabilities with AI-powered content processing. It provides tools for scraping existing AI-generated images from Lexica.art (note: images are not generated, only scraped from existing ones) and processing content with various AI providers to create AI-narrated videos with matching visuals.

## Features

- Text-to-video content generation
- Support for multiple AI providers (Hyperbolic, OpenAI, Anthropic, Ollama)
- Image scraping from Lexica.art's existing AI-generated image database (no image generation)
- Text-to-speech narration
- Automated video creation
- Customizable image count per segment
- JSON export of processed content

## Installation

You can install Scraperly using pip:
```bash
pip install scraperly
```

Or install from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/adelelawady/scraperly.git
   cd scraperly
   ```

2. Install the package and its dependencies:
   ```bash
   pip install -e .
   ```

3. For AI provider support, install the optional dependencies:
   ```bash
   pip install -e ".[ai]"
   ```


## Input/Output Examples

### Example : Story Content
**Input Text:**
```text
The wind howled through the abandoned streets as Elias tightened his coat around his shoulders. The city had once been alive, filled with laughter and the hum of everyday life, but now only the echoes of the past remained. He stepped over the broken pavement, eyes scanning for any sign of movement. The sun was setting, casting long shadows against the crumbling buildings. He needed to find shelter before nightfall. There was always something lurking in the darkness.
His footsteps echoed as he approached an old bookstore, its windows shattered, pages of forgotten stories scattered across the floor. He pushed the door open carefully, the hinges groaning in protest. Dust hung thick in the air, disturbed only by his breath. Shelves stood like silent sentinels, their contents long since plundered. He made his way toward the back, past fallen books and overturned chairs, and found what he was looking for. A hidden door, half-concealed behind a collapsed shelf.
With effort, he pushed through, stepping into a smaller room, untouched by the chaos outside. A single lantern sat on a desk, its wick dry but intact. He rummaged through his pack, pulling out a match, and struck it against the rough surface of his sleeve. The flame flickered to life, casting dancing shadows along the walls. He exhaled slowly, the brief warmth comforting.
He lowered himself into an old chair, feeling the exhaustion settle into his bones. He had been walking for days, searching for something he wasn't sure existed anymore. A place safe from the nightmares that roamed the world, from the hunger that gnawed at his ribs, from the memories that refused to fade.
Outside, the wind picked up again, rattling the broken glass and whispering secrets through the ruins. He closed his eyes, listening, waiting, knowing that soon, he would have to move again.
```

**Output Video:**
[Video sample will be added]


Note: These examples will be updated with actual content and video samples.

## Quick Start

Here's a simple example to get you started:

```python
from scraperly import scraperly

# Process content using the simplified scraperly function
result = scraperly(
    content="""
    The Rise of Artificial Intelligence
    AI has transformed various industries, from healthcare to transportation.
    Machine learning algorithms now power everything from recommendation systems
    to autonomous vehicles, making our lives more efficient and connected.
    """,
    provider_name="openai",
    api_key="your-openai-api-key",
    max_images_per_segment=2,
    output_video_path="ai_video.mp4",
    output_json_path="processed_content.json"
)
```

For more control, you can also use the ContentProcessor directly:

```python
from scraperly import ContentProcessor

# Initialize the processor with OpenAI
processor = ContentProcessor(
    provider_name="openai",
    api_key="your-openai-api-key"
)

# Content to process
content = """
The Rise of Artificial Intelligence
AI has transformed various industries, from healthcare to transportation.
Machine learning algorithms now power everything from recommendation systems
to autonomous vehicles, making our lives more efficient and connected.
"""

# Process the content and create a video
result = processor.process_content(
    content=content,
    max_images_per_segment=2,
    output_video_path="ai_video.mp4",
    output_json_path="processed_content.json"
)

print(f"Video created successfully at: {result['video_path']}")
print(f"Processed content saved at: {result['json_path']}")
```

This example will:
1. Process the input text into segments
2. Scrape relevant existing AI-generated images from Lexica.art (no new images are generated)
3. Generate text-to-speech narration
4. Create a video with the scraped images and narration

## Supported AI Providers

### Hyperbolic AI
- Default model: `deepseek-ai/DeepSeek-V3`
- Available models: `deepseek-v3`, `deepseek-v2`

### OpenAI
- Default model: `gpt-4`
- Available models: `gpt-4`, `gpt-3.5-turbo`, `gpt-4-turbo`

### Anthropic
- Default model: `claude-3-sonnet-20240229`
- Available models: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`

### Ollama (Local)
- Default model: `llama2`
- Available models: `llama2`, `mistral`, `codellama`

## Advanced Usage

### Manual Processing

### Configuration Options

- `content`: Text content to process
- `provider_name`: AI provider to use (`"hyperbolic"`, `"openai"`, `"anthropic"`, `"ollama"`)
- `api_key`: API key for the chosen provider
- `max_images_per_segment`: Maximum number of images per content segment (default: 2)
- `model`: Specific model to use (provider-dependent)
- `output_video_path`: Path for the output video file
- `output_json_path`: Path for the processed content JSON file

## Requirements

- Python 3.9+
- Chrome browser (for web scraping)
- FFmpeg (for video processing)

## Dependencies

Core dependencies:
- requests>=2.31.0
- selenium>=4.15.2
- beautifulsoup4>=4.12.0
- numpy>=1.24.3
- Pillow>=9.5.0
- moviepy>=2.0.0.dev2
- gTTS>=2.3.1
- pydub>=0.25.1

Optional AI dependencies:
- openai>=1.0.0
- anthropic>=0.3.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- adelelawady (adel50ali5@gmail.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Chrome browser is installed
   - Update Chrome to the latest version
   - Check if chromedriver matches your Chrome version

2. **AI Provider Errors**
   - Verify API key is correct
   - Check if chosen model is available for your provider
   - Ensure you have the required AI provider package installed

3. **Video Processing Issues**
   - Verify FFmpeg is installed and accessible
   - Check disk space for temporary files
   - Ensure write permissions in output directory

## Support

For support, please open an issue on the GitHub repository or contact the author directly.


