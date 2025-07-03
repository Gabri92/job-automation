from langdetect import detect
from deep_translator import GoogleTranslator

def translate_job_descriptions(resume_text, jobs, known_languages, desc_key='job-description'):
    """
    Detects language of resume and each job description. If the job description's language is in known_languages,
    translates it to the resume's language (if needed). If not, sets score to 0 for that job.
    Modifies jobs in place and returns them.
    """
    resume_lang = detect(resume_text)
    for job in jobs:
        desc = job.get(desc_key, '')
        try:
            desc_lang = detect(desc)
        except Exception:
            desc_lang = None
        if desc_lang not in known_languages:
            job['score'] = 0
            job[desc_key] = desc  # keep original for debug
            continue
        if desc_lang != resume_lang:
            try:
                translated = GoogleTranslator(source=desc_lang, target=resume_lang).translate(desc)
                job[desc_key] = translated
            except Exception:
                job['score'] = 0
                job[desc_key] = desc  # fallback to original
    return jobs 