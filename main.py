from extractors.pdf_reader import extract_text_from_pdf
from extractors.job_reader import read_job_descriptions

if __name__ == "__main__":
    pdf_path = "GabrieleBaldi_Resume.pdf"  # ← Replace this with your actual file path
    text = extract_text_from_pdf(pdf_path)
    print("=== Extracted CV Text ===\n")
    print(text)
    
    csv_path = "jobs-found.csv"  # Replace with your file path
    job_descriptions = read_job_descriptions(csv_path)

    print("=== Job Descriptions (first 3 shown) ===\n")
    for i, desc in enumerate(job_descriptions[:], start=1):
        print(f"Job {i}:\n{desc}\n{'-' * 40}")