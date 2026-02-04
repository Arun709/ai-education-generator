
# AI Educational Content Generator - Complete Documentation
## Agent-Based, UI-Driven System

---

## Table of Contents
1. Project Overview
2. System Architecture
3. Setup Instructions
4. Component Details
5. Usage Guide
6. API Configuration
7. Troubleshooting
8. Testing Guide
9. Deployment Options
10. Future Enhancements

---

## 1. PROJECT OVERVIEW

### Purpose
Generate grade-appropriate educational content using a two-agent AI system:
- **Generator Agent**: Creates educational content
- **Reviewer Agent**: Evaluates content quality

### Key Features
- Structured JSON input/output
- Automatic content refinement
- Interactive Streamlit UI
- Support for multiple LLM APIs (OpenAI, Groq)
- Visual pipeline display

### Technology Stack
- Python 3.8+
- Streamlit (UI framework)
- OpenAI/Groq API (LLM)
- Requests (HTTP library)

---

## 2. SYSTEM ARCHITECTURE

### Agent Flow Diagram
```
User Input (Grade + Topic)
         ↓
   Generator Agent
         ↓
   Generated Content (JSON)
         ↓
   Reviewer Agent
         ↓
   Review Result (pass/fail + feedback)
         ↓
   [If fail] → Refine Content → Final Output
   [If pass] → Final Output
```

### Data Structure

**Input Format:**
```json
{
  "grade": 4,
  "topic": "Types of angles"
}
```

**Generator Output:**
```json
{
  "explanation": "Content explanation...",
  "mcqs": [
    {
      "question": "Question text",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "answer": "B"
    }
  ]
}
```

**Reviewer Output:**
```json
{
  "status": "pass",
  "feedback": ["Issue 1", "Issue 2"]
}
```

---

## 3. SETUP INSTRUCTIONS

### Step 1: System Requirements
- Python 3.8 or higher
- pip package manager
- Internet connection
- API key (OpenAI or Groq)

### Step 2: Create Project Directory
```bash
mkdir ai-education-generator
cd ai-education-generator
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Create Project Files

Create the following file structure:
```
ai-education-generator/
│
├── app.py                 # Main Streamlit application
├── agents.py             # Agent implementations
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt contents:**
```
streamlit==1.31.0
requests==2.31.0
```

---

## 4. COMPONENT DETAILS

### 4.1 Generator Agent (agents.py)

**Responsibility:** Generate educational content

**Methods:**
- `__init__(api_key, model)`: Initialize agent
- `generate(input_data)`: Create initial content
- `refine(input_data, feedback)`: Improve content based on feedback
- `_call_llm(prompt)`: Make API calls

**Key Features:**
- Grade-appropriate language
- Structured JSON output
- 3 MCQs per topic
- Clear explanations

### 4.2 Reviewer Agent (agents.py)

**Responsibility:** Evaluate content quality

**Methods:**
- `__init__(api_key, model)`: Initialize agent
- `review(content, input_data)`: Evaluate content
- `_call_llm(prompt)`: Make API calls

**Evaluation Criteria:**
- Age appropriateness
- Conceptual correctness
- Clarity
- MCQ quality

### 4.3 Streamlit UI (app.py)

**Components:**
- Sidebar: Input parameters and API key
- Main area: Agent output display
- Progress tracking
- JSON/Formatted view toggle

---

## 5. USAGE GUIDE

### Step 1: Start the Application
```bash
streamlit run app.py
```

### Step 2: Configure Parameters
1. Enter **Grade Level** (1-12)
2. Enter **Topic** (e.g., "Types of angles")
3. Enter **API Key** in the sidebar

### Step 3: Generate Content
Click the "🚀 Generate Content" button

### Step 4: Review Results

**Generator Output:**
- Explanation text
- Multiple choice questions
- JSON structure

**Reviewer Feedback:**
- Pass/Fail status
- Specific feedback points

**Refined Output (if applicable):**
- Improved content
- Addresses feedback

### Step 5: Export (Optional)
Copy JSON output for use in other systems

---

## 6. API CONFIGURATION

### Option 1: OpenAI API

**Get API Key:**
1. Visit https://platform.openai.com/api-keys
2. Create account or sign in
3. Click "Create new secret key"
4. Copy and save the key

**Configuration in agents.py:**
```python
self.base_url = "https://api.openai.com/v1/chat/completions"
self.model = "gpt-4o-mini"  # or "gpt-4o", "gpt-3.5-turbo"
```

**Pricing (as of 2026):**
- GPT-4o-mini: $0.15/1M input tokens
- GPT-4o: $2.50/1M input tokens

### Option 2: Groq API (FREE - Recommended for Testing)

**Get API Key:**
1. Visit https://console.groq.com/keys
2. Create account or sign in
3. Generate API key
4. Copy and save the key

**Configuration in agents.py:**
```python
self.base_url = "https://api.groq.com/openai/v1/chat/completions"
self.model = "llama-3.1-70b-versatile"  # or "mixtral-8x7b-32768"
```

**Advantages:**
- Free tier available
- Fast inference
- High quality outputs

### Switching Between APIs

**In agents.py, modify the __init__ method:**
```python
# For OpenAI
def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
    self.api_key = api_key
    self.model = model
    self.base_url = "https://api.openai.com/v1/chat/completions"

# For Groq
def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
    self.api_key = api_key
    self.model = model
    self.base_url = "https://api.groq.com/openai/v1/chat/completions"
```

---

## 7. TROUBLESHOOTING

### Issue 1: "Module not found" Error
**Problem:** Dependencies not installed
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: API Authentication Error
**Problem:** Invalid or missing API key
**Solution:**
- Verify API key is correct
- Check for extra spaces
- Ensure API key is active

### Issue 3: JSON Parsing Error
**Problem:** LLM returned invalid JSON
**Solution:**
- Try again (LLMs can be inconsistent)
- Use `response_format: {"type": "json_object"}` in API call
- Add error handling in code

### Issue 4: "Connection Error"
**Problem:** Network or API endpoint issue
**Solution:**
- Check internet connection
- Verify API endpoint URL
- Check API service status

### Issue 5: Content Quality Issues
**Problem:** Generated content not appropriate
**Solution:**
- Adjust prompts in agents.py
- Use stronger model (e.g., GPT-4o instead of GPT-4o-mini)
- Add more specific instructions in prompts

### Issue 6: Streamlit Port Already in Use
**Problem:** Port 8501 occupied
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

---

## 8. TESTING GUIDE

### Test Case 1: Basic Functionality
**Input:**
- Grade: 4
- Topic: "Types of angles"

**Expected Output:**
- Explanation with 2-3 paragraphs
- 3 MCQs with 4 options each
- Age-appropriate language
- Pass/Fail review status

### Test Case 2: Different Grade Levels
**Test inputs:**
- Grade 1 + "Colors"
- Grade 8 + "Photosynthesis"
- Grade 12 + "Calculus derivatives"

**Verify:** Language complexity matches grade

### Test Case 3: Refinement Loop
**Steps:**
1. Generate content
2. If it passes, try different topic
3. If it fails, verify refinement occurs
4. Check refined content addresses feedback

### Test Case 4: Edge Cases
- Very simple topics (e.g., "Addition")
- Complex topics (e.g., "Quantum mechanics")
- Grade 1 vs Grade 12 same topic

### Manual Testing Checklist
- [ ] App starts without errors
- [ ] Input validation works
- [ ] Generator produces valid JSON
- [ ] Reviewer evaluates correctly
- [ ] Refinement loop works
- [ ] UI displays all outputs
- [ ] Progress bar updates
- [ ] JSON view works
- [ ] Multiple topics work
- [ ] Different grades work

---

## 9. DEPLOYMENT OPTIONS

### Option 1: Local Development
```bash
streamlit run app.py
```
**Use case:** Testing, development

### Option 2: Streamlit Cloud (FREE)

**Steps:**
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Connect GitHub repository
4. Deploy app

**Important:** Store API keys in Streamlit Secrets:
```toml
# .streamlit/secrets.toml
api_key = "your-api-key-here"
```

**Access in code:**
```python
api_key = st.secrets["api_key"]
```

### Option 3: Docker Container

**Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Build and run:**
```bash
docker build -t ai-education-generator .
docker run -p 8501:8501 ai-education-generator
```

### Option 4: Cloud Platforms
- **Heroku**: Use buildpack for Streamlit
- **AWS EC2**: Deploy on virtual machine
- **Google Cloud Run**: Containerized deployment
- **Azure Web Apps**: Python web app

---

## 10. FUTURE ENHANCEMENTS

### Phase 1: Enhanced Features
- [ ] Support for images/diagrams
- [ ] PDF export functionality
- [ ] Multiple languages support
- [ ] Save/load content history
- [ ] Batch generation

### Phase 2: Advanced Agents
- [ ] Add "Fact-Checker" agent
- [ ] Add "Accessibility" agent (for special needs)
- [ ] Add "Difficulty Adjuster" agent
- [ ] Multi-agent collaboration

### Phase 3: User Features
- [ ] User authentication
- [ ] Content library
- [ ] Analytics dashboard
- [ ] Teacher/Student roles
- [ ] Classroom integration

### Phase 4: Content Types
- [ ] Essay questions
- [ ] Fill-in-the-blanks
- [ ] True/False questions
- [ ] Matching exercises
- [ ] Interactive quizzes

### Phase 5: Technical Improvements
- [ ] Caching for faster responses
- [ ] Async API calls
- [ ] Rate limiting
- [ ] Error recovery
- [ ] Unit tests

---

## APPENDIX A: Complete Code Reference

### File: app.py
Location: Root directory
Purpose: Main Streamlit application
Lines: ~120

### File: agents.py
Location: Root directory
Purpose: Agent implementations
Classes:
- GeneratorAgent
- ReviewerAgent
Lines: ~150

### File: requirements.txt
Location: Root directory
Purpose: Python dependencies
Packages: 2

---

## APPENDIX B: API Response Examples

### Successful Generator Response
```json
{
  "explanation": "Angles are formed when two lines meet at a point. There are different types of angles based on their measurement. An acute angle is less than 90 degrees, like the corner of a slice of pizza. A right angle is exactly 90 degrees, like the corner of a book. An obtuse angle is more than 90 degrees but less than 180 degrees, like when you open a door wide.",
  "mcqs": [
    {
      "question": "What type of angle is exactly 90 degrees?",
      "options": ["A) Acute angle", "B) Right angle", "C) Obtuse angle", "D) Straight angle"],
      "answer": "B"
    }
  ]
}
```

### Failed Review Example
```json
{
  "status": "fail",
  "feedback": [
    "Explanation uses term 'measurement' which may be too advanced for Grade 4",
    "Question 3 introduces 'straight angle' concept not explained in the main content"
  ]
}
```

---

## APPENDIX C: Prompt Engineering Tips

### For Better Generator Output
1. Specify exact output structure
2. Emphasize age-appropriateness
3. Provide examples when needed
4. Use clear formatting instructions
5. Set appropriate temperature (0.7 for creativity)

### For Better Reviewer Output
1. Define clear evaluation criteria
2. Ask for specific feedback
3. Use lower temperature (0.3 for consistency)
4. Provide examples of good/bad content
5. Request actionable suggestions

---

## APPENDIX D: Common LLM Models

### OpenAI Models
- **gpt-4o**: Most capable, expensive
- **gpt-4o-mini**: Good balance, recommended
- **gpt-3.5-turbo**: Faster, cheaper, less capable

### Groq Models (Free Tier)
- **llama-3.1-70b-versatile**: Best quality
- **llama-3.1-8b-instant**: Fastest
- **mixtral-8x7b-32768**: Large context window

---

## SUPPORT & RESOURCES

### Documentation Links
- Streamlit Docs: https://docs.streamlit.io
- OpenAI API: https://platform.openai.com/docs
- Groq API: https://console.groq.com/docs

### Community Support
- Streamlit Forum: https://discuss.streamlit.io
- Stack Overflow: Tag [streamlit]

### Contact
For project-specific issues, refer to GitHub repository issues section.

---

## LICENSE
[MIT License]


---

**Document Version:** 1.0
**Last Updated:** February 4, 2026
**Author:** [Arunachalam Kannan]
