from scrapers.linkedin_scraper import LinkedInScraper
from storage.excel_handler import ExcelHandler
from llm.job_matcher import JobMatcher
from llm.resume_generator import ResumeGenerator

from utils.text_utils import clean_text
from services.resume_service import ResumeService

import pandas as pd
import os
import time


class JobPipeline:

    def __init__(self):
        self.scraper = LinkedInScraper()
        self.storage = ExcelHandler()
        self.matcher = JobMatcher()
        self.resume_gen = ResumeGenerator()

        self.raw_path = "job_ai_engine/data/raw/jobs_1.xlsx"
        self.processed_path = "job_ai_engine/data/processed/filtered_jobs_1.xlsx"
        self.about_me_path = "config/about_me.txt"

        self.template_path = "config/template/resume_template.tex"
        self.output_dir = "generated_resumes"

        self.resume_service = ResumeService(
            self.template_path,
            self.output_dir
        )

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
        # 3. LOAD ABOUT ME
        # =========================
        if not os.path.exists(self.about_me_path):
            print("❌ about_me.txt not found")
            return

        with open(self.about_me_path) as f:
            about_me = clean_text(f.read())

        # =========================
        # 4. PROCESS JOBS
        # =========================
        results = []

        for _, row in df.iterrows():

            title = clean_text(row.get("title", ""))
            print(f"\n🔍 Matching: {title}")

            job = type("Job", (), {})()
            job.title = title
            job.company = clean_text(row.get("company", ""))
            job.job_id = clean_text(str(row.get("job_id", "")))
            job.location = clean_text(row.get("location", ""))
            job.description = clean_text(row.get("description", ""))[:1000]
            job.link = row.get("link", "")

            pdf_path = ""
            hiring_message = ""

            # =========================
            # MATCH JOB
            # =========================
            try:
                score, decision = self.matcher.score_job(job, about_me)
                print(f"   → Score: {score} | {decision}")

            except Exception as e:
                print("❌ LLM Error:", e)
                score, decision = 0, "SKIP"

            # =========================
            # GENERATE RESUME
            # =========================
            if score >= 80 and decision == "APPLY":

                print("✨ Generating Resume...")

                try:
                    hiring = self.resume_gen.generate_sections(job, about_me)

                    hiring_message = clean_text(hiring)
                    print(f"💡 Hiring Message:\n{hiring_message}\n")

                    pdf_path = self.resume_service.generate_resume(
                        job,
                        hiring_message
                    )

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
                "link": job.link,
                "resume_path": pdf_path or "",
                "hiring_message": hiring_message or ""
            })

            # Avoid rate limits
            time.sleep(1)

            # Save progressively (safe)
            self.storage.save_filtered_jobs(results, self.processed_path)

            print(f"✅ Saved → {self.processed_path}")

        print("\n🎯 DONE ALL JOBS PROCESSED")