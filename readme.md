pip install pandas openpyxl
pip install playwright
playwright install
install request

ollama --version
ollama run mistral



python -m test_llm 







job_ai_engine/
│
├── main.py                      # Entry point
├── pipeline.py                  # Orchestrates full flow
├── test_llm.py 
│
├── config/
│   ├── settings.py              # API keys, configs
│   └── constants.py             # static values
│
├── data/
│   ├── raw/
│   │   └── jobs.xlsx
│   ├── processed/
│   │   └── filtered_jobs.xlsx
│   ├── applied/
│   │   └── applied_jobs.xlsx
│   └── resumes/
│       └── generated/
│
├── models/                      # Data structures
│   └── job.py
│
├── scrapers/
│   |── linkedin_scraper.py
|   └── save_session.py
│
├── filters/
│   └── job_filter.py
│
├── llm/
│   ├── llm_client.py
│   ├── job_analyzer.py
│   └── resume_generator.py
│
├── apply/
│   ├── apply_manager.py
│   └── form_filler.py
│
├── storage/
│   ├── excel_handler.py
│   └── file_manager.py
│
├── utils/
│   ├── logger.py
│   └── helpers.py
│
└── prompts/
    ├── job_analysis.txt
    └── resume_prompt.txt