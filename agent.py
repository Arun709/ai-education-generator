import json
from openai import OpenAI


class GeneratorAgent:
    """Agent responsible for generating educational content"""
    
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate(self, input_data):
        """Generate educational content based on grade and topic"""
        grade = input_data.get("grade")
        topic = input_data.get("topic")
        
        prompt = f"""You are an educational content generator. Create grade-appropriate content for:
        
Grade Level: {grade}
Topic: {topic}

Generate:
1. A clear, age-appropriate explanation of the topic (2-3 paragraphs)
2. 3 multiple choice questions with 4 options each

Return ONLY a valid JSON object with this exact structure:
{{
    "explanation": "your explanation here",
    "mcqs": [
        {{
            "question": "question text",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "answer": "A) correct option"
        }}
    ]
}}

Make sure the content is appropriate for grade {grade} students."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            return {
                "explanation": f"Error generating content: {str(e)}",
                "mcqs": []
            }
    
    def refine(self, input_data, feedback):
        """Refine content based on reviewer feedback"""
        grade = input_data.get("grade")
        topic = input_data.get("topic")
        
        feedback_text = "\n".join([f"- {f}" for f in feedback])
        
        prompt = f"""You are an educational content generator. Refine the content based on feedback:

Grade Level: {grade}
Topic: {topic}

Reviewer Feedback:
{feedback_text}

Generate improved content addressing all feedback points:
1. A clear, age-appropriate explanation of the topic (2-3 paragraphs)
2. 3 multiple choice questions with 4 options each

Return ONLY a valid JSON object with this exact structure:
{{
    "explanation": "your improved explanation here",
    "mcqs": [
        {{
            "question": "question text",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "answer": "A) correct option"
        }}
    ]
}}

Make sure the content is appropriate for grade {grade} students and addresses all feedback."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            return {
                "explanation": f"Error refining content: {str(e)}",
                "mcqs": []
            }


class ReviewerAgent:
    """Agent responsible for reviewing educational content quality"""
    
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def review(self, generated_content, input_data):
        """Review generated content for quality and appropriateness"""
        grade = input_data.get("grade")
        topic = input_data.get("topic")
        
        content_text = json.dumps(generated_content, indent=2)
        
        prompt = f"""You are an educational content reviewer. Review this content for grade {grade} students on the topic "{topic}".

Content to Review:
{content_text}

Evaluation Criteria:
1. Is the explanation clear and age-appropriate for grade {grade}?
2. Are the vocabulary and concepts suitable for this grade level?
3. Are the MCQs well-formed with one clear correct answer?
4. Do the questions test understanding of the topic?
5. Are all options plausible but only one correct?

Return ONLY a valid JSON object with this exact structure:
{{
    "status": "pass" or "fail",
    "feedback": ["feedback point 1", "feedback point 2", ...]
}}

If content is excellent, return status "pass" with empty or positive feedback.
If improvements needed, return status "fail" with specific feedback points."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content reviewer. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Ensure feedback is a list
            if "feedback" not in result:
                result["feedback"] = []
            elif isinstance(result["feedback"], str):
                result["feedback"] = [result["feedback"]]
            
            return result
            
        except Exception as e:
            return {
                "status": "fail",
                "feedback": [f"Error during review: {str(e)}"]
            }
