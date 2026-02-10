import streamlit as st
import pandas as pd
import datetime
import random
import time
import json
import base64
from typing import List, Dict, Optional

# Initialize session state for conversation
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'advocacy_cases' not in st.session_state:
    st.session_state.advocacy_cases = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Human Advocate',
        'concerns': [],
        'interaction_count': 0
    }

# Page configuration
st.set_page_config(
    page_title="Human AI Advocate",
    page_icon="🤖💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with conversation styling
st.markdown("""
<style>
    .conversation-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 15px;
        margin: 20px 0;
        border: 2px solid #e3e3e3;
    }
    
    .message-human {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 12px 0 12px auto;
        max-width: 75%;
        box-shadow: 0 3px 10px rgba(26, 115, 232, 0.2);
    }
    
    .message-ai {
        background: linear-gradient(135deg, #0d9d58, #0a8043);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        box-shadow: 0 3px 10px rgba(13, 157, 88, 0.2);
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.9;
        text-align: right;
        margin-top: 8px;
        font-weight: 300;
    }
    
    .main-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #eaeaea;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white !important;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# AI Response Generator
class AIAdvocateAssistant:
    def __init__(self):
        self.name = "Alex"
        self.role = "Human AI Advocate"
        self.conversation_memory = []
        
    def load_knowledge_base(self):
        return {
            "greetings": [
                "Hello! I'm Alex, your Human AI Advocate. I'm here to help protect human dignity in the age of AI. What concerns do you have today?",
                "Welcome! As your AI ethics advocate, I'm ready to discuss how we can ensure AI systems respect human rights. How can I assist you?",
                "Hi there! I'm here to support you in navigating AI-related human rights issues. What would you like to discuss?"
            ],
            "human_rights": {
                "privacy": {
                    "description": "The right to privacy in AI includes data protection, informed consent, and control over personal information.",
                    "violations": ["Mass surveillance", "Data collection without consent", "Unauthorized data sharing"],
                    "solutions": ["Demand transparency reports", "Exercise data rights", "Support privacy legislation"],
                },
                "non_discrimination": {
                    "description": "AI must not discriminate based on protected characteristics like race, gender, age, or disability.",
                    "violations": ["Biased hiring algorithms", "Discriminatory loan approvals", "Unequal healthcare access"],
                    "solutions": ["Request bias audits", "Demand diverse training data", "Advocate for fairness testing"],
                }
            }
        }
    
    def generate_response(self, user_input: str) -> Dict:
        """Generate AI response based on user input"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        user_input_lower = user_input.lower()
        
        # Determine response type
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'start']):
            response = random.choice([
                "Hello! I'm Alex, your Human AI Advocate. I'm here to help protect human dignity in the age of AI. What concerns do you have today?",
                "Welcome! I'm ready to discuss how we can ensure AI systems respect human rights. How can I assist you?"
            ])
            response_type = "greeting"
            follow_up = ["What aspect of AI human rights concerns you most?", "Have you encountered specific AI systems causing harm?"]
            actions = ["📚 Research relevant laws", "🤝 Identify advocacy groups", "📝 Start documenting concerns"]
            
        elif any(word in user_input_lower for word in ['privacy', 'data', 'surveillance']):
            response = "Regarding privacy rights: AI systems must respect data protection, informed consent, and personal information control. Common violations include mass surveillance and unauthorized data sharing. Solutions involve demanding transparency reports and exercising data rights."
            response_type = "privacy"
            follow_up = ["Would you like to know about data protection regulations?", "Should we discuss consent mechanisms?"]
            actions = ["📝 Document the privacy violation", "🔍 Review privacy policies", "📋 Collect evidence of data misuse"]
            
        elif any(word in user_input_lower for word in ['discrimination', 'bias', 'fair', 'unfair']):
            response = "Regarding non-discrimination: AI must not discriminate based on protected characteristics. Common violations include biased hiring algorithms and discriminatory loan approvals. Solutions involve requesting bias audits and demanding diverse training data."
            response_type = "discrimination"
            follow_up = ["Would you like guidance on conducting bias audits?", "Should we discuss diversity in AI teams?"]
            actions = ["📊 Gather demographic data", "🔍 Request bias audit", "🤝 Connect with affected groups"]
            
        elif any(word in user_input_lower for word in ['help', 'assist', 'support']):
            response = "I can help you with: 1) Understanding AI human rights violations 2) Developing advocacy strategies 3) Documenting cases 4) Connecting with resources 5) Taking legal/policy action. What specific help do you need?"
            response_type = "help"
            follow_up = ["What human right is being affected?", "Can you describe the AI system involved?"]
            actions = ["📚 Research your rights", "📝 Document the situation", "🗣️ Prepare to speak about it"]
            
        elif any(word in user_input_lower for word in ['report', 'violation', 'issue', 'problem']):
            response = "I can help you report an AI human rights violation. Please provide details about: 1) What AI system is involved 2) Which human right is affected 3) Who is being harmed 4) What evidence you have 5) What outcome you're seeking."
            response_type = "report"
            follow_up = ["Can you describe the AI system involved?", "How many people are affected?"]
            actions = ["📅 Create a timeline of events", "📸 Capture screenshots", "👥 Identify other affected individuals"]
            
        else:
            response = "I understand you're concerned about AI and human rights. Could you tell me more about your specific situation? I can help with advocacy strategies, legal options, or connecting you with relevant resources."
            response_type = "general"
            follow_up = ["What aspect of AI human rights concerns you most?", "What outcome are you hoping to achieve?"]
            actions = ["📚 Research relevant laws", "🤝 Identify advocacy groups", "📝 Start documenting your concerns"]
        
        return {
            "text": response,
            "follow_up": follow_up,
            "suggested_actions": actions,
            "time": current_time,
            "response_type": response_type
        }

# Initialize AI Assistant
ai_assistant = AIAdvocateAssistant()

# Add message to conversation
def add_message(sender: str, text: str, follow_up: List[str] = None, 
                actions: List[str] = None):
    """Add a message to the conversation history"""
    message = {
        "sender": sender,
        "text": text,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "follow_up": follow_up or [],
        "suggested_actions": actions or []
    }
    
    st.session_state.conversation_history.append(message)
    st.session_state.user_profile['interaction_count'] += 1

# Sidebar
with st.sidebar:
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("## 🤖💬 AI Advocate Assistant")
    st.markdown("Conversation interface for human rights advocacy")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User Profile
    st.markdown("### 👤 Your Profile")
    
    user_name = st.text_input("Your Name", value=st.session_state.user_profile['name'], 
                             key="sidebar_user_name")
    if user_name != st.session_state.user_profile['name']:
        st.session_state.user_profile['name'] = user_name
    
    st.markdown(f"**Interactions:** {st.session_state.user_profile['interaction_count']}")
    
    st.markdown("---")
    
    # Quick Topics with unique keys
    st.markdown("### 💡 Quick Topics")
    
    topics = [
        ("🔒", "AI Privacy Violation", "topic_privacy"),
        ("⚖️", "Algorithmic Discrimination", "topic_discrimination"), 
        ("🔍", "Transparency Issues", "topic_transparency"),
        ("📋", "Report a Case", "topic_report"),
        ("🚀", "Advocacy Strategies", "topic_strategies")
    ]
    
    for icon, topic, key in topics:
        if st.button(f"{icon} {topic}", use_container_width=True, key=key):
            user_msg = f"I want to discuss {topic.lower()}"
            add_message("human", user_msg)
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_msg)
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"])
            
            st.rerun()
    
    st.markdown("---")
    
    # Conversation Management
    st.markdown("### ⚙️ Conversation Tools")
    
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat"):
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True, key="export_chat"):
        if st.session_state.conversation_history:
            # Create download link
            text_content = f"AI Advocate Conversation with {st.session_state.user_profile['name']}\n"
            text_content += "="*50 + "\n\n"
            
            for msg in st.session_state.conversation_history:
                sender = "You" if msg["sender"] == "human" else "AI Advocate"
                text_content += f"{sender} ({msg['time']}):\n{msg['text']}\n\n"
            
            b64 = base64.b64encode(text_content.encode()).decode()
            st.markdown(f'<a href="data:file/txt;base64,{b64}" download="ai_advocate_chat.txt">📥 Download Conversation</a>', unsafe_allow_html=True)

# Main Content
st.markdown("""
<div class="highlight-box">
    <h1 style="text-align: center; color: white !important; margin-bottom: 10px;">🤖💬 Human AI Advocate Assistant</h1>
    <p style="text-align: center; color: white !important; font-size: 1.2rem; opacity: 0.9;">
        Protecting human dignity through AI-human collaboration
    </p>
</div>
""", unsafe_allow_html=True)

# Two main columns
col_main1, col_main2 = st.columns([3, 1])

with col_main1:
    # Conversation Interface
    st.markdown("## 💬 Live Conversation")
    
    # Conversation Display Container
    conversation_container = st.container()
    
    with conversation_container:
        st.markdown('<div class="conversation-container" id="chat-container">', unsafe_allow_html=True)
        
        if not st.session_state.conversation_history:
            # Initial greeting
            initial_greeting = ai_assistant.generate_response("hello")
            add_message("ai", initial_greeting["text"], 
                       initial_greeting["follow_up"],
                       initial_greeting["suggested_actions"])
        
        # Display conversation
        for idx, msg in enumerate(st.session_state.conversation_history):
            if msg["sender"] == "human":
                st.markdown(f'''
                <div class="message-human">
                    {msg["text"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="message-ai">
                    {msg["text"]}
                    <div class="message-time">{msg["time"]}</div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Show follow-up questions
                if msg.get("follow_up"):
                    st.markdown("**💭 Follow-up questions:**")
                    for q_idx, question in enumerate(msg["follow_up"]):
                        # Create unique key using message index and question index
                        unique_key = f"followup_{idx}_{q_idx}_{hash(question) % 10000}"
                        if st.button(f"💭 {question}", key=unique_key):
                            add_message("human", question)
                            ai_response = ai_assistant.generate_response(question)
                            add_message("ai", ai_response["text"], 
                                       ai_response["follow_up"],
                                       ai_response["suggested_actions"])
                            st.rerun()
                
                # Show suggested actions
                if msg.get("suggested_actions"):
                    st.markdown("**🎯 Suggested actions:**")
                    for action in msg["suggested_actions"]:
                        st.write(f"• {action}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown("### 📝 Continue the Conversation")
    
    # Text input
    user_text = st.text_area(
        "Type your message:",
        placeholder="Describe your AI human rights concern, ask for advice, or discuss advocacy strategies...",
        height=100,
        label_visibility="collapsed",
        key="main_text_input"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.button("📤 Send Message", use_container_width=True, 
                    disabled=not user_text.strip(), key="send_main"):
            add_message("human", user_text.strip())
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_text.strip())
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"])
            
            st.rerun()
    
    with col2:
        if st.button("💡 Quick Help", use_container_width=True, key="quick_help"):
            add_message("human", "I need help understanding my options")
            ai_response = ai_assistant.generate_response("help")
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"])
            st.rerun()

with col_main2:
    # AI Advocate Profile
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🤖 AI Advocate Profile")
    
    st.markdown(f"""
    **Name:** {ai_assistant.name}  
    **Role:** {ai_assistant.role}  
    **Experience:** 5+ years in AI ethics advocacy  
    
    ### 🎯 Current Focus:
    - Privacy protection in AI
    - Bias mitigation  
    - Transparency advocacy
    
    ### 📚 Recent Successes:
    ✅ Helped 50+ individuals  
    ✅ Contributed to policy changes  
    ✅ Trained 200+ advocates
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation Insights
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📈 Conversation Insights")
    
    if st.session_state.conversation_history:
        # Analyze conversation
        topics_discussed = set()
        for msg in st.session_state.conversation_history:
            text = msg["text"].lower()
            if "privacy" in text:
                topics_discussed.add("🔒 Privacy")
            if any(word in text for word in ['bias', 'discrimination', 'fair']):
                topics_discussed.add("⚖️ Discrimination")
            if "transparency" in text:
                topics_discussed.add("🔍 Transparency")
        
        st.markdown("**Topics discussed:**")
        for topic in topics_discussed:
            st.markdown(f"• {topic}")
        
        # Conversation length
        total_words = sum(len(msg["text"].split()) for msg in st.session_state.conversation_history)
        st.metric("Total Words", total_words, key="word_count")
    else:
        st.info("Start talking to see insights!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Resources with unique keys
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📚 Quick Resources")
    
    resources = [
        ("📖", "AI Human Rights Handbook", "res_handbook"),
        ("⚖️", "Legal Complaint Template", "res_legal"),
        ("📊", "Advocacy Strategy Guide", "res_strategy"),
        ("🔍", "Bias Detection Toolkit", "res_bias")
    ]
    
    for icon, resource, key in resources:
        if st.button(f"{icon} {resource}", use_container_width=True, key=key):
            st.success(f"Opening {resource}...")

# Auto-scroll JavaScript
st.markdown("""
<script>
    // Auto-scroll to bottom
    var container = document.getElementById('chat-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-top: 30px;">
    <h4 style="color: #1a73e8 !important;">🤖💬 Human AI Advocate Assistant</h4>
    <p>Protecting human dignity through AI-human collaboration</p>
    <div style="margin-top: 20px; color: #666; font-size: 0.9rem;">
        Built for ethical AI advocacy • Last updated: {}
    </div>
</div>
""".format(datetime.datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# Auto-refresh option
if st.checkbox("🔄 Enable auto-refresh (every 10 seconds)", value=False, key="auto_refresh"):
    time.sleep(10)
    st.rerun()
