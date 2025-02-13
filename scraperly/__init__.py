from .lexica import LexicaScraper
from .providers import get_ai_provider
from .processor import ContentProcessor

__version__ = "2.0.0"

def scraperly(
    content: str = None,
    provider_name: str = "hyperbolic",
    api_key: str = None,
    max_images_per_segment: int = 2,
    model: str = None,
    output_video_path: str = "output_with_captions.mp4",
    output_json_path: str = "processed_content.json"
) -> ContentProcessor:
    """
    Initialize and process content with the specified AI provider configuration.
    
    Args:
        content (str, optional): The text content to process
        provider_name (str): Name of the AI provider (e.g., 'hyperbolic', 'openai', 'anthropic')
        api_key (str): API key for the specified provider
        max_images_per_segment (int, optional): Maximum number of images per content segment. Defaults to 2.
        model (str, optional): Specific model to use with the provider. If not specified, uses provider's default.
        output_video_path (str, optional): Path for the output video file. Defaults to "output_with_captions.mp4"
        output_json_path (str, optional): Path for the processed content JSON file. Defaults to "processed_content.json"
    
    Returns:
        ContentProcessor: Configured processor ready to handle the content
    
    Raises:
        Exception: If any error occurs during processing
    """
    try:
        # Create the content processor directly with the parameters it expects
        processor = ContentProcessor(
            content=content,
            provider_name=provider_name,
            api_key=api_key,
            model=model,
            max_images_per_segment=max_images_per_segment
        )

        if content:
            # Process the content
            print("Processing content...")
            processed_segments = processor.process_content(content)
            
            # Save results with audio and timing information
            print("Saving results with audio timing...")
            processor.save_processed_content(processed_segments, output_json_path)
            
            # Create video with captions
            print("Creating video with captions...")
            processor.create_video(output_json_path, output_video_path)
            
            print(f"Video created successfully: {output_video_path}")
        
        return processor
    
    except Exception as e:
        print(f"Error in scraperly: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        if 'processor' in locals() and hasattr(processor, 'scraper'):
            processor.scraper.close()

__all__ = ['LexicaScraper', 'get_ai_provider', 'ContentProcessor', 'scraperly'] 