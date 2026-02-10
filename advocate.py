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
    /* Conversation styling */
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
        position: relative;
        animation: slideInRight 0.3s ease;
    }
    
    .message-human:before {
        content: "👤";
        position: absolute;
        left: -40px;
        top: 12px;
        font-size: 1.3rem;
        background: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .message-ai {
        background: linear-gradient(135deg, #0d9d58, #0a8043);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 12px auto 12px 0;
        max-width: 75%;
        box-shadow: 0 3px 10px rgba(13, 157, 88, 0.2);
        position: relative;
        animation: slideInLeft 0.3s ease;
    }
    
    .message-ai:before {
        content: "🤖";
        position: absolute;
        right: -40px;
        top: 12px;
        font-size: 1.3rem;
        background: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.9;
        text-align: right;
        margin-top: 8px;
        font-weight: 300;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-30px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 15px;
        background: #f0f0f0;
        border-radius: 20px;
        width: fit-content;
        margin: 10px 0;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #666;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        background: #e3f2fd;
        color: #1a73e8;
        border: 2px solid #1a73e8;
        padding: 10px 16px;
        border-radius: 25px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: 500;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .quick-action-btn:hover {
        background: #1a73e8;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 115, 232, 0.3);
    }
    
    /* Main containers */
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

# AI Response Generator - Enhanced
class AIAdvocateAssistant:
    def __init__(self):
        self.name = "Alex"
        self.role = "Human AI Advocate"
        self.conversation_memory = []
        self.knowledge_base = self.load_knowledge_base()
        
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
                    "resources": ["GDPR guidelines", "Privacy by Design framework", "Data protection laws"]
                },
                "non_discrimination": {
                    "description": "AI must not discriminate based on protected characteristics like race, gender, age, or disability.",
                    "violations": ["Biased hiring algorithms", "Discriminatory loan approvals", "Unequal healthcare access"],
                    "solutions": ["Request bias audits", "Demand diverse training data", "Advocate for fairness testing"],
                    "resources": ["Algorithmic fairness toolkit", "Bias assessment framework", "Fairness metrics guide"]
                },
                "transparency": {
                    "description": "Humans have the right to understand AI decisions affecting their lives.",
                    "violations": ["Black box algorithms", "Lack of explanation", "Secret AI systems"],
                    "solutions": ["Demand explainable AI", "Request decision documentation", "Advocate for transparency laws"],
                    "resources": ["Explainable AI guidelines", "Transparency assessment tools", "Right to explanation guide"]
                }
            }
        }
    
    def generate_response(self, user_input: str) -> Dict:
        """Generate AI response based on user input"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        user_input_lower = user_input.lower()
        
        # Update conversation memory
        self.conversation_memory.append({
            "role": "human",
            "content": user_input,
            "time": current_time
        })
        
        # Determine response type
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'start']):
            response = random.choice(self.knowledge_base["greetings"])
            response_type = "greeting"
        elif any(word in user_input_lower for word in ['privacy', 'data', 'surveillance']):
            response = self._generate_privacy_response()
            response_type = "privacy"
        elif any(word in user_input_lower for word in ['discrimination', 'bias', 'fair', 'unfair']):
            response = self._generate_discrimination_response()
            response_type = "discrimination"
        elif any(word in user_input_lower for word in ['transparent', 'explain', 'black box']):
            response = self._generate_transparency_response()
            response_type = "transparency"
        elif any(word in user_input_lower for word in ['help', 'assist', 'support']):
            response = "I can help you with: 1) Understanding AI human rights violations 2) Developing advocacy strategies 3) Documenting cases 4) Connecting with resources 5) Taking legal/policy action. What specific help do you need?"
            response_type = "help"
        elif any(word in user_input_lower for word in ['report', 'violation', 'issue', 'problem']):
            response = "I can help you report an AI human rights violation. Please provide details about: 1) What AI system is involved 2) Which human right is affected 3) Who is being harmed 4) What evidence you have 5) What outcome you're seeking."
            response_type = "report"
        else:
            response = "I understand you're concerned about AI and human rights. Could you tell me more about your specific situation? I can help with advocacy strategies, legal options, or connecting you with relevant resources."
            response_type = "general"
        
        # Generate follow-up questions
        follow_up = self._generate_follow_up(response_type)
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(response_type)
        
        # Update conversation memory with AI response
        self.conversation_memory.append({
            "role": "ai",
            "content": response,
            "time": current_time
        })
        
        return {
            "text": response,
            "follow_up": follow_up,
            "suggested_actions": suggested_actions,
            "time": current_time,
            "response_type": response_type
        }
    
    def _generate_privacy_response(self) -> str:
        info = self.knowledge_base["human_rights"]["privacy"]
        return f"Regarding privacy rights: {info['description']} Common violations include {', '.join(info['violations'][:2])}. Solutions involve {', '.join(info['solutions'][:2])}."
    
    def _generate_discrimination_response(self) -> str:
        info = self.knowledge_base["human_rights"]["non_discrimination"]
        return f"Regarding non-discrimination: {info['description']} Common violations include {', '.join(info['violations'][:2])}. Solutions involve {', '.join(info['solutions'][:2])}."
    
    def _generate_transparency_response(self) -> str:
        info = self.knowledge_base["human_rights"]["transparency"]
        return f"Regarding transparency: {info['description']} Common violations include {', '.join(info['violations'][:2])}. Solutions involve {', '.join(info['solutions'][:2])}."
    
    def _generate_follow_up(self, response_type: str) -> List[str]:
        """Generate relevant follow-up questions"""
        if response_type == "privacy":
            return [
                "Would you like to know about data protection regulations?",
                "Should we discuss consent mechanisms for AI systems?",
                "Are you interested in privacy-preserving AI techniques?"
            ]
        elif response_type == "discrimination":
            return [
                "Would you like guidance on conducting bias audits?",
                "Should we discuss diversity in AI development teams?",
                "Are you interested in fairness metrics and evaluation?"
            ]
        elif response_type == "report":
            return [
                "Can you describe the AI system involved?",
                "How many people are affected by this issue?",
                "What evidence do you currently have?"
            ]
        else:
            return [
                "What aspect of AI human rights concerns you most?",
                "Have you encountered specific AI systems causing harm?",
                "What outcome are you hoping to achieve?"
            ]
    
    def _generate_suggested_actions(self, response_type: str) -> List[str]:
        """Generate suggested actions based on the conversation"""
        if response_type == "privacy":
            return [
                "📝 Document the privacy violation with timestamps",
                "🔍 Review privacy policies of the AI system",
                "📋 Collect evidence of data misuse",
                "⚖️ Consider filing a data protection complaint"
            ]
        elif response_type == "discrimination":
            return [
                "📊 Gather demographic data of affected groups",
                "🔍 Request bias audit from the system owner",
                "🤝 Connect with others facing similar discrimination",
                "⚖️ Explore legal options for redress"
            ]
        elif response_type == "report":
            return [
                "📅 Create a timeline of events",
                "📸 Capture screenshots or recordings",
                "👥 Identify other affected individuals",
                "📋 Organize evidence systematically"
            ]
        else:
            return [
                "📚 Research relevant laws and regulations",
                "🤝 Identify advocacy groups working on similar issues",
                "📝 Start documenting your concerns",
                "🗣️ Prepare to speak with affected parties"
            ]

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
    
    user_name = st.text_input("Your Name", value=st.session_state.user_profile['name'])
    if user_name != st.session_state.user_profile['name']:
        st.session_state.user_profile['name'] = user_name
    
    st.markdown(f"**Interactions:** {st.session_state.user_profile['interaction_count']}")
    
    st.markdown("---")
    
    # Quick Topics
    st.markdown("### 💡 Quick Topics")
    
    topics = [
        "🔒 AI Privacy Violation",
        "⚖️ Algorithmic Discrimination", 
        "🔍 Transparency Issues",
        "📋 Report a Case",
        "🚀 Advocacy Strategies"
    ]
    
    for topic in topics:
        if st.button(topic, use_container_width=True, key=f"topic_{topic}"):
            user_msg = f"I want to discuss {topic.split(' ')[-2:]}"
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
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
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
    st.markdown('<div class="conversation-container" id="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.conversation_history:
        # Initial greeting
        initial_greeting = ai_assistant.generate_response("hello")
        add_message("ai", initial_greeting["text"], 
                   initial_greeting["follow_up"],
                   initial_greeting["suggested_actions"])
    
    # Display conversation
    for msg in st.session_state.conversation_history:
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
                for question in msg["follow_up"]:
                    question_hash = hash(question) % 10000
                    if st.button(f"💭 {question}", key=f"follow_{question_hash}"):
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Section
    st.markdown("### 📝 Continue the Conversation")
    
    # Text input
    user_text = st.text_area(
        "Type your message:",
        placeholder="Describe your AI human rights concern, ask for advice, or discuss advocacy strategies...",
        height=100,
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        if st.button("📤 Send Message", use_container_width=True, disabled=not user_text.strip()):
            add_message("human", user_text.strip())
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_text.strip())
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"])
            
            st.rerun()
    
    with col2:
        if st.button("💡 Quick Help", use_container_width=True):
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
    **Specialties:** Human rights, Legal strategy, Policy advocacy
    
    ### 🎯 Current Focus:
    - Privacy protection in surveillance AI
    - Bias mitigation in hiring algorithms  
    - Transparency in automated decision-making
    
    ### 📚 Recent Successes:
    ✅ Helped 50+ individuals report violations  
    ✅ Contributed to 3 policy changes  
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
        st.metric("Total Words", total_words)
    else:
        st.info("Start talking to see insights!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Resources
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📚 Quick Resources")
    
    resources = [
        "📖 AI Human Rights Handbook",
        "⚖️ Legal Complaint Template",
        "📊 Advocacy Strategy Guide",
        "🔍 Bias Detection Toolkit"
    ]
    
    for resource in resources:
        if st.button(resource, use_container_width=True, key=f"res_{resource}"):
            st.success(f"Opening {resource}...")

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-top: 30px;">
    <h4 style="color: #1a73e8 !important;">🤖💬 Human AI Advocate Assistant</h4>
    <p>Protecting human dignity through AI-human collaboration</p>
    <div style="margin-top: 20px; color: #666; font-size: 0.9rem;">
        Built for ethical AI advocacy • Privacy-focused • Last updated: {}
    </div>
</div>
""".format(datetime.datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# Auto-refresh for conversation updates
if st.checkbox("🔄 Enable auto-refresh (every 5 seconds)", value=False):
    time.sleep(5)
    st.rerun()
