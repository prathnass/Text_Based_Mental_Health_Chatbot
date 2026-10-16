import streamlit as st
import ollama
import base64
from streamlit.components.v1 import html

# Set page configuration
st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to set background image
def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image.
    """
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64_encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Main content container with glass effect */
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.88);
                border-radius: 20px;
                padding: 3rem;
                margin-top: 2rem;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }}
            
            /* Questionnaire specific styles */
            .question-section {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                border-left: 5px solid #2E86AB;
            }}
            
            .result-section {{
                background: linear-gradient(45deg, #e8f5e8, #f0f8ff);
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                border: 2px solid #4CAF50;
            }}
            </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Background image not found: {e}. Using default background.")

# Set the background
set_background("backgroung.jpg")

# Questionnaire Data
QUESTIONNAIRES = {
    "depression": {
        "name": "Depression Screening (PHQ-9 Inspired)",
        "questions": [
            "Over the past two weeks, how often have you been bothered by feeling down, depressed, or hopeless?",
            "Over the past two weeks, how often have you had little interest or pleasure in doing things?",
            "How is your sleep?",
            "How is your energy level?",
            "How do you feel about yourself?",
            "How is your ability to concentrate?"
        ],
        "options": {
            "q1_q2": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
            "q3_q6": ["Normal", "Some issues", "Severe problems"]
        }
    },
    "anxiety": {
        "name": "Anxiety Screening (GAD-7 Inspired)",
        "questions": [
            "How often do you feel nervous, anxious, or on edge?",
            "How often do you feel unable to stop or control your worrying?",
            "How often do you feel restless, keyed up, or on edge?",
            "How often do you become easily annoyed or irritable?",
            "Do you experience physical symptoms when you're anxious?"
        ],
        "options": ["Not at all", "Some of the time", "Most of the time"]
    },
    "burnout": {
        "name": "Burnout Assessment",
        "questions": [
            "Do you feel emotionally drained or exhausted by your work or daily tasks?",
            "Have you become more cynical, critical, or detached from your work or colleagues?",
            "Do you feel a sense of reduced accomplishment or ineffectiveness in your role?"
        ],
        "options": ["No", "Sometimes", "Yes, constantly"]
    }
}

def calculate_results(questionnaire_type, answers):
    """Calculate results based on questionnaire type and answers"""
    score = sum(answers)
    
    if questionnaire_type == "depression":
        if score >= 10:
            return "High likelihood of depression", "Based on your responses, you are reporting several symptoms commonly associated with Major Depressive Disorder. It is crucial that you share these results with a doctor or mental health professional."
        elif score >= 5:
            return "Moderate symptoms", "Your answers suggest you may be experiencing a depressive episode. Speaking with a therapist or counselor could be very beneficial."
        else:
            return "Mild symptoms", "You're reporting some symptoms. Consider monitoring your mood and practicing self-care."
    
    elif questionnaire_type == "anxiety":
        if score >= 10:
            return "High anxiety levels", "The pattern of your responses indicates symptoms consistent with an anxiety disorder. A mental health professional can provide strategies to manage this anxiety effectively."
        elif score >= 5:
            return "Moderate anxiety", "You're experiencing some anxiety symptoms. Learning coping strategies could be helpful."
        else:
            return "Mild anxiety", "Your anxiety levels appear manageable, but continue to monitor them."
    
    elif questionnaire_type == "burnout":
        if score >= 6:
            return "High burnout risk", "The symptoms you're describing are strongly aligned with burnout. Addressing this often requires lifestyle changes, setting boundaries, and potentially speaking with a professional."
        elif score >= 3:
            return "Moderate burnout risk", "You're showing some signs of burnout. Consider implementing stress-management techniques."
        else:
            return "Low burnout risk", "You seem to be managing well, but remember to maintain work-life balance."

def display_questionnaire(questionnaire_type):
    """Display a specific questionnaire"""
    questionnaire = QUESTIONNAIRES[questionnaire_type]
    
    st.markdown(f"### {questionnaire['name']}")
    st.markdown("---")
    
    answers = []
    
    for i, question in enumerate(questionnaire['questions']):
        st.markdown(f'<div class="question-section">', unsafe_allow_html=True)
        
        if questionnaire_type == "depression":
            if i < 2:  # First two questions use different options
                options = questionnaire['options']['q1_q2']
            else:
                options = questionnaire['options']['q3_q6']
        else:
            options = questionnaire['options']
        
        answer = st.radio(
            f"{i+1}. {question}",
            options,
            key=f"{questionnaire_type}_{i}"
        )
        
        # Convert answer to score
        score = options.index(answer)
        answers.append(score)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(f"Get Results for {questionnaire['name']}", key=f"btn_{questionnaire_type}"):
        level, recommendation = calculate_results(questionnaire_type, answers)
        total_score = sum(answers)
        
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.success(f"### 📊 Assessment Results")
        st.write(f"*Level:* {level}")
        st.write(f"*Score:* {total_score} out of {len(answers) * (len(options)-1)}")
        st.write(f"*Recommendation:* {recommendation}")
        
        # Disclaimer
        st.warning("""
        *Important Disclaimer:* This is not a diagnostic tool. The results are based on self-reported symptoms 
        and are for informational purposes only. A proper diagnosis can only be made by a qualified mental health 
        professional after a comprehensive evaluation.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# Main app content
st.title("🌿SoulSync: Text Based Mental Health Support System")
st.markdown("### 💫 Your AI companion for mental wellness and support")

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📋 Self-Assessment", "🎯 Quick Tools"])

with tab1:
    # Initialize chat
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history in an expandable section
    with st.expander("💬 Chat History", expanded=True):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Share your thoughts or feelings...")

    if user_input:
        with st.spinner("🤔 Thinking..."):
            try:
                # Use the FAST model
                response = ollama.chat(
                    model="llama3.2:3b", 
                    messages=[{"role": "user", "content": user_input}]
                )
                ai_response = response['message']['content']
                
                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("🧠 Mental Health Self-Assessment")
    st.markdown("""
    Select a questionnaire below to assess different aspects of your mental health. 
    These tools can help you understand your current state and provide guidance on next steps.
    """)
    
    # Questionnaire selection
    assessment_type = st.selectbox(
        "Choose an assessment:",
        ["Select an assessment", "Depression Screening", "Anxiety Screening", "Burnout Assessment"]
    )
    
    if assessment_type == "Depression Screening":
        display_questionnaire("depression")
    elif assessment_type == "Anxiety Screening":
        display_questionnaire("anxiety")
    elif assessment_type == "Burnout Assessment":
        display_questionnaire("burnout")
    else:
        st.info("👆 Please select an assessment from the dropdown above to begin.")

with tab3:
    # Quick action buttons with icons
    st.subheader("🎯 Quick Support Tools")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("😊 *Get Affirmation*", use_container_width=True):
            with st.spinner("✨ Creating affirmation..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=[{"role": "user", "content": "Give a positive, uplifting one-sentence affirmation for mental wellness"}]
                    )
                    st.success(f"*Affirmation:* {response['message']['content']}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col2:
        if st.button("🧘 *Mindfulness*", use_container_width=True):
            with st.spinner("🌱 Preparing mindfulness exercise..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b", 
                        messages=[{"role": "user", "content": "Provide a brief 30-second mindfulness or breathing exercise"}]
                    )
                    st.info(f"*Mindfulness Exercise:* {response['message']['content']}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col3:
        if st.button("🌞 *Motivation*", use_container_width=True):
            with st.spinner("💪 Generating motivation..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b", 
                        messages=[{"role": "user", "content": "Give a short motivational quote for someone feeling down"}]
                    )
                    st.success(f"*Motivation:* {response['message']['content']}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col4:
        if st.button("😴 *Sleep Aid*", use_container_width=True):
            with st.spinner("🌙 Preparing sleep help..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b", 
                        messages=[{"role": "user", "content": "Suggest one simple technique for better sleep"}]
                    )
                    st.info(f"*Sleep Tip:* {response['message']['content']}")
                except Exception as e:
                    st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤝 Remember: This AI companion is here to support you, but it's not a replacement for professional help.</p>
    <p>If you're in crisis, please contact a mental health professional or emergency services.</p>
</div>
""", unsafe_allow_html=True)

st.caption("🌿 Using llama3.2:3b AI Model | Mental Health Support Chatbot v2.0")