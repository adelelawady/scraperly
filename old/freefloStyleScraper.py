import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

class FreefloStyleScraper:
    def __init__(self, headless=True):
        # Initialize Chrome options
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.results = []

    def scrape_style_details(self, style_url, style_name):
        try:
            self.driver.get(style_url)
            
            # Wait for the tags to load and add a small delay
            wait = WebDriverWait(self.driver, 10)
            time.sleep(2)  # Add delay to ensure content loads
            
            # Find all tag elements with the specific class
            tag_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "[class^='StyleHero_prompt_bar_tags_tag']")
            
            # Extract keywords/tags
            keywords = []
            for tag in tag_elements:
                try:
                    # Find p tag directly within the tag element
                    keyword = tag.find_element(By.TAG_NAME, "p").text.strip()
                    if keyword:  # Only add non-empty text
                        keywords.append(keyword)
                except Exception as e:
                    print(f"Error extracting tag: {e}")
            
            print('keywords', keywords)
            style_details = {
                "style_name": style_name,
                "style_url": style_url,
                "keywords": keywords
            }
            
            return style_details
            
        except TimeoutException:
            print(f"Timeout waiting for {style_url} to load")
            return None
        except Exception as e:
            print(f"Error scraping style details: {e}")
            return None

    def scrape_from_results(self, results_file="freeflo_results.json"):
        """Scrape style details and update the original results file"""
        try:
            # Read the existing results
            with open(results_file, 'r', encoding='utf-8') as f:
                styles = json.load(f)
            
            # Scrape and update each style with keywords
            for style in styles:
                style_details = self.scrape_style_details(
                    style["style_link"], 
                    style["style_name"]
                )
                if style_details:
                    # Update the original style dict with keywords
                    style["keywords"] = style_details["keywords"]
            
            # Save the updated results back to the same file
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(styles, f, indent=2, ensure_ascii=False)
            
            return styles
                    
        except Exception as e:
            print(f"Error processing results file: {e}")
            return []

    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    scraper = FreefloStyleScraper(headless=True)  # Default to headless
    try:
        results = scraper.scrape_from_results()
        print(f"Updated {len(results)} styles with keywords")
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 