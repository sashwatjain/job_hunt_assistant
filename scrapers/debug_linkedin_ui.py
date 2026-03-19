from playwright.sync_api import sync_playwright
import time


def debug_job_card(card, index):
    print("\n" + "=" * 100)
    print(f"🔎 DEBUGGING JOB CARD #{index}")
    print("=" * 100)

    try:
        # -----------------------------
        # 1. FULL TEXT
        # -----------------------------
        print("\n📄 FULL INNER TEXT:\n")
        print(card.inner_text())

        # -----------------------------
        # 2. HTML STRUCTURE
        # -----------------------------
        print("\n🌐 INNER HTML (first 2000 chars):\n")
        html = card.inner_html()
        print(html[:2000])

        # -----------------------------
        # 3. TRY COMMON SELECTORS
        # -----------------------------
        print("\n🎯 TESTING SELECTORS:\n")

        selectors = {
            "TITLE (a span)": "a span[aria-hidden='true']",
            "TITLE ALT": ".job-card-list__title",
            "COMPANY 1": ".job-card-container__company-name",
            "COMPANY 2": ".artdeco-entity-lockup__subtitle span",
            "COMPANY 3": ".artdeco-entity-lockup__subtitle",
            "COMPANY 4": "span.t-14.t-normal",
            "LOCATION": ".job-card-container__metadata-item",
        }

        for name, selector in selectors.items():
            try:
                el = card.query_selector(selector)
                if el:
                    print(f"✅ {name}: {el.inner_text().strip()}")
                else:
                    print(f"❌ {name}: NOT FOUND")
            except Exception as e:
                print(f"⚠️ {name}: ERROR -> {e}")

        # -----------------------------
        # 4. PRINT ALL SPANS (IMPORTANT)
        # -----------------------------
        print("\n🧠 ALL SPANS (first 20):\n")

        spans = card.query_selector_all("span")
        for i, s in enumerate(spans[:20]):
            try:
                txt = s.inner_text().strip()
                if txt:
                    print(f"{i}: {txt}")
            except:
                pass

        # -----------------------------
        # 5. PRINT ALL LINKS (sometimes company inside <a>)
        # -----------------------------
        print("\n🔗 ALL LINKS:\n")

        links = card.query_selector_all("a")
        for i, a in enumerate(links[:10]):
            try:
                txt = a.inner_text().strip()
                href = a.get_attribute("href")
                print(f"{i}: TEXT={txt} | LINK={href}")
            except:
                pass

    except Exception as e:
        print("❌ DEBUG FAILED:", e)


def run_debug():
    with sync_playwright() as p:
        print("🚀 Connecting to Chrome...")

        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]

        # Find LinkedIn page
        page = None
        for p_ in context.pages:
            if "linkedin.com/jobs" in p_.url:
                page = p_
                break

        if not page:
            print("❌ No LinkedIn jobs tab found.")
            return

        print("✅ Connected to LinkedIn tab")

        # Wait for jobs to load
        time.sleep(5)

        # Scroll a bit (important)
        print("🔽 Scrolling...")
        for _ in range(5):
            page.mouse.wheel(0, 2000)
            time.sleep(2)

        # Get job cards
        job_cards = page.query_selector_all(".scaffold-layout__list-item")

        print(f"\n📦 Found {len(job_cards)} job cards")

        if not job_cards:
            print("❌ No jobs found. Try changing page or scrolling more.")
            return

        # Debug first 3 cards only
        for i, card in enumerate(job_cards[:3]):
            debug_job_card(card, i)

        print("\n✅ DEBUG COMPLETE")


if __name__ == "__main__":
    run_debug()