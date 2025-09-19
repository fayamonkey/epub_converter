import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
import os
from markdownify import markdownify


class EpubConverter:
    def __init__(self, epub_path):
        self.epub_path = epub_path
        self.book = epub.read_epub(epub_path)
        self.title = self.book.get_metadata('DC', 'title')[0][0] if self.book.get_metadata('DC', 'title') else 'Unknown Title'
        self.author = self.book.get_metadata('DC', 'creator')[0][0] if self.book.get_metadata('DC', 'creator') else 'Unknown Author'

    def extract_text(self):
        """Extract plain text from EPUB"""
        text_content = []

        # Add title and author info
        text_content.append(f"Title: {self.title}")
        text_content.append(f"Author: {self.author}")
        text_content.append("=" * 50)
        text_content.append("")

        # Extract content from each item
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text and clean it up
                text = soup.get_text()

                # Clean up whitespace
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)

                if text.strip():
                    text_content.append(text)
                    text_content.append("")  # Add spacing between chapters

        return '\n'.join(text_content)

    def extract_markdown(self):
        """Extract content as markdown"""
        markdown_content = []

        # Add title and author info
        markdown_content.append(f"# {self.title}")
        markdown_content.append(f"**Author:** {self.author}")
        markdown_content.append("")
        markdown_content.append("---")
        markdown_content.append("")

        chapter_count = 0

        # Extract content from each item
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Convert HTML to markdown
                html_content = str(soup)
                if html_content.strip():
                    chapter_count += 1

                    # Add chapter header if there's substantial content
                    text_preview = soup.get_text().strip()
                    if len(text_preview) > 100:  # Only add chapter header for substantial content
                        markdown_content.append(f"## Chapter {chapter_count}")
                        markdown_content.append("")

                    # Convert to markdown
                    markdown = markdownify(html_content, heading_style="ATX")

                    # Clean up the markdown
                    markdown = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown)  # Remove excessive line breaks
                    markdown = markdown.strip()

                    if markdown:
                        markdown_content.append(markdown)
                        markdown_content.append("")

        return '\n'.join(markdown_content)

    def convert_to_text(self, output_path):
        """Convert EPUB to plain text file"""
        text_content = self.extract_text()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        return output_path

    def convert_to_markdown(self, output_path):
        """Convert EPUB to markdown file"""
        markdown_content = self.extract_markdown()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return output_path


def convert_epub(epub_path, output_format='txt', output_dir=None):
    """
    Convert EPUB file to specified format

    Args:
        epub_path (str): Path to the EPUB file
        output_format (str): 'txt' or 'md'
        output_dir (str): Directory to save output file (optional)

    Returns:
        str: Path to the converted file
    """
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"EPUB file not found: {epub_path}")

    converter = EpubConverter(epub_path)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(epub_path))[0]
    safe_title = re.sub(r'[^\w\s-]', '', converter.title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)

    if output_dir is None:
        output_dir = os.path.dirname(epub_path)

    if output_format.lower() == 'md':
        output_path = os.path.join(output_dir, f"{safe_title}.md")
        return converter.convert_to_markdown(output_path)
    else:
        output_path = os.path.join(output_dir, f"{safe_title}.txt")
        return converter.convert_to_text(output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python epub_converter.py <epub_file> [output_format]")
        print("Output format: 'txt' (default) or 'md'")
        sys.exit(1)

    epub_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'txt'

    try:
        output_file = convert_epub(epub_file, output_format)
        print(f"Conversion successful! Output saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)