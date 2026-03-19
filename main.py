from pipeline.job_pipeline import JobPipeline

if __name__ == "__main__":
    pipeline = JobPipeline()
    pipeline.run()
    # pipeline.run(scrape=True)