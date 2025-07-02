# Job Automation Project

## Overview

This project automates the process of matching your resume to job descriptions scraped from the web. It reads your resume (PDF), processes one or more job description CSV files, scores each job for relevance, and outputs the results in a structured and organized way. The pipeline is modular, allowing for easy extension or replacement of the scoring algorithm.

**Key Features:**
- Batch processing of multiple job description CSVs.
- Resume body extraction with personal info and regulatory phrase removal.
- TF-IDF-based scoring of job descriptions against your resume.
- Output of filtered and discarded jobs, with debug files for transparency.
- Automatic organization of input, output, and processed files.

---

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your files:**
   - Place your resume PDF in `input/cv/` (e.g., `input/cv/GabrieleBaldi_Resume.pdf`).
   - Place one or more job description CSV files in the `input/` folder (not in any subfolder).

3. **Run the script:**
   ```bash
   python main.py
   ```

4. **Check the results:**
   - Filtered and discarded jobs are saved as CSVs in `output/output/` (e.g., `inputname_filtered.csv`, `inputname_discarded.csv`).
   - Debug files are saved in `output/debug/`.
   - Processed CSVs are moved to `input/processed/`.

---

## Scoring Algorithm (Fast Explanation)

The default scoring algorithm uses **TF-IDF (Term Frequency–Inverse Document Frequency) vectorization** combined with **cosine similarity**:

- Both your resume and each job description are converted into numerical vectors that represent the importance of each word.
- Cosine similarity is then calculated between your resume and each job description, resulting in a score from 0 to 100.
- Jobs with higher scores are more similar to your resume and are considered better matches.

The system is modular and ready for future upgrades to more advanced semantic matching (e.g., using BERT or other language model embeddings). 