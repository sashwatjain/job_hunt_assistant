# Helper functions
    # =========================
    # UTILS
    # =========================
import subprocess
import re

def clean_text(self, text):
    if not text:
        return ""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def safe_filename(self, text):
    text = re.sub(r'[^a-zA-Z0-9]', '_', text)
    return text[:50]

def escape_latex(self, text):
    replacements = {
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def build_resume(self, template, hiring):
    resume = template.replace("__TOHIRINGMANAGER__", hiring)
    return resume

def compile_pdf(self, tex_path):
    try:
        folder = os.path.dirname(tex_path)
        filename = os.path.basename(tex_path)

        pdflatex_path = r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe"

        result = subprocess.run(
            [pdflatex_path, "-interaction=nonstopmode", filename],
            cwd=folder,
            capture_output=True,
            text=True
        )

        print(result.stdout)  # 🔥 IMPORTANT (see errors)
        print(result.stderr)

        if result.returncode == 0:
            print("✅ PDF compiled successfully")
        else:
            print("❌ LaTeX compilation failed")

    except Exception as e:
        print("❌ PDF Compilation Error:", e)
