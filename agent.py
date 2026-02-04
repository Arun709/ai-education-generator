import json
from typing import Dict, List
import requests

class GeneratorAgent:
    """Agent responsible for generating educational content"""

    def __init__(self, api_key: str, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider.lower()

        # Set base URL and model based on provider
        if self.provider == "groq":
            self.base_url = "https://api.groq.com/openai/v1/chat/completions"
            self.model = "llama-3.1-70b-versatile"
        else:  # openai
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.model = "gpt-4o-mini"

    def generate(self, input_data: Dict) -> Dict:
        """Generate educational content for given grade and topic"""
        grade = input_data["grade"]
        topic = input_data["topic"]

        prompt = f"""You are an educational content creator. Generate age-appropriate content for Grade {grade} students.

Topic: {topic}

Create:
1. A clear explanation (2-3 paragraphs) suitable for Grade {grade} students
2. 3 multiple-choice questions to test understanding

IMPORTANT: Return ONLY a valid JSON object with this exact structure:
{{
  "explanation": "Your explanation here",
  "mcqs": [
    {{
      "question": "Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "answer": "A"
    }}
  ]
}}

Guidelines:
- Use simple language appropriate for Grade {grade}
- Ensure concepts are accurate
- Make questions clear and unambiguous
- Each MCQ should have exactly 4 options labeled A, B, C, D
"""

        return self._call_llm(prompt)

    def refine(self, input_data: Dict, feedback: List[str]) -> Dict:
        """Refine content based on reviewer feedback"""
        grade = input_data["grade"]
        topic = input_data["topic"]

        feedback_text = "\n".join([f"- {fb}" for fb in feedback])

        prompt = f"""You are an educational content creator. The previous content was rejected. Create IMPROVE
