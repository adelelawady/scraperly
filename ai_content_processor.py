from typing import List, Dict, Any
import json
from dataclasses import dataclass
from ai_providers import get_ai_provider
from LexicaScraper import LexicaScraper
import random
from gtts import gTTS
from pydub import AudioSegment
import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from captacity_clipify import add_captions

@dataclass
class ContentSegment:
    text: str
    keywords: List[str]
    images: List[Dict[str, Any]]

class ContentProcessor:
    def __init__(
        self,
        provider_name: str = "hyperbolic",
        api_key: str = None,
        model: str = "meta-llama/Llama-3.3-70B-Instruct",
        max_images_per_segment: int = 2
    ):
        self.ai_provider = get_ai_provider(provider_name, api_key, model)
        self.scraper = LexicaScraper(image_limit=5, headless=True)
        self.max_images_per_segment = max_images_per_segment

    def _split_into_segments(self, content: str) -> List[str]:
        """Use AI to split content into logical segments"""
        prompt = """Split the following content into logical segments for a video. 
        Each segment should be a coherent thought or idea that can be illustrated with 1-3 images.
        Format your response as a JSON array of strings. For example:
        ["First segment text here", "Second segment text here", "Third segment text here"]
        
        Content:
        {content}
        """.format(content=content)

        try:
            response = self.ai_provider.get_response(prompt)
            response_content = response['choices'][0]['message']['content']
            
            # Clean up the response content to ensure it's valid JSON
            response_content = response_content.strip()
            if not response_content.startswith('['):
                # If response isn't JSON, try to extract array portion
                import re
                array_match = re.search(r'\[(.*?)\]', response_content, re.DOTALL)
                if array_match:
                    response_content = array_match.group(0)
                else:
                    # If no array found, split by newlines as fallback
                    return [seg.strip() for seg in content.split('\n') if seg.strip()]
            
            segments = json.loads(response_content)
            if not isinstance(segments, list):
                raise ValueError("Response is not a list")
            
            return segments
            
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response: {e}")
            # Fallback: split by sentences or paragraphs
            segments = [seg.strip() for seg in content.split('\n') if seg.strip()]
            return segments
        except Exception as e:
            print(f"Error in split_into_segments: {e}")
            return [content]

    def _generate_keywords(self, segment: str) -> List[str]:
        """Generate relevant keywords for image search based on segment content"""
        prompt = """Generate 5 specific visual keywords or phrases that would work well as image generation prompts.
        Focus on artistic styles, visual elements, and specific imagery that could be found in stock photos or AI art.
        
        Guidelines:
        - Include specific art styles (e.g., 'digital art', 'photorealistic', 'cinematic')
        - Mention specific visual elements (e.g., 'glowing particles', 'dramatic lighting')
        - Avoid abstract concepts unless they have clear visual representations
        - Include setting and environment details
        - Consider composition elements
        
        Format your response as a JSON array of strings. For example:
        ["cinematic urban landscape at night", "glowing digital interface with blue tones", "dramatic portrait with rim lighting"]
        
        Text to generate keywords for:
        {segment}
        """.format(segment=segment)

        try:
            response = self.ai_provider.get_response(prompt)
            response_content = response['choices'][0]['message']['content']
            
            # Clean up the response content
            response_content = response_content.strip()
            if not response_content.startswith('['):
                import re
                array_match = re.search(r'\[(.*?)\]', response_content, re.DOTALL)
                if array_match:
                    response_content = array_match.group(0)
                else:
                    # Fallback keywords that work well with image generation
                    return [
                        "cinematic composition",
                        "high quality digital art",
                        "detailed illustration",
                        "professional photography",
                        "dramatic lighting"
                    ]
            
            keywords = json.loads(response_content)
            if not isinstance(keywords, list):
                raise ValueError("Response is not a list")
            
            # Ensure keywords are image-generation friendly
            enhanced_keywords = []
            for keyword in keywords:
                # Add quality-enhancing prefixes if they're not present
                if not any(term in keyword.lower() for term in ['high quality', 'detailed', 'professional', 'cinematic']):
                    enhanced_keyword = f"high quality {keyword}"
                else:
                    enhanced_keyword = keyword
                enhanced_keywords.append(enhanced_keyword)
            
            return enhanced_keywords[:5]  # Limit to 5 keywords
            
        except json.JSONDecodeError as e:
            print(f"Error parsing AI response for keywords: {e}")
            # Fallback to safe, general image-friendly keywords
            return [
                "high quality digital illustration",
                "cinematic composition",
                "professional photography",
                "detailed artwork",
                "dramatic scene"
            ]
        except Exception as e:
            print(f"Error in generate_keywords: {e}")
            return [
                "high quality illustration",
                "detailed digital art",
                "professional photo",
                "cinematic scene",
                "dramatic composition"
            ]

    def _get_images_for_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Get images from Lexica based on keywords"""
        all_images = []
        
        # Try each keyword until we get enough images
        for keyword in keywords:
            try:
                images = self.scraper.search_and_scrape(keyword)
                all_images.extend(images)
                
                if len(all_images) >= self.max_images_per_segment:
                    break
            except Exception as e:
                print(f"Error searching for keyword '{keyword}': {str(e)}")
                continue

        # Randomly select up to max_images_per_segment
        if all_images:
            num_images = random.randint(1, min(self.max_images_per_segment, len(all_images)))
            return random.sample(all_images, num_images)
        return []

    def process_content(self, content: str) -> List[ContentSegment]:
        """Process content into segments with keywords and images"""
        # Split content into segments
        segments = self._split_into_segments(content)
        
        processed_segments = []
        
        for segment in segments:
            # Generate keywords for the segment
            keywords = self._generate_keywords(segment)
            
            # Get images based on keywords
            images = self._get_images_for_keywords(keywords)
            
            # Create segment object
            processed_segment = ContentSegment(
                text=segment,
                keywords=keywords,
                images=images
            )
            
            processed_segments.append(processed_segment)
        
        return processed_segments

    def generate_speech_and_timing(self, processed_segments: List[ContentSegment]) -> List[Dict]:
        """
        Convert segments to speech and calculate timing information.
        Returns list of segments with audio paths and timing information.
        """
        print("Generating speech and calculating timing...")
        
        # Create audio directory if it doesn't exist
        audio_dir = "audio_segments"
        os.makedirs(audio_dir, exist_ok=True)
        
        timed_segments = []
        current_time = 0  # Running time in milliseconds
        
        for i, segment in enumerate(processed_segments):
            try:
                # Generate speech file
                audio_path = os.path.join(audio_dir, f"segment_{i}.mp3")
                tts = gTTS(text=segment.text, lang='en', slow=False)
                tts.save(audio_path)
                
                # Load audio file to get duration
                audio = AudioSegment.from_mp3(audio_path)
                duration = len(audio)  # Duration in milliseconds
                
                # Create timed segment info
                timed_segment = {
                    "text": segment.text,
                    "keywords": segment.keywords,
                    "images": segment.images,
                    "audio_path": audio_path,
                    "start_time": current_time / 1000,  # Convert to seconds
                    "end_time": (current_time + duration) / 1000,  # Convert to seconds
                    "duration": duration / 1000  # Convert to seconds
                }
                
                timed_segments.append(timed_segment)
                current_time += duration
                
            except Exception as e:
                print(f"Error processing segment {i}: {str(e)}")
                # Add segment without audio if there's an error
                timed_segment = {
                    "text": segment.text,
                    "keywords": segment.keywords,
                    "images": segment.images,
                    "audio_path": None,
                    "start_time": current_time / 1000,
                    "end_time": current_time / 1000,
                    "duration": 0
                }
                timed_segments.append(timed_segment)
        
        return timed_segments

    def save_processed_content(self, processed_segments: List[ContentSegment], filename: str):
        """Save processed content to JSON file with timing information"""
        # Generate speech and get timing information
        timed_segments = self.generate_speech_and_timing(processed_segments)
        
        # Save to JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(timed_segments, f, indent=2, ensure_ascii=False)

    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'scraper'):
            self.scraper.close()

    def _download_and_resize_image(self, url: str) -> np.ndarray:
        """Download image from URL and convert to numpy array with proper video dimensions"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if image is in RGBA mode
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Target dimensions
            target_width = 1920
            target_height = 1080
            
            # Calculate aspect ratios
            target_ratio = target_width / target_height
            image_ratio = img.size[0] / img.size[1]
            
            # Initialize dimensions for the resized image
            new_width = target_width
            new_height = target_height
            
            if image_ratio > target_ratio:
                # Image is wider than 16:9
                new_height = int(target_width / image_ratio)
            else:
                # Image is taller than 16:9
                new_width = int(target_height * image_ratio)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create black background
            background = Image.new('RGB', (target_width, target_height), (0, 0, 0))
            
            # Calculate position to center the image
            x = (target_width - new_width) // 2
            y = (target_height - new_height) // 2
            
            # Paste resized image onto black background
            background.paste(img, (x, y))
            
            return np.array(background)
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            # Return a black frame as fallback
            return np.zeros((1080, 1920, 3), dtype=np.uint8)

    def _create_full_audio(self, segments: List[Dict]) -> AudioFileClip:
        """Create a single audio file from all segments"""
        print("Creating full audio narration...")
        
        # Combine all text
        full_text = " ".join(segment['text'] for segment in segments)
        
        # Create audio file
        audio_path = "full_narration.mp3"
        try:
            tts = gTTS(text=full_text, lang='en', slow=False)
            tts.save(audio_path)
            
            # Return audio clip
            return AudioFileClip(audio_path)
        except Exception as e:
            print(f"Error creating audio: {e}")
            return None

    def add_captions_to_video(self, input_video: str, output_video: str, segments: List[Dict]):
        """Add captions to video using Captacity Clipify"""
        print("Adding captions to video...")
        
        try:
            # Initialize Captacity Clipify
            
            # Add captions to video using the simple method
            add_captions(
                video_file=input_video,
                output_file=output_video,
                position="bottom",
                font_size=50
            )
            
            print(f"Captions added successfully: {output_video}")
            
        except Exception as e:
            print(f"Error adding captions: {e}")
            raise

    def create_video(self, json_file: str, output_file: str = "output.mp4"):
        """Create video from processed content with captions"""
        print("Creating video...")
        
        # Create temporary video without captions
        temp_video = "temp_output.mp4"
        
        try:
            # Load processed content
            with open(json_file, 'r') as f:
                segments = json.load(f)
            
            # Create full audio narration
            full_audio = self._create_full_audio(segments)
            if full_audio is None:
                print("Failed to create audio narration")
                return
            
            total_duration = full_audio.duration
            video_clips = []
            current_time = 0
            
            for segment in segments:
                try:
                    # Calculate segment duration based on text length ratio
                    segment_text_length = len(segment['text'])
                    total_text_length = sum(len(seg['text']) for seg in segments)
                    segment_duration = (segment_text_length / total_text_length) * total_duration
                    
                    # Process images for this segment
                    if segment['images']:
                        # Limit to maximum 2 images per segment to avoid quick transitions
                        images_to_use = segment['images'][:2]
                        image_clips = []
                        
                        # Calculate timing for images
                        time_per_image = segment_duration / len(images_to_use)
                        # Ensure each image shows for at least 3 seconds
                        time_per_image = max(time_per_image, 3.0)
                        
                        for i, img_data in enumerate(images_to_use):
                            # Download and create image clip
                            img_array = self._download_and_resize_image(img_data['image_url'])
                            img_clip = ImageClip(img_array)
                            
                            # Set duration for this image
                            img_clip = img_clip.set_duration(time_per_image)
                            
                            # Add longer fade effects for smoother transitions
                            fade_duration = min(1.0, time_per_image / 3)
                            img_clip = img_clip.fadein(fade_duration).fadeout(fade_duration)
                            
                            image_clips.append(img_clip)
                        
                        # Combine all image clips for this segment
                        video_segment = concatenate_videoclips(image_clips)
                        
                        # If video segment is shorter than segment duration, extend last image
                        if video_segment.duration < segment_duration:
                            last_image = image_clips[-1]
                            extended_duration = segment_duration - video_segment.duration
                            last_image = last_image.set_duration(last_image.duration + extended_duration)
                            image_clips[-1] = last_image
                            video_segment = concatenate_videoclips(image_clips)
                    else:
                        # Create black frame if no images
                        black_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
                        video_segment = ImageClip(black_frame).set_duration(segment_duration)
                    
                    video_clips.append(video_segment)
                    current_time += segment_duration
                    
                except Exception as e:
                    print(f"Error processing segment: {e}")
                    continue
            
            try:
                # Combine all segments
                final_video = concatenate_videoclips(video_clips)
                
                # Add full audio to video
                final_video = final_video.set_audio(full_audio)
                
                # Write final video with higher quality settings
                final_video.write_videofile(
                    temp_video,
                    fps=30,
                    codec='libx264',
                    audio_codec='aac',
                    threads=4,
                    preset='medium',
                    bitrate='4000k'
                )
                
                # Clean up
                final_video.close()
                full_audio.close()
                for clip in video_clips:
                    clip.close()
                
                # Remove temporary audio file
                if os.path.exists("full_narration.mp3"):
                    os.remove("full_narration.mp3")
                
                # Add captions to the video
                self.add_captions_to_video(temp_video, output_file, segments)
                
            except Exception as e:
                print(f"Error creating final video: {e}")
                raise
            
            print(f"Video created successfully: {output_file}")
            
        except Exception as e:
            print(f"Error creating video: {e}")
            raise
        finally:
            # Ensure temporary file is removed
            if os.path.exists(temp_video):
                try:
                    os.remove(temp_video)
                except:
                    pass

def main():
    # Example usage
    content = """
In a world drowning in distractions, where convenience is worshiped, and effort is underestimated… one silent force separates the extraordinary from the forgotten.
Not talent. Not luck. But self-discipline.
Every moment, you face a choice. Give in… or rise above.
Discipline isn’t about punishment. It’s about power. Your power. The ability to command your mind when comfort tries to steal your future.
Success isn’t built on motivation—it fades. It’s built on habits. Rituals. A war fought in the shadows of your daily choices.
Who do you choose to be? The one who dreams… or the one who does?
The world won’t give you discipline. You must forge it. Build it like steel in the fire of resistance. Burn away weakness. Temper your will. Become relentless.
Most people live their lives in a loop, repeating yesterday’s mistakes. But you? You break the cycle. Because you know something they don’t...
Discipline is freedom. And those who master it… master life.
    """
    
    try:
        # Initialize processor with your API key
        processor = ContentProcessor(
            provider_name="hyperbolic",
            api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZGVsNTBhbGk1MEBnbWFpbC5jb20iLCJpYXQiOjE3Mzg1MTE1Mzd9.q3lmzpYKd5EZTaN2YOf6wKwwUTqAWafcphte5oClzQk",
            max_images_per_segment=2
        )
        
        # Process the content
        print("Processing content...")
        processed_segments = processor.process_content(content)
        
        # Save results with audio and timing information
        print("Saving results with audio timing...")
        processor.save_processed_content(processed_segments, "processed_content.json")
        
        # Create video with captions
        print("Creating video with captions...")
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