from scrapers.linkedin_scraper import LinkedInScraper
from storage.excel_handler import ExcelHandler
from llm.job_matcher import JobMatcher


class JobPipeline:

    def __init__(self):
        self.scraper = LinkedInScraper()
        self.storage = ExcelHandler()
        self.matcher = JobMatcher()

    def run(self):
        print("🚀 Starting Job Pipeline...")

        # =========================
        # 1. SCRAPE JOBS
        # =========================
        jobs = self.scraper.fetch_jobs()
        print(f"📦 Total jobs scraped: {len(jobs)}")

        # =========================
        # 2. SAVE RAW DATA
        # =========================
        raw_path = "job_ai_engine/data/raw/jobs.xlsx"

        self.storage.save_jobs(jobs, raw_path)
        print(f"💾 Saved raw jobs → {raw_path}")

        # =========================
        # 3. LOAD RESUME
        # =========================
        with open("job_ai_engine/data/base_resume.txt") as f:
            resume_text = f.read()

        # =========================
        # 4. MATCH JOBS (LLM)
        # =========================
        print("\n🤖 Starting AI Matching...\n")

        results = []

        for job in jobs:
            print(f"🔍 Matching: {job.title}")

            try:
                score, decision, reason = self.matcher.score_job(job, resume_text)

                print(f"   → Score: {score} | {decision}")

            except Exception as e:
                print("❌ LLM Error:", e)
                score, decision, reason = 0, "SKIP", "LLM failed"

            results.append({
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "score": score,
                "decision": decision,
                "reason": reason,
                "link": job.link
            })

        # =========================
        # 5. SAVE PROCESSED DATA
        # =========================
        processed_path = "job_ai_engine/data/processed/matched_jobs.xlsx"

        self.storage.save_results(results, processed_path)

        print(f"\n✅ Processed jobs saved → {processed_path}")
        print("🎯 Pipeline completed successfully!")