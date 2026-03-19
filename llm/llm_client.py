import requests
from config.settings import GROQ_API_KEY


class LLMClient:

    def generate(self, prompt):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                },
                timeout=30
            )

            # Debug status
            if response.status_code != 200:
                print("❌ LLM API Error:", response.text)
                return "Score: 0\nDecision: SKIP\nReason: API error"

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print("❌ LLM Exception:", e)
            return "Score: 0\nDecision: SKIP\nReason: Exception occurred"