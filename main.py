import json
import os
import time
import logging
import argparse
from tqdm import tqdm

from freefloScraper import FreefloScraper
from freefloStyleScraper import FreefloStyleScraper
from LexicaScraper import LexicaScraper

# Global configuration
HEADLESS_MODE = True  # Can be changed to False to see the browser

# Set up argument parser
parser = argparse.ArgumentParser(
    description="Run the scraper with optional debug mode."
)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
parser.add_argument(
    "-n", "--no-headless", action="store_true", help="Disable headless mode"
)
args = parser.parse_args()

# Set headless mode and logging based on debug flag
if args.debug:
    HEADLESS_MODE = False
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def process_lexica_results(freeflo_results):
    """Process Lexica results for each FreeFlo style"""
    combined_results = []
    max_retries = 3

    lexica_scraper = None
    logging.info("Starting Lexica results processing...")
    for attempt in tqdm(range(max_retries), desc="Processing Lexica results"):
        try:
            lexica_scraper = LexicaScraper(image_limit=10, headless=HEADLESS_MODE)

            # Process each FreeFlo style
            for style in tqdm(freeflo_results, desc="Processing styles"):
                style_name = style["style_name"]
                style_link = style["style_link"]

                # Keep original FreeFlo images and keywords
                freeflo_images = style.get("images", [])
                style_keywords = style.get("keywords", [])

                # Create search query from style keywords
                search_query = " ".join(style_keywords[:3])  # Use first 3 keywords
                logging.debug(
                    f"Searching Lexica for style '{style_name}' with query: {search_query}"
                )

                # Search Lexica with style keywords
                lexica_images = []
                try:
                    lexica_results = lexica_scraper.search_and_scrape(search_query)

                    # Get up to 2 related images from Lexica results
                    for lexica_item in tqdm(
                        lexica_results[:10], desc="Processing Lexica items"
                    ):
                        image_data = {
                            "src": lexica_item["image_url"],
                            "alt": style_name,
                            "prompt": lexica_item.get("prompt", ""),
                            "dimensions": lexica_item.get("dimensions", ""),
                        }
                        lexica_images.append(image_data)

                except Exception as e:
                    logging.error(f"Error searching Lexica for {style_name}: {e}")
                    continue

                # Create combined result
                combined_style = {
                    "style_name": style_name,
                    "style_link": style_link,
                    "images": freeflo_images,
                    "lexica_images": lexica_images,
                    "keywords": style_keywords,
                }

                combined_results.append(combined_style)

            # If we get here without errors, break the retry loop
            break

        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                logging.info("Retrying...")
                time.sleep(2)  # Wait before retrying
            else:
                logging.error("Max retries reached")
        if lexica_scraper is not None:
            try:
                lexica_scraper.close()
            except:
                pass

    # Save combined results
    with open("combined_results.json", "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)

    return combined_results


if __name__ == "__main__":
    logging.info("Initializing FreefloScraper...")
    scraper = FreefloScraper(headless=HEADLESS_MODE)
    try:
        # Example search term
        logging.info("Starting search and scrape with FreefloScraper...")
        results = scraper.search_and_scrape(
            "adventure video game immersive quests fantasy adventure game"
        )
        logging.info("Saving FreefloScraper results...")
        scraper.save_results()
        style_scraper = FreefloStyleScraper(headless=HEADLESS_MODE)
        logging.info("Scraping styles from FreefloScraper results...")
        style_scraper.scrape_from_results()

        # Process Lexica results
        freeflo_results = []
        if os.path.exists("freeflo_results.json"):
            logging.info("Loading Freeflo results from file...")
            with open("freeflo_results.json", "r") as f:
                freeflo_results = json.load(f)

        logging.info("Processing Lexica results...")
        combined_results = process_lexica_results(freeflo_results)
        logging.info(
            f"Found {len(combined_results)} styles with combined Lexica results"
        )

    except KeyboardInterrupt:
        logging.info("Shutdown requested...exiting")
    finally:
        logging.info("Closing FreefloScraper...")
        scraper.close()
