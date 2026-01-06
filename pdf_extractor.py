from pypdf import PdfReader
import sys
import os

# Methodology: Uses the assignment PDF as a real-world reference source for benchmarks
DEFAULT_PATH = r"f:\2022BCD0028\final\Research Scientist Internship_ Take-Home Assignment.pdf"

def extract_assignment_text(path=None):
    """
    Reads the Take-Home Assignment PDF to extract grounding text for LLM prompts.
    This ensures the generated tasks align with the 'Anatomy of Work' benchmarks.
    """
    target_path = path or DEFAULT_PATH
    
    if not os.path.exists(target_path):
        return f"Warning: Assignment PDF not found at {target_path}"

    try:
        reader = PdfReader(target_path)
        text_content = []
        
        for page in reader.pages:
            # Extracting text from each page for keyword analysis
            page_text = page.extract_text() or ''
            text_content.append(page_text)

        return '\n\n'.join(text_content)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

if __name__ == "__main__":
    # Allow command line overrides for different document paths
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    content = extract_assignment_text(pdf_path)
    print(content)