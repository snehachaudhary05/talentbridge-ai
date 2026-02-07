"""
Utility to extract text from resume files (PDF, DOC, DOCX)
"""
import os
from typing import Optional


def extract_text_from_file(file) -> str:
    """
    Extract text from uploaded resume file

    Args:
        file: UploadedFile object from Django

    Returns:
        Extracted text content
    """
    filename = file.name.lower()

    try:
        if filename.endswith('.txt'):
            return file.read().decode('utf-8', errors='ignore')

        elif filename.endswith('.pdf'):
            return extract_text_from_pdf(file)

        elif filename.endswith(('.doc', '.docx')):
            return extract_text_from_docx(file)

        else:
            raise ValueError(f"Unsupported file format: {filename}")

    except Exception as e:
        raise ValueError(f"Failed to extract text from file: {str(e)}")


def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        import PyPDF2
        import re

        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # Clean up the extracted text
        text = clean_extracted_text(text)

        print(f"[DEBUG] PDF extraction: {len(text)} chars from {len(pdf_reader.pages)} pages")
        return text.strip()
    except ImportError:
        # If PyPDF2 not installed, try simple text extraction
        return file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {str(e)}")


def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        import docx
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        # Clean up the extracted text
        text = clean_extracted_text(text)

        return text.strip()
    except ImportError:
        # If python-docx not installed, try simple text extraction
        return file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        raise ValueError(f"Failed to extract DOCX text: {str(e)}")


def clean_extracted_text(text: str) -> str:
    """
    Clean up extracted text from PDFs/DOCX files
    Removes excessive whitespace, special characters, and formatting artifacts
    """
    import re

    # Remove null bytes and other control characters
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    # Remove excessive whitespace (more than 2 spaces)
    text = re.sub(r' {3,}', '  ', text)

    # Remove excessive newlines (more than 2)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove repeated identical lines (common in PDF extraction errors)
    lines = text.split('\n')
    cleaned_lines = []
    prev_line = None
    repeat_count = 0

    for line in lines:
        line = line.strip()
        if line == prev_line:
            repeat_count += 1
            # Skip if same line repeated more than 2 times
            if repeat_count > 2:
                continue
        else:
            repeat_count = 0

        cleaned_lines.append(line)
        prev_line = line

    text = '\n'.join(cleaned_lines)

    # Final cleanup
    text = text.strip()

    print(f"[DEBUG] Text cleaning: {len(text)} chars after cleanup")

    return text
