# AI Educational Content Generator

An intelligent educational content generation system using AI agents to create and review grade-appropriate learning materials.

##streamlit(https://ai-education-generator.streamlit.app/undefined)

## Features

- **Generator Agent**: Creates educational explanations and multiple-choice questions
- **Reviewer Agent**: Evaluates content quality and provides feedback
- **Refinement Loop**: Automatically improves content based on reviewer feedback
- **Grade-Appropriate**: Adjusts content complexity for grades 1-12

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get an API Key

You need an OpenAI API key. Get one from:
- OpenAI: https://platform.openai.com/api-keys

### 3. Run the Application

```bash
streamlit run app.py
```

### 4. Use the Application

1. Enter your grade level (1-12)
2. Enter a topic (e.g., "Types of angles")
3. Paste your OpenAI API key
4. Click "Generate Content"

## File Structure

```
.
├── app.py              # Main Streamlit application
├── agent.py            # Agent classes (Generator & Reviewer)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## How It Works

1. **Generation Phase**: The Generator Agent creates educational content based on the grade level and topic
2. **Review Phase**: The Reviewer Agent evaluates the content for appropriateness and quality
3. **Refinement Phase** (if needed): If content fails review, the Generator Agent refines it based on feedback

## Agent Architecture

### GeneratorAgent
- Creates grade-appropriate explanations
- Generates multiple-choice questions
- Refines content based on feedback

### ReviewerAgent
- Evaluates content appropriateness
- Checks question quality
- Provides specific improvement suggestions

## API Models

By default, the app uses `gpt-4o-mini` for cost efficiency. You can modify the model in `agent.py`:

```python
GeneratorAgent(api_key=api_key, model="gpt-4o")
ReviewerAgent(api_key=api_key, model="gpt-4o")
```

## Troubleshooting

### Import Error
Make sure all files (`app.py`, `agent.py`) are in the same directory.

### API Key Error
Ensure your API key is valid and has sufficient credits.

### JSON Parse Error
The app uses `response_format={"type": "json_object"}` which requires OpenAI models that support structured outputs.

## License

MIT License
