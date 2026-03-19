from playwright.sync_api import sync_playwright
from models.job import Job
import time
import uuid


class LinkedInScraper:

    def __init__(self):
        self.roles = [
            "AI Engineer",
            "Machine Learning Engineer",
            "AI Developer"
        ]

        self.locations = ["India"]

        self.max_jobs_per_page = 20
        self.pagination_steps = [0, 25, 50]  # 🔥 load more jobs

    def fetch_jobs(self):
        all_jobs = []

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]

            # Get LinkedIn tab
            page = None
            for p_ in context.pages:
                if "linkedin.com" in p_.url:
                    page = p_
                    break

            if not page:
                page = context.new_page()

            print("✅ Connected to Chrome")

            for role in self.roles:
                for location in self.locations:

                    for start in self.pagination_steps:

                        print("\n" + "="*60)
                        print(f"🔍 {role} | {location} | start={start}")

                        url = f"https://www.linkedin.com/jobs/search/?keywords={role}&location={location}&start={start}"
                        page.goto(url)

                        time.sleep(6)

                        # 🔥 scroll inside job container
                        self.scroll_jobs_list(page)

                        job_cards = page.query_selector_all(".scaffold-layout__list-item")

                        print(f"📦 Found {len(job_cards)} jobs")

                        for card in job_cards[:self.max_jobs_per_page]:
                            try:
                                job = self.parse_job(card, page)

                                if job:
                                    print(f"✅ {job.title} | {job.company}")
                                    all_jobs.append(job)

                            except Exception as e:
                                print("❌ Error:", e)

        return self.remove_duplicates(all_jobs)

    # 🔥 SMART SCROLL (container-based)
    def scroll_jobs_list(self, page):
        print("🔽 Scrolling job list...")

        # Try direct selector first
        container = page.query_selector(".scaffold-layout__list-container")

        # fallback if needed
        if not container:
            print("⚠️ Fallback: detecting container dynamically...")

            divs = page.query_selector_all("div")

            for d in divs:
                try:
                    is_scrollable = page.evaluate(
                        "(el) => el.scrollHeight > el.clientHeight", d
                    )

                    if is_scrollable:
                        text = d.inner_text()

                        if "engineer" in text.lower():
                            container = d
                            break
                except:
                    pass

        if not container:
            print("❌ No scroll container found")
            return

        print("✅ Using correct scroll container")

        prev_count = 0

        for i in range(20):
            page.evaluate("(el) => el.scrollTop += 1000", container)
            time.sleep(2)

            job_cards = page.query_selector_all(".scaffold-layout__list-item")
            current_count = len(job_cards)

            print(f"Scroll {i+1} → {current_count} jobs")

            if current_count == prev_count:
                print("✅ No more jobs loading")
                break

            prev_count = current_count

    # 🔍 Parse job
    def parse_job(self, card, page):
        try:
            text = card.inner_text().strip()

            lines = [l.strip() for l in text.split("\n") if l.strip()]

            if len(lines) < 3:
                return None

            title = lines[0]
            company = lines[1]
            location = lines[2]

            # click job
            try:
                card.click()
                time.sleep(2)
            except:
                pass

            # extract description
            description = ""
            desc_el = page.query_selector(".jobs-description__content")

            if desc_el:
                description = desc_el.inner_text()

            return Job(
                job_id=str(uuid.uuid4()),
                title=title,
                company=company,
                location=location,
                description=description,
                link=page.url,
            )

        except Exception as e:
            print("❌ parse_job failed:", e)
            return None

    # 🧹 remove duplicates
    def remove_duplicates(self, jobs):
        seen = set()
        unique_jobs = []

        for job in jobs:
            key = (job.title, job.company)

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        print(f"\n✅ Final jobs collected: {len(unique_jobs)}")
        return unique_jobs