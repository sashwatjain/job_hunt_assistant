from llm.local_llm import LocalLLM
import re

class ResumeGenerator:

    def __init__(self):
        self.client = LocalLLM()

    def generate_sections(self, job, resume_base):

        prompt = f"""
You are an expert resume writer.
Given:
RESUME BASE:
{resume_base}

JOB:
Company: {job.company}
Title: {job.title}
Description: {job.description}

TASK:
1. Write a strong message(4-5 lines max) "Why I am a Good Fit" section (personal, confident, not generic)

IMPORTANT:
- Keep it concise
- Make it feel human and confident
- Avoid buzzwords
- Tailor to THIS job specifically

OUTPUT STRICTLY IN THIS FORMAT:

WHY_I_AM_GOOD_FIT: <text>
"""

        response = self.client.generate(prompt)
        # print("Resume LLM Response:\n", response)

        return self.parse_sections(response)

    def parse_sections(self, text):
        hiring = ""

        for line in text.split("\n"):
            line = line.strip()

            if line.upper().startswith("WHY_I_AM_GOOD_FIT"):
                # Extract content after colon
                parts = line.split(":", 1)
                if len(parts) > 1:
                    hiring += parts[1].strip()

        return hiring.strip()
    
