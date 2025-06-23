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