import os
import subprocess

def compile_pdf(tex_path):
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

        if result.returncode == 0:
            base = os.path.splitext(tex_path)[0]

            for ext in [".aux", ".log", ".out", ".tex"]:
                file_path = base + ext
                if os.path.exists(file_path):
                    os.remove(file_path)

            return True

        return False

    except Exception as e:
        print("❌ PDF Compilation Error:", e)
        return False