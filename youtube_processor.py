from yt_dlp import YoutubeDL
import whisper
import os
from ai_content_processor import ContentProcessor
import argparse
from openai import OpenAI

class ContentEnhancementAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def enhance_content(self, transcript: str) -> str:
        """Enhance and improve the transcript content using AI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a content enhancement expert. 
                     Your task is to improve the given transcript by:
                     1. Fixing grammar and clarity issues
                     2. Adding more descriptive language
                     3. Organizing content into clear sections
                     4. Expanding on key points
                     5. Making the content more engaging
                     Please maintain the original message while making these improvements."""},
                    {"role": "user", "content": f"Please enhance this transcript:\n{transcript}"}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error enhancing content: {e}")
            raise

class YouTubeProcessor:
    def __init__(self, openai_api_key: str = None):
        # Initialize whisper model for speech recognition
        self.whisper_model = whisper.load_model("base")
        self.temp_dir = "temp_downloads"
        self.content_enhancer = ContentEnhancementAgent(openai_api_key) if openai_api_key else None
        os.makedirs(self.temp_dir, exist_ok=True)

    def download_audio(self, url: str) -> str:
        """Download audio from YouTube video"""
        output_path = os.path.join(self.temp_dir, "audio")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return f"{output_path}.mp3"
        except Exception as e:
            print(f"Error downloading video: {e}")
            raise

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text using Whisper"""
        try:
            result = self.whisper_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            raise

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def process_youtube_video(self, url: str, api_key: str, output_file: str = "output_video.mp4", openai_api_key: str = None):
        """Process YouTube video and create new AI-generated video"""
        try:
            # Download audio
            print("Downloading audio from YouTube...")
            audio_path = self.download_audio(url)

            # Transcribe audio
            print("Transcribing audio...")
            transcript = self.transcribe_audio(audio_path)

            # Enhance content if OpenAI API key is provided
            if self.content_enhancer:
                print("Enhancing content...")
                transcript = self.content_enhancer.enhance_content(transcript)

            # Initialize content processor
            print("Initializing content processor...")
            processor = ContentProcessor(
                provider_name="hyperbolic",
                api_key=api_key,
                max_images_per_segment=2
            )

            # Process content
            print("Processing content...")
            processed_segments = processor.process_content(transcript)

            # Save processed content
            print("Saving processed content...")
            processor.save_processed_content(processed_segments, "processed_youtube_content.json")

            # Create video
            print("Creating video...")
            processor.create_video("processed_youtube_content.json", output_file)

            print(f"Video processing complete! Output saved to: {output_file}")

        except Exception as e:
            print(f"Error processing video: {e}")
            raise
        finally:
            self.cleanup()

def main():
    # Option 1: Remove argument parsing since using hardcoded values
    processor = YouTubeProcessor()
    processor.process_youtube_video(
        "https://youtu.be/nZg3hzOReWY?si=5DUYQOTVVHx1RNMO",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZGVsNTBhbGk1MEBnbWFpbC5jb20iLCJpYXQiOjE3Mzg1MTE1Mzd9.q3lmzpYKd5EZTaN2YOf6wKwwUTqAWafcphte5oClzQk",
        "output_video.mp4"
    )

if __name__ == "__main__":
    main() 