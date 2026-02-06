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
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
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
        return text.strip()
    except ImportError:
        # If python-docx not installed, try simple text extraction
        return file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        raise ValueError(f"Failed to extract DOCX text: {str(e)}")
