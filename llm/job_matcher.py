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
    def parse_response(self, text):
        score = 0
        decision = "SKIP"
        reason = ""

        try:
            for line in text.split("\n"):
                line = line.strip()

                if line.lower().startswith("score"):
                    score = int(''.join(filter(str.isdigit, line)))

                elif line.lower().startswith("decision"):
                    decision = line.split(":")[-1].strip().upper()

                # elif line.lower().startswith("reason"):
                #     reason = line.split(":", 1)[-1].strip()

        except Exception as e:
            print("Parsing error:", e)

        return score, decision
    def __init__(self):
        self.client = LocalLLM()  # 🔥 switch to local

    def score_job(self, job, resume_text):
        prompt = f"""
You are an expert career assistant. given my resume and a job description, you will score how well the job suits for me and my qualifications. PLEASE tell me to skip if i am underqualified, my skills are limited to what i mention in resume
i only want to apply for jobs that are a good match, so be strict with your scoring and decision. dont recommend to apply if the job is a stretch or requires skills i dont have. dont recommand jobs which deen more then 4 years of experience 
i have notice period of 2 months cant join before 2 months
my Resume:
{resume_text}

Job description:
{job.title} - {job.description}

only Give (strictly in this format, no explaination, no extra text):
Score (0-100)
Decision (APPLY/SKIP)
"""

        response = self.client.generate(prompt)
        print("LLM Response:\n", response)  # Debugging output

        return self.parse_response(response)
    
    