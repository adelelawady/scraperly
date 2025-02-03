"""
This is a scraper for Lexica.art to extract image information and metadata
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import urllib.parse

class LexicaScraper:
    def __init__(self, image_limit=10, headless=True):
        self.base_url = "https://lexica.art/"
        self.image_limit = image_limit
        self.headless = headless
        self.initialize_driver()
        
    def initialize_driver(self):
        """Initialize or reinitialize the Chrome driver"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-logging')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        
    def ensure_driver_active(self):
        """Ensure the driver is active, reinitialize if necessary"""
        try:
            # Try to get the current URL to test if driver is active
            self.driver.current_url
        except:
            print("Reinitializing WebDriver...")
            self.initialize_driver()

    def get_full_resolution_url(self, image_url):
        """Convert medium resolution URL to full resolution"""
        return image_url.replace('md2_webp', 'full_webp')
        
    def wait_for_images_to_load(self):
        """Helper method to ensure images are loaded"""
        try:
            # Wait for grid to be present
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="grid"]'))
            )
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="gridcell"]'))
            )
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img[width="520"]'))
            )
        except Exception as e:
            print(f"Error waiting for images: {str(e)}")

    def extract_modal_data(self):
        """Extract data from the modal view"""
        try:
            # Wait for modal to be visible
            modal = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "fullscreen-modal-overlay"))
            )
            
            # Get the main prompt
            prompt = ""
            try:
                prompt_element = modal.find_element(By.CSS_SELECTOR, 'div.mt-6 p a')
                prompt = prompt_element.text
            except:
                print("Main prompt not found in modal")

            # Get the model info
            model = ""
            try:
                model_element = modal.find_element(By.CSS_SELECTOR, 'div.text-sm')
                model = model_element.text
            except:
                print("Model info not found in modal")

            # Get the full resolution image URL
            image_url = ""
            try:
                img_element = modal.find_element(By.CSS_SELECTOR, 'img.relative.z-20')
                image_url = img_element.get_attribute('src')
            except:
                print("Full resolution image not found in modal")

            # Get dimensions
            dimensions = ""
            try:
                dim_element = modal.find_elements(By.CSS_SELECTOR, 'div.text-sm')[1]
                dimensions = dim_element.text
            except:
                print("Dimensions not found in modal")

            # Close modal using ESC key
            webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            
            return {
                'prompt': prompt,
                'model': model,
                'image_url': image_url,
                'dimensions': dimensions
            }
            
        except Exception as e:
            print(f"Error extracting modal data: {str(e)}")
            return None
        
    def search_and_scrape(self, search_query):
        try:
            self.ensure_driver_active()
            encoded_query = urllib.parse.quote(search_query)
            query_url = f"{self.base_url}?q={encoded_query}"
            
            self.driver.get(query_url)
            self.wait_for_images_to_load()
            
            image_cells = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="gridcell"]')
            image_cells = image_cells[:self.image_limit]
            
            images_data = []
            for index, cell in enumerate(image_cells, 1):
                try:
                    print(f"Processing image {index} of {self.image_limit}...")
                    
                    # Click the cell to open modal
                    cell.click()
                    
                    # Extract data from modal
                    modal_data = self.extract_modal_data()
                    
                    if modal_data:
                        images_data.append(modal_data)
                    
                    if len(images_data) >= self.image_limit:
                        break
                        
                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    continue
            
            return images_data
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            try:
                # Try to reinitialize and retry once
                print("Attempting to recover...")
                self.initialize_driver()
                # Retry the search
                encoded_query = urllib.parse.quote(search_query)
                query_url = f"{self.base_url}?q={encoded_query}"
                self.driver.get(query_url)
                self.wait_for_images_to_load()
                # ... rest of the scraping logic ...
            except Exception as retry_error:
                print(f"Recovery failed: {str(retry_error)}")
                return []
        return []  # Return empty list if all attempts fail

    def save_results(self, images_data, filename='lexica_results.json'):
        """Save the scraped results to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(images_data, f, indent=4, ensure_ascii=False)

    def close(self):
        """Close the browser"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
        except:
            pass  # Ignore errors during close

    def __del__(self):
        """Destructor to ensure browser is closed"""
        self.close()

def main():
    scraper = LexicaScraper(image_limit=30, headless=True)  # Default to headless
    search_query = '{subject} in the style of futuristic robots...'
    results = scraper.search_and_scrape(search_query)
    
    if results:
        scraper.save_results(results)
        print(f"Found {len(results)} images. Results saved to lexica_results.json")
    else:
        print("No results found or an error occurred")

if __name__ == "__main__":
    main()

