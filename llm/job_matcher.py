# from llm.llm_client import LLMClient


# class JobMatcher:

#     def __init__(self):
#         self.client = LLMClient()

#     def score_job(self, job, resume_text):
#         prompt = f"""
# You are an expert career assistant.

# Given:

# RESUME:
# {resume_text}

# JOB DESCRIPTION:
# {job.description}

# TASK:
# 1. Give a match score from 0 to 100
# 2. Explain briefly why
# 3. Say APPLY or SKIP

# Respond strictly in this format:
# Score: <number>
# Decision: <APPLY or SKIP>
# Reason: <short reason>
# """

#         response = self.client.generate(prompt)

#         return self.parse_response(response)

#     def parse_response(self, text):
#         score = 0
#         decision = "SKIP"
#         reason = ""

#         try:
#             for line in text.split("\n"):
#                 line = line.strip()

#                 if line.lower().startswith("score"):
#                     score = int(''.join(filter(str.isdigit, line)))

#                 elif line.lower().startswith("decision"):
#                     decision = line.split(":")[-1].strip().upper()

#                 elif line.lower().startswith("reason"):
#                     reason = line.split(":", 1)[-1].strip()

#         except:
#             pass

#         return score, decision, reason






from llm.local_llm import LocalLLM


class JobMatcher:

    def __init__(self):
        self.client = LocalLLM()  # 🔥 switch to local

    def score_job(self, job, resume_text):
        prompt = f"""
Resume:
{resume_text}

Job:
{job.description}

Give:
Score (0-100)
Decision (APPLY/SKIP)
Reason (short)
"""

        response = self.client.generate(prompt)

        return self.parse_response(response)