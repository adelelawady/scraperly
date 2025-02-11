from freefloScraper import FreefloScraper
from freefloStyleScraper import FreefloStyleScraper
from LexicaScraper import LexicaScraper
import json
import os
import time

# Global configuration
HEADLESS_MODE = True  # Can be changed to False to see the browser

def process_lexica_results(freeflo_results):
    """Process Lexica results for each FreeFlo style"""
    combined_results = []
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            lexica_scraper = LexicaScraper(image_limit=10, headless=HEADLESS_MODE)
            
            # Process each FreeFlo style
            for style in freeflo_results:
                style_name = style['style_name']
                style_link = style['style_link']
                
                # Keep original FreeFlo images and keywords
                freeflo_images = style.get('images', [])
                style_keywords = style.get('keywords', [])
                
                # Create search query from style keywords
                search_query = ' '.join(style_keywords[:3])  # Use first 3 keywords
                print(f"Searching Lexica for style '{style_name}' with query: {search_query}")
                
                # Search Lexica with style keywords
                lexica_images = []
                try:
                    lexica_results = lexica_scraper.search_and_scrape(search_query)
                    
                    # Get up to 2 related images from Lexica results
                    for lexica_item in lexica_results[:10]:
                        image_data = {
                            "src": lexica_item['image_url'],
                            "alt": style_name,
                            "prompt": lexica_item.get('prompt', ''),
                            "dimensions": lexica_item.get('dimensions', '')
                        }
                        lexica_images.append(image_data)
                        
                except Exception as e:
                    print(f"Error searching Lexica for {style_name}: {e}")
                    continue
                
                # Create combined result
                combined_style = {
                    "style_name": style_name,
                    "style_link": style_link,
                    "images": freeflo_images,
                    "lexica_images": lexica_images,
                    "keywords": style_keywords
                }
                
                combined_results.append(combined_style)
            
            # If we get here without errors, break the retry loop
            break
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print("Retrying...")
                time.sleep(2)  # Wait before retrying
            else:
                print("Max retries reached")
        finally:
            try:
                lexica_scraper.close()
            except:
                pass
    
    # Save combined results
    with open('combined_results.json', 'w', encoding='utf-8') as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)
    
    return combined_results

if __name__ == "__main__":
    scraper = FreefloScraper(headless=HEADLESS_MODE)
    try:
        # Example search term
        results = scraper.search_and_scrape("adventure video game immersive quests fantasy adventure game")
        scraper.save_results()
        style_scraper = FreefloStyleScraper(headless=HEADLESS_MODE)
        style_scraper.scrape_from_results()
        
        # Process Lexica results
        freeflo_results = []
        if os.path.exists('freeflo_results.json'):
            with open('freeflo_results.json', 'r') as f:
                freeflo_results = json.load(f)
        
        combined_results = process_lexica_results(freeflo_results)
        print(f"Found {len(combined_results)} styles with combined Lexica results")
        
    finally:
        scraper.close()