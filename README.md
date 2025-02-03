# AI Art Style Scraper

A Python-based web scraping tool that collects art style information and example images from various AI art platforms including Freeflo.ai and Lexica.art.

## Features

- Scrapes art styles and example images from Freeflo.ai
- Collects style-specific keywords and metadata
- Gathers image data from Lexica.art
- Saves results in JSON format
- Headless browser operation support

## Prerequisites

- Python 3.7+
- Chrome/Firefox WebDriver
- Selenium WebDriver

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-art-style-scraper.git
   cd ai-art-style-scraper
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the appropriate WebDriver for your browser:
   - [ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (for Firefox)

## Usage

1. Configure the scraper settings in `main.py`:
   ```python
   HEADLESS_MODE = True  # Set to False if you want to see the browser
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

The script will:
- Scrape art styles and images from Freeflo.ai
- Collect associated keywords and metadata
- Gather relevant images from Lexica.art
- Save all data in JSON format

## Project Structure
```python
ai-art-style-scraper/
├── main.py # Main script
├── freefloScraper.py # Freeflo main scraper
├── freefloStyleScraper.py # Freeflo style details scraper
├── LexicaScraper.py # Lexica.art scraper
├── requirements.txt # Project dependencies
└── README.md # Documentation

```


## Output Files

The script generates several JSON files:
- `freeflo_results.json`: Contains art styles and images from Freeflo.ai
- `lexica_results.json`: Contains image data from Lexica.art
- `combined_results.json`: Merged and processed data from both sources

Example output structure:

```json
{
"style_name": "Style Name",
"style_link": "https://freeflo.ai/style/...",
"images": [...],
"keywords": [...]
}
```

## Error Handling

The scraper includes:
- Timeout handling for slow-loading pages
- Automatic retries for failed requests
- Graceful error handling for missing elements
- Browser cleanup on script completion

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational purposes only. Please:
- Review and comply with the terms of service of target websites
- Respect robots.txt directives
- Implement appropriate rate limiting
- Do not use scraped data for commercial purposes without permission

## Support

For support, please:
1. Check existing issues
2. Create a new issue with a detailed description
3. Include relevant error messages and screenshots

## Acknowledgments

- Selenium WebDriver team
- BeautifulSoup4 developers
- Freeflo.ai and Lexica.art for their services