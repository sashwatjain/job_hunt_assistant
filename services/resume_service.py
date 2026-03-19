import os
from utils.text_utils import safe_filename
from utils.latex_utils import escape_latex, build_resume
from utils.file_utils import compile_pdf


class ResumeService:

    def __init__(self, template_path, output_dir):
        self.template_path = template_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_resume(self, job, hiring_text):
        try:
            hiring_latex = escape_latex(hiring_text)

            with open(self.template_path) as f:
                template = f.read()

            final_resume = build_resume(template, hiring_latex)

            filename = f"Sashwat_resume_for_{safe_filename(job.company)}_{safe_filename(job.title)}"
            tex_path = os.path.join(self.output_dir, filename + ".tex")

            with open(tex_path, "w") as f:
                f.write(final_resume)

            success = compile_pdf(tex_path)

            if success:
                return os.path.join(self.output_dir, filename + ".pdf")

            return ""

        except Exception as e:
            print("❌ Resume Service Error:", e)
            return ""