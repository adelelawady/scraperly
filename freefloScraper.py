import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

class FreefloScraper:
    def __init__(self, headless=True):
        self.base_url = "https://freeflo.ai/styles/search-here"
        # Initialize Chrome options
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.results = []

    def search_and_scrape(self, search_term):
        # Replace spaces with hyphens in search term
        formatted_search = search_term.replace(' ', '-')
        search_url = self.base_url.replace('search-here', formatted_search)
        
        try:
            self.driver.get(search_url)
            
            # Wait for the grid to load
            wait = WebDriverWait(self.driver, 10)
            grid = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[class^='GridColumn_page_wrapper']")))
            
            # Wait additional time for dynamic content
            time.sleep(2)
            
            # Find all style cards using partial class name match
            style_cards = self.driver.find_elements(
                By.CSS_SELECTOR, "[class^='StyleCard_card_wrapper']")
            
            for card in style_cards:
                try:
                    # Extract style name using partial class name match
                    style_name = card.find_element(
                        By.CSS_SELECTOR, "[class^='typography_text_sm__medium']").text
                    
                    # Extract images
                    images = []
                    img_elements = card.find_elements(By.TAG_NAME, "img")
                    
                    for img in img_elements:
                        if img.get_attribute("src"):
                            images.append({
                                "src": img.get_attribute("src"),
                                "alt": img.get_attribute("alt")
                            })
                    
                    # Extract style link using partial class name match
                    style_link = card.find_element(
                        By.CSS_SELECTOR, "[class^='StyleCard_card_link']").get_attribute("href")
                    
                    self.results.append({
                        "style_name": style_name,
                        "style_link": style_link,
                        "images": images
                    })
                    
                except Exception as e:
                    print(f"Error processing card: {e}")
                    continue
                    
        except TimeoutException:
            print("Timeout waiting for page to load")
        except Exception as e:
            print(f"Error during scraping: {e}")
            
        return self.results

    def save_results(self, filename="freeflo_results.json"):
        """Save the scraped results to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

    def close(self):
        """Close the browser"""
        self.driver.quit()

def main():
    scraper = FreefloScraper(headless=True)  # Default to headless
    try:
        results = scraper.search_and_scrape("neon")
        scraper.save_results()
        print(f"Found {len(results)} styles")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
