import os
import shutil
from extractors.pdf_reader import extract_text_from_pdf, extract_resume_body, write_debug_resume_body
from extractors.job_reader import read_job_data, write_debug_job_data
from extractors.scoring import score_jobs_tfidf, write_debug_scored_jobs, filter_and_sort_jobs, write_debug_filtered_jobs, write_debug_discarded_jobs, write_jobs_to_csv

if __name__ == "__main__":
    # Ensure output and processed folders exist
    os.makedirs("output/output", exist_ok=True)
    os.makedirs("output/debug", exist_ok=True)
    os.makedirs("input/cv", exist_ok=True)
    os.makedirs("input/processed", exist_ok=True)

    '''
    RESUME EXTRACTING AND WORKING
    '''
    pdf_path = "input/cv/GabrieleBaldi_Resume.pdf"  # ← Replace this with your actual file path
    text = extract_text_from_pdf(pdf_path)
    revised_text = extract_resume_body(text)
    write_debug_resume_body(revised_text, "output/debug/resume_post_process.txt")

    # Process all CSVs in the input folder
    for filename in os.listdir("input"):
        if filename.lower().endswith(".csv"):
            input_csv_path = os.path.join("input", filename)
            base_name = os.path.splitext(filename)[0]

            jobs = read_job_data(input_csv_path)
            write_debug_job_data(jobs, f"output/debug/{base_name}_job_data_debug.txt")

            # Score jobs and write debug output
            scored_jobs = score_jobs_tfidf(revised_text, jobs)
            write_debug_scored_jobs(scored_jobs, f"output/debug/{base_name}_scored_jobs_debug.txt")

            # Filter and sort jobs, then write debug outputs
            filtered_jobs, discarded_jobs = filter_and_sort_jobs(scored_jobs, threshold=20.0)
            write_debug_filtered_jobs(filtered_jobs, f"output/debug/{base_name}_filtered_debug.txt")
            write_debug_discarded_jobs(discarded_jobs, f"output/debug/{base_name}_discarded_debug.txt")

            # Write final CSV outputs
            write_jobs_to_csv(filtered_jobs, f"output/output/{base_name}_filtered.csv")
            write_jobs_to_csv(discarded_jobs, f"output/output/{base_name}_discarded.csv")

            # Move processed CSV to 'processed' folder
            shutil.move(input_csv_path, os.path.join("input/processed", filename))

    #print("=== Job Descriptions (first 3 shown) ===\n")
    #for i, desc in enumerate(job_descriptions[:], start=1):
    #    print(f"Job {i}:\n{desc}\n{'-' * 40}")