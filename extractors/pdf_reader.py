import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from a PDF file using PyMuPDF (fitz).
    """
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text.strip()

def extract_resume_body(text: str) -> str:
    """
    Extracts the main body of a resume, removing headers/titles and personal info using heuristics:
    - Removes lines matching personal info patterns (email, github, linkedin, location, phone, etc.)
    - Always keeps SKILLS/STRENGTHS sections and their content (even if short or all caps)
    - Removes other section headers and very short lines elsewhere
    - Removes up to the last 3 lines if they match regulatory/authorization patterns (e.g., GDPR, authorize, personal data, regulation)
    Returns the cleaned body text.
    """
    section_headers = [
        r"^EDUCATION$", r"^EXPERIENCE$", r"^PROJECTS$", r"^CONTACT$", r"^SUMMARY$", r"^PROFILE$",
        r"^CERTIFICATIONS$", r"^LANGUAGES$", r"^INTERESTS$", r"^AWARDS$", r"^PUBLICATIONS$"
    ]
    keep_sections = [r"^SKILLS$", r"^STRENGTHS$"]
    personal_info_patterns = [
        r"@",  # email
        r"github", r"linkedin", r"location", r"email", r"phone"  # links and location
    ]
    lines = text.splitlines()
    body_lines = []
    in_keep_section = False
    for line in lines:
        line_stripped = line.strip()
        # Remove personal info lines
        if any(re.search(pattern, line_stripped, re.IGNORECASE) for pattern in personal_info_patterns):
            continue
        # Section header logic
        if any(re.match(pattern, line_stripped, re.IGNORECASE) for pattern in keep_sections):
            in_keep_section = True
            body_lines.append(line_stripped)
            continue
        if any(re.match(pattern, line_stripped, re.IGNORECASE) for pattern in section_headers):
            in_keep_section = False
            continue
        # If in SKILLS/STRENGTHS section, keep all lines
        if in_keep_section:
            body_lines.append(line_stripped)
            continue
        # Skip empty lines
        if not line_stripped:
            continue
        # Skip all-caps lines (likely headers)
        if line_stripped.isupper() and len(line_stripped) < 30:
            continue
        # Skip very short lines
        if len(line_stripped.split()) < 3:
            continue
        body_lines.append(line_stripped)
    # Remove up to the last 3 lines if they match regulatory/authorization patterns
    regulatory_patterns = [
        r"gdpr", r"authorize", r"personal data", r"regulation"
    ]
    # Check last 3 lines
    for i in range(1, min(4, len(body_lines)+1)):
        line = body_lines[-i]
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in regulatory_patterns):
            body_lines[-i] = None
    # Remove marked lines
    body_lines = [line for line in body_lines if line is not None]
    return "\n".join(body_lines)

def write_debug_resume_body(body_text: str, filename: str = "resume_body_debug.txt"):
    """
    Writes the cleaned resume body to a file for debugging (overwrites each run).
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(body_text)