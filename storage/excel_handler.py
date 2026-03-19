import pandas as pd
import os

class ExcelHandler:

    def save_jobs(self, jobs, path):
        data = []

        for job in jobs:
            data.append({
                "job_id": job.job_id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "description": job.description,
                "link": job.link,
            })

        df = pd.DataFrame(data)

        # ✅ Create folder if not exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        df.to_excel(path, index=False)

        print(f"✅ Saved {len(df)} jobs to {path}")

    def save_filtered_jobs(self, jobs, path):
        data = []

        for job in jobs:
            data.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "score": job["score"],
                "decision": job["decision"],
                "link": job["link"],
                "resume_path": job["pdf_path"]
            })

        df = pd.DataFrame(data)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_excel(path, index=False)

        print(f"✅ Saved {len(df)} jobs to {path}")
