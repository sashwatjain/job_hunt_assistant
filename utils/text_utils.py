import re

def clean_text(text):
    if text is None or isinstance(text, float):
        return ""

    text = str(text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def safe_filename(text):
    text = re.sub(r'[^a-zA-Z0-9]', '_', text)
    return text[:50]