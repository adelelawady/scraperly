from .processor import ContentProcessor, LexicaScraper
import json

def main():
    # Example content
    content = """
    In the realm of artificial intelligence, innovation knows no bounds.
    Each day brings new breakthroughs, pushing the boundaries of what's possible.
    From machine learning to neural networks, the future is being shaped by code.
    """
    
    try:
        # Initialize processor with your API key
        processor = ContentProcessor(
            provider_name="hyperbolic",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZGVsNTBhbGk1MEBnbWFpbC5jb20iLCJpYXQiOjE3Mzg1MTE1Mzd9.q3lmzpYKd5EZTaN2YOf6wKwwUTqAWafcphte5oClzQk",
            max_images_per_segment=3
        )
        
        # Process the content
        print("Processing content...")
        processed_segments = processor.process_content(content)
        
        # Save results with audio and timing information
        print("Saving results...")
        processor.save_processed_content(processed_segments, "processed_content.json")
        
        # Create video with captions
        print("Creating video...")
        processor.create_video("processed_content.json", "output_with_captions.mp4")
        
        # Print results
        for i, segment in enumerate(processed_segments, 1):
            print(f"\nSegment {i}:")
            print(f"Text: {segment.text}")
            print(f"Keywords: {segment.keywords}")
            print(f"Number of images: {len(segment.images)}")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if 'processor' in locals():
            processor.scraper.close()

if __name__ == "__main__":
    main() 