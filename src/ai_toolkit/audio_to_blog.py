"""
Audio to Blog Post Converter
Converts transcript text files into markdown blog posts.
"""

import os
from pathlib import Path
from datetime import datetime


def load_transcript(file_path: str) -> str:
    """Load transcript from a text file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def create_blog_post(transcript: str, title: str = None) -> str:
    """Convert transcript to markdown blog post."""
    if title is None:
        title = "Untitled Transcript"
    
    date = datetime.now().strftime("%Y-%m-%d")
    
    markdown = f"""# {title}

**Published:** {date}

## Transcript

{transcript}

---

*Generated from audio transcript*
"""
    return markdown


def save_blog_post(markdown: str, filename: str, output_dir: str = "posts") -> str:
    """Save blog post to posts/ folder."""
    # Create posts directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Ensure filename ends with .md
    if not filename.endswith('.md'):
        filename += '.md'
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    return file_path


def convert_transcript_to_blog(transcript_file: str, title: str = None, output_dir: str = "posts") -> str:
    """
    Main function to convert a transcript file to a blog post.
    
    Args:
        transcript_file: Path to the transcript text file
        title: Title for the blog post (optional, defaults to "Untitled Transcript")
        output_dir: Directory to save the blog post (default: "posts")
    
    Returns:
        Path to the saved blog post file
    """
    # Load transcript
    transcript = load_transcript(transcript_file)
    
    # Create markdown blog post
    markdown = create_blog_post(transcript, title)
    
    # Generate output filename from input filename
    input_filename = Path(transcript_file).stem
    output_filename = f"{input_filename}_blog"
    
    # Save blog post
    saved_path = save_blog_post(markdown, output_filename, output_dir)
    
    return saved_path


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python audio_to_blog.py <transcript_file> [title]")
        print("\nExample: python audio_to_blog.py transcript.txt 'My Awesome Post'")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        saved_path = convert_transcript_to_blog(transcript_file, title)
        print(f"✓ Blog post saved to: {saved_path}")
    except FileNotFoundError:
        print(f"✗ Error: Transcript file '{transcript_file}' not found")
        sys.exit(1)
