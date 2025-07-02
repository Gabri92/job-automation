import pandas as pd

def read_job_descriptions(file_path: str) -> list[str]:
    """
    Reads the 'job-description' column from a CSV file.
    Returns a list of job descriptions.
    """
    df = pd.read_csv(file_path)
    if 'job-description' not in df.columns:
        raise ValueError("'job-description' column not found in CSV.")
    return df['job-description'].dropna().tolist()


def read_job_data(file_path: str) -> list[dict]:
    """
    Reads the CSV and returns a list of dicts with keys: job-company, job-title, job-description, job-link-href.
    Raises an error if any column is missing.
    """
    required_cols = ['job-company', 'job-title', 'job-description', 'job-link-href']
    df = pd.read_csv(file_path)
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"'{col}' column not found in CSV.")
    jobs = df[required_cols].dropna(subset=['job-description']).to_dict(orient='records')
    return jobs


def write_debug_job_data(jobs: list[dict], filename: str = "job_data_debug.txt"):
    """
    Writes the list of job dicts to a file for debugging (overwrites each run).
    Each job is separated by a line of dashes.
    """
    with open(filename, "w", encoding="utf-8") as f:
        for i, job in enumerate(jobs, 1):
            f.write(f"Job {i}:\n")
            for k, v in job.items():
                f.write(f"  {k}: {v}\n")
            f.write("-" * 40 + "\n")