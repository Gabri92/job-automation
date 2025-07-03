import os
import shutil
from extractors.pdf_reader import extract_text_from_pdf, extract_resume_body, write_debug_resume_body
from extractors.job_reader import read_job_data, write_debug_job_data
from extractors.scoring import score_jobs_tfidf, score_jobs_embedding, write_debug_scored_jobs, filter_and_sort_jobs, write_debug_filtered_jobs, write_debug_discarded_jobs, write_jobs_to_csv
from extractors.translation_utils import translate_job_descriptions

if __name__ == "__main__":
    
    use_embeddings = True
    
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

    # Define known languages (e.g., English and Spanish)
    known_languages = ['en', 'es']

    # Process all CSVs in the input folder
    for filename in os.listdir("input"):
        if filename.lower().endswith(".csv"):
            input_csv_path = os.path.join("input", filename)
            base_name = os.path.splitext(filename)[0]

            jobs = read_job_data(input_csv_path)
            write_debug_job_data(jobs, f"output/debug/{base_name}_job_data_debug.txt")

            # Translate job descriptions as needed
            jobs = translate_job_descriptions(revised_text, jobs, known_languages)

            # Split jobs: those to score and those with score=0
            jobs_to_score = [job for job in jobs if job.get('score', None) != 0]
            jobs_score_zero = [job for job in jobs if job.get('score', None) == 0]

            # Score only jobs that are eligible
            if use_embeddings:
                scored_jobs = score_jobs_embedding(revised_text, jobs_to_score)
                treshold = 25
            else:
                scored_jobs = score_jobs_tfidf(revised_text, jobs_to_score)
                treshold = 20
                
            # Merge back
            all_jobs = scored_jobs + jobs_score_zero

            write_debug_scored_jobs(all_jobs, f"output/debug/{base_name}_scored_jobs_debug.txt")

            # Filter and sort jobs, then write debug outputs
            filtered_jobs, discarded_jobs = filter_and_sort_jobs(all_jobs, threshold=treshold)
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