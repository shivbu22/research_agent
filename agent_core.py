import os
import openai
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AgentCore:
    def __init__(self, preferred_provider="openai"):
        self.provider = preferred_provider
        self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def analyze(self, query, context_data):
        prompt = f"""
        You are a Research Analysis Agent. 
        Query: {query}
        
        Below is search data from several sources:
        {context_data}
        
        Task: 
        1. Summarize the key findings.
        2. Identify trends or important insights.
        3. Provide a clear, actionable report.
        Format the output in clean Markdown.
        """
        
        if self.provider == "openai":
            return self._call_openai(prompt)
        else:
            return self._call_gemini(prompt)

    def _call_openai(self, prompt):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {e}"

    def _call_gemini(self, prompt):
        try:
            response = self.gemini_client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                    )
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"

if __name__ == "__main__":
    agent = AgentCore(preferred_provider="gemini")
    # print(agent.analyze("What is the current state of quantum computing?", "Quantum computing is evolving rapidly with companies like Google and IBM leading the way."))
