import streamlit as st
import json
from agents import GeneratorAgent, ReviewerAgent

st.set_page_config(page_title="AI Educational Content Generator", layout="wide")

st.title("🎓 AI Educational Content Generator")
st.markdown("*Generate grade-appropriate educational content using AI agents*")

# Sidebar for input
with st.sidebar:
    st.header("📝 Input Parameters")
    grade = st.number_input("Grade Level", min_value=1, max_value=12, value=4)
    topic = st.text_input("Topic", value="Types of angles")
    api_key = st.text_input("API Key (OpenAI/Groq)", type="password")
    
    st.markdown("---")
    st.markdown("### About")
    st.info("This app uses two AI agents:\n\n1. **Generator**: Creates educational content\n2. **Reviewer**: Evaluates and provides feedback")

# Main content area
if st.button("🚀 Generate Content", type="primary"):
    if not api_key:
        st.error("Please provide an API key")
    else:
        input_data = {"grade": grade, "topic": topic}
        
        # Initialize agents
        generator = GeneratorAgent(api_key=api_key)
        reviewer = ReviewerAgent(api_key=api_key)
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Generate content
        status_text.text("🤖 Generator Agent: Creating educational content...")
        progress_bar.progress(33)
        
        with st.spinner("Generating..."):
            generated_content = generator.generate(input_data)
        
        # Display generator output
        st.subheader("📄 Generator Output")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Explanation:**")
            st.write(generated_content.get("explanation", ""))
            
            st.markdown("**Multiple Choice Questions:**")
            for idx, mcq in enumerate(generated_content.get("mcqs", []), 1):
                with st.expander(f"Question {idx}: {mcq['question']}", expanded=True):
                    for option in mcq['options']:
                        st.write(f"- {option}")
                    st.success(f"✅ Correct Answer: {mcq['answer']}")
        
        with col2:
            st.json(generated_content)
        
        # Step 2: Review content
        status_text.text("🔍 Reviewer Agent: Evaluating content quality...")
        progress_bar.progress(66)
        
        with st.spinner("Reviewing..."):
            review_result = reviewer.review(generated_content, input_data)
        
        # Display reviewer feedback
        st.subheader("🔍 Reviewer Feedback")
        
        if review_result["status"] == "pass":
            st.success("✅ Content PASSED review!")
        else:
            st.warning("⚠️ Content FAILED review - Refinement needed")
        
        if review_result.get("feedback"):
            st.markdown("**Feedback Points:**")
            for feedback in review_result["feedback"]:
                st.write(f"- {feedback}")
        
        # Step 3: Refinement if needed
        if review_result["status"] == "fail":
            status_text.text("🔄 Refining content based on feedback...")
            progress_bar.progress(100)
            
            with st.spinner("Refining..."):
                refined_content = generator.refine(input_data, review_result["feedback"])
            
            st.subheader("✨ Refined Output")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("**Explanation:**")
                st.write(refined_content.get("explanation", ""))
                
                st.markdown("**Multiple Choice Questions:**")
                for idx, mcq in enumerate(refined_content.get("mcqs", []), 1):
                    with st.expander(f"Question {idx}: {mcq['question']}", expanded=True):
                        for option in mcq['options']:
                            st.write(f"- {option}")
                        st.success(f"✅ Correct Answer: {mcq['answer']}")
            
            with col2:
                st.json(refined_content)
        else:
            progress_bar.progress(100)
            st.balloons()
        
        status_text.text("✅ Process Complete!")

