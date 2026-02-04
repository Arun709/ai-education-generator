import json
from typing import Dict, List
import streamlit as st
from groq import Groq

class GeneratorAgent:
    """Agent responsible for generating educational content"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=self.api_key)
    
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
        
        prompt = f"""You are an educational content creator. The previous content was rejected. Create IMPROVED content for Grade {grade} students.

Topic: {topic}

Previous Feedback:
{feedback_text}

Create NEW content that addresses all feedback points:
1. A clear explanation (2-3 paragraphs) suitable for Grade {grade} students
2. 3 multiple-choice questions to test understanding

IMPORTANT: Return ONLY a valid JSON object with this exact structure:
{{
  "explanation": "Your improved explanation here",
  "mcqs": [
    {{
      "question": "Question text",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "answer": "A"
    }}
  ]
}}

Address ALL the feedback points above.
"""
        
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> Dict:
        """Make API call to Groq LLM"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content generator. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            
            content = chat_completion.choices[0].message.content
            if content is None:
                raise ValueError("No content returned from API")
            return json.loads(content)
        except Exception as e:
            return {
                "explanation": f"Error generating content: {str(e)}",
                "mcqs": []
            }


class ReviewerAgent:
    """Agent responsible for reviewing generated content"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=self.api_key)
    
    def review(self, content: Dict, input_data: Dict) -> Dict:
        """Review the generated content for quality and appropriateness"""
        grade = input_data["grade"]
        topic = input_data["topic"]
        
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""You are an educational content reviewer. Evaluate the following content created for Grade {grade} students on the topic "{topic}".

Content to Review:
{content_str}

Evaluation Criteria:
1. Age appropriateness: Is the language suitable for Grade {grade}?
2. Conceptual correctness: Are the concepts accurate?
3. Clarity: Is the explanation clear and easy to understand?
4. MCQ quality: Are questions clear, relevant, and have correct answers?

IMPORTANT: Return ONLY a valid JSON object with this exact structure:
{{
  "status": "pass or fail",
  "feedback": [
    "Specific issue 1",
    "Specific issue 2"
  ]
}}

Rules:
- Return "pass" if content meets all criteria
- Return "fail" if there are any issues
- Provide specific, actionable feedback in the feedback array
- Be strict but fair
- If status is "pass", feedback array can be empty
"""
        
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> Dict:
        """Make API call to Groq LLM"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content reviewer. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            
            content = chat_completion.choices[0].message.content
            if content is None:
                raise ValueError("No content returned from API")
            return json.loads(content)
        except Exception as e:
            return {
                "status": "fail",
                "feedback": [f"Error during review: {str(e)}"]
            }


# Usage in your Streamlit app
def initialize_agents():
    """Initialize agents with API key from Streamlit secrets"""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        generator = GeneratorAgent(api_key=api_key)
        reviewer = ReviewerAgent(api_key=api_key)
        return generator, reviewer
    except KeyError:
        st.error("❌ GROQ_API_KEY not found in secrets. Please configure it.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error initializing agents: {str(e)}")
        st.stop()
