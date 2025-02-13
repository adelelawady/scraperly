# Scraperly

Scraperly is a Python package that combines web scraping capabilities with AI-powered content processing. It provides tools for scraping images from Lexica.art and processing content with various AI providers to create AI-narrated videos with matching visuals.

## Features

- Text-to-video content generation
- Support for multiple AI providers (Hyperbolic, OpenAI, Anthropic, Ollama)
- Automatic image scraping from Lexica.art
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
2. Scrape relevant images from Lexica.art
3. Generate text-to-speech narration
4. Create a video with the images and narration

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