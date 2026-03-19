from scrapers.linkedin_scraper import LinkedInScraper
from storage.excel_handler import ExcelHandler
from llm.job_matcher import JobMatcher
from llm.resume_generator import ResumeGenerator
# from utils.helpers import clean_text, escape_latex, build_resume, safe_filename, compile_pdf
import pandas as pd
import os
import time
import subprocess
import re


class JobPipeline:

    def __init__(self):
        self.scraper = LinkedInScraper()
        self.storage = ExcelHandler()
        self.matcher = JobMatcher()
        self.resume_gen = ResumeGenerator()

        self.raw_path = "job_ai_engine/data/raw/jobs.xlsx"
        self.processed_path = "job_ai_engine/data/processed/filtered_jobs.xlsx"
        self.about_me = "data/about_me.txt"

        self.template_path = "data/template/resume_template.tex"
        self.output_dir = "generated_resumes"
        os.makedirs(self.output_dir, exist_ok=True)
    # Helper functions
    # =========================
    # UTILS
    # =========================
    def clean_text(self, text):
        if text is None:
            return ""
        
        # 🔥 handle NaN (float issue from pandas)
        if isinstance(text, float):
            return ""

        text = str(text)  # ensure string

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

            if result.returncode == 0:
                print("✅ PDF compiled successfully")

                # 🔥 CLEANUP FILES
                base = os.path.splitext(tex_path)[0]
                for ext in [".aux", ".log", ".out", ".tex"]:
                    file_path = base + ext
                    if os.path.exists(file_path):
                        os.remove(file_path)

            # else:
            #     # print("❌ LaTeX compilation failed")
            #     # print(result.stdout)
            #     # print(result.stderr)

        except Exception as e:
            print("❌ PDF Compilation Error:", e)


    # =========================
    # MAIN PIPELINE
    # =========================

    def run(self, scrape=False):
        print("🚀 Starting Job Pipeline...\n")

        # =========================
        # 1. SCRAPE
        # =========================
        if scrape:
            print("🌐 Scraping jobs...")
            jobs = self.scraper.fetch_jobs()
            print(f"📦 Scraped {len(jobs)} jobs")
            self.storage.save_jobs(jobs, self.raw_path)

        # =========================
        # 2. LOAD JOBS
        # =========================
        if not os.path.exists(self.raw_path):
            print("❌ No jobs.xlsx found")
            return

        df = pd.read_excel(self.raw_path)

        if df.empty:
            print("❌ jobs.xlsx is empty")
            return

        print(f"📂 Loaded {len(df)} jobs")

        # =========================
        # 3. LOAD RESUME BASE
        # =========================
        with open(self.about_me) as f:
            about_me = self.clean_text(f.read())

        # =========================
        # 4. MATCH + GENERATE
        # =========================
        results = []

        for _, row in df.iterrows():

            title = self.clean_text(row.get("title", ""))
            print(f"\n🔍 Matching: {title}")

            job = type("Job", (), {})()
            job.title = title
            job.company = self.clean_text(row.get("company", ""))
            job.job_id = self.clean_text(str(row.get("job_id", "")))
            job.location = self.clean_text(row.get("location", ""))
            job.description = self.clean_text(row.get("description", ""))[:1000]
            job.link = row.get("link", "")

            pdf_path = ""

            try:
                score, decision = self.matcher.score_job(job, about_me)
                print(f"   → Score: {score} | {decision}")

            except Exception as e:
                print("❌ LLM Error:", e)
                score, decision = 0, "SKIP"

            # =========================
            # 5. GENERATE RESUME
            # =========================
            if score >= 80 and decision == "APPLY":

                print("✨ Generating Resume...")

                try:
                    hiring = self.resume_gen.generate_sections(job, about_me)
                    hiring = self.escape_latex(hiring)

                    with open(self.template_path) as f:
                        template = f.read()

                    final_resume = self.build_resume(template, hiring)

                    company_clean = self.safe_filename(job.company)
                    role_clean = self.safe_filename(job.title)
                    filename = f"Sashwat_resume_for_{company_clean}_{role_clean}"

                    tex_path = os.path.join(self.output_dir, filename + ".tex")

                    with open(tex_path, "w") as f:
                        f.write(final_resume)

                    self.compile_pdf(tex_path)

                    pdf_path = os.path.join(self.output_dir, filename + ".pdf")

                    print(f"📄 Resume Created: {pdf_path}")

                except Exception as e:
                    print("❌ Resume Generation Failed:", e)

            # =========================
            # SAVE RESULT
            # =========================
            results.append({
                "job_id": job.job_id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "score": score,
                "decision": decision,
                # "reason": reason,
                "link": job.link,
                "resume_path": pdf_path
            })

            time.sleep(1)

            # =========================
            # 6. SAVE EXCEL
            # =========================
            self.storage.save_filtered_jobs(results, self.processed_path)

            print(f"\n✅ Saved → {self.processed_path}")
        print("🎯 DONE ALL SAVED")