from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def score_jobs_tfidf(resume_text: str, jobs: List[Dict], desc_key: str = 'job-description') -> List[Dict]:
    """
    Scores each job by computing the cosine similarity between the resume and job description using TF-IDF.
    Adds a 'score' key (0-100) to each job dict and returns the updated list.
    """
    texts = [resume_text] + [job[desc_key] for job in jobs]
    vectorizer = TfidfVectorizer().fit(texts)
    tfidf_matrix = vectorizer.transform(texts)
    resume_vec = tfidf_matrix[0]
    job_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(resume_vec, job_vecs)[0]
    for job, sim in zip(jobs, similarities):
        job['score'] = round(sim * 100, 2)
    return jobs


def score_jobs_embedding(resume_text: str, jobs: List[Dict], desc_key: str = 'job-description') -> List[Dict]:
    """
    Stub for future: Scores each job using advanced embedding-based similarity (e.g., Sentence Transformers, OpenAI, etc).
    Adds a 'score' key (0-100) to each job dict and returns the updated list.
    """
    raise NotImplementedError("Embedding-based scoring not implemented yet.")


def write_debug_scored_jobs(jobs: List[Dict], filename: str = "scored_jobs_debug.txt"):
    """
    Writes the list of scored job dicts to a file for debugging (overwrites each run).
    Each job is separated by a line of dashes and includes the score.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for i, job in enumerate(jobs, 1):
            f.write(f"Job {i}:\n")
            for k, v in job.items():
                f.write(f"  {k}: {v}\n")
            f.write("-" * 40 + "\n")


def filter_and_sort_jobs(jobs: List[Dict], threshold: float = 80.0):
    """
    Splits jobs into filtered (score > threshold) and discarded (score <= threshold),
    sorts both by score descending, and returns (filtered_jobs, discarded_jobs).
    """
    filtered = [job for job in jobs if job.get('score', 0) > threshold]
    discarded = [job for job in jobs if job.get('score', 0) <= threshold]
    filtered_sorted = sorted(filtered, key=lambda x: x['score'], reverse=True)
    discarded_sorted = sorted(discarded, key=lambda x: x['score'], reverse=True)
    return filtered_sorted, discarded_sorted


def write_debug_filtered_jobs(jobs: List[Dict], filename: str = "filtered_jobs_debug.txt"):
    """
    Writes the filtered jobs to a file for debugging (overwrites each run).
    """
    write_debug_scored_jobs(jobs, filename)


def write_debug_discarded_jobs(jobs: List[Dict], filename: str = "discarded_jobs_debug.txt"):
    """
    Writes the discarded jobs to a file for debugging (overwrites each run).
    """
    write_debug_scored_jobs(jobs, filename)


def write_jobs_to_csv(jobs: List[Dict], filename: str):
    """
    Writes a list of job dicts to a CSV file with columns: job-company, job-title, job-description, job-link-href, score.
    """
    columns = ['job-company', 'job-title', 'job-description', 'job-link-href', 'score']
    df = pd.DataFrame(jobs)
    # Only keep the specified columns (if present)
    df = df[[col for col in columns if col in df.columns]]
    df.to_csv(filename, index=False) 