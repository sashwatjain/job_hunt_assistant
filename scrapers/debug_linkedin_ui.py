from playwright.sync_api import sync_playwright
import time


def analyze_real_search_ui():

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]

        # get correct tab
        page = None
        for p_ in context.pages:
            if "linkedin.com" in p_.url:
                page = p_
                break

        if not page:
            page = context.new_page()

        print("✅ Connected to Chrome")

        # 🔥 FORCE SEARCH PAGE (IMPORTANT)
        url = "https://www.linkedin.com/jobs/search/?keywords=AI%20Engineer&location=India"
        print("🌐 Opening:", url)

        page.goto(url)
        time.sleep(10)  # VERY IMPORTANT

        print("\n📍 Current URL:", page.url)

        # 🔥 SCROLL (to trigger lazy load)
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        print("\n" + "="*80)
        print("🔍 ANALYZING STRUCTURE...\n")

        # 🔹 Find ALL ULs (job list containers)
        uls = page.query_selector_all("ul")
        print(f"Total ULs: {len(uls)}")

        for i, ul in enumerate(uls[:10]):
            try:
                items = ul.query_selector_all("li")
                text = ul.inner_text()[:200]

                print(f"\n--- UL {i+1} ---")
                print(f"Items: {len(items)}")
                print(f"Text: {text}")

            except:
                pass

        # 🔹 Detect job cards (IMPORTANT)
        print("\n" + "="*80)
        print("🔍 DETECTING JOB CARDS\n")

        selectors = [
            "li.jobs-search-results__list-item",
            ".job-card-container",
            ".scaffold-layout__list-item",
            "li"
        ]

        for sel in selectors:
            elements = page.query_selector_all(sel)
            print(f"{sel} → {len(elements)} elements")

        # 🔹 Print real job samples
        print("\n" + "="*80)
        print("🧪 JOB SAMPLES\n")

        cards = page.query_selector_all("li")

        count = 0
        for card in cards:
            try:
                text = card.inner_text()

                if "engineer" in text.lower():
                    print(text[:300])
                    print("-"*40)
                    count += 1

                    if count >= 5:
                        break

            except:
                pass


if __name__ == "__main__":
    analyze_real_search_ui()