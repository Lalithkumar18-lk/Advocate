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
    
    /* Follow-up questions */
    .follow-up-question {
        background: #fff3e0;
        color: #ef6c00;
        border: 1px solid #ffb74d;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 0.95rem;
    }
    
    .follow-up-question:hover {
        background: #ffb74d;
        color: white;
        transform: translateX(5px);
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
    
    /* Topic bubbles */
    .topic-bubble {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 8px;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid transparent;
        font-weight: 500;
        box-shadow: 0 3px 8px rgba(102, 126, 234, 0.2);
    }
    
    .topic-bubble:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
        border-color: white;
    }
    
    /* Conversation input */
    .conversation-input {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #e3e3e3;
        margin: 20px 0;
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        border-top: 4px solid #1a73e8;
        transition: transform 0.3s;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .message-human, .message-ai {
            max-width: 85%;
        }
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
                },
                "accountability": {
                    "description": "When AI causes harm, there must be clear accountability and redress mechanisms.",
                    "violations": ["No human oversight", "Lack of grievance procedures", "No legal recourse"],
                    "solutions": ["Demand human review processes", "Establish oversight committees", "Create compensation mechanisms"],
                    "resources": ["Accountability framework", "Oversight guidelines", "Redress mechanisms"]
                }
            },
            "advocacy_strategies": {
                "legal": [
                    "File human rights complaints with relevant authorities",
                    "Initiate class action lawsuits for group violations",
                    "Submit legal petitions for injunctions",
                    "Engage with human rights commissions",
                    "Use freedom of information requests"
                ],
                "policy": [
                    "Lobby for AI regulation legislation",
                    "Propose ethical AI guidelines",
                    "Participate in public consultations",
                    "Submit policy recommendations",
                    "Build coalitions with other organizations"
                ],
                "public": [
                    "Launch public awareness campaigns",
                    "Organize community workshops",
                    "Create educational materials",
                    "Use social media for advocacy",
                    "Engage with traditional media"
                ],
                "technical": [
                    "Request algorithmic impact assessments",
                    "Demand source code audits",
                    "Propose technical safeguards",
                    "Develop monitoring tools",
                    "Create alternative ethical systems"
                ]
            },
            "conversation_patterns": {
                "empathy": [
                    "I understand this must be concerning for you.",
                    "That sounds like a serious issue that needs attention.",
                    "Thank you for bringing this to my attention.",
                    "I can see why this would be troubling."
                ],
                "clarification": [
                    "Could you tell me more about the specific AI system involved?",
                    "How many people are affected by this issue?",
                    "What evidence do you have of the violation?",
                    "How long has this been going on?"
                ],
                "action": [
                    "Based on what you've described, here are some immediate steps...",
                    "I recommend we start by documenting everything.",
                    "Let me help you develop a strategy to address this.",
                    "Here are some resources that might be helpful."
                ]
            }
        }
    
    def generate_response(self, user_input: str, context: List[Dict] = None) -> Dict:
        """Generate AI response based on user input with context awareness"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        user_input_lower = user_input.lower()
        
        # Update conversation memory
        self.conversation_memory.append({
            "role": "human",
            "content": user_input,
            "time": current_time
        })
        
        # Determine response type
        response_type = self._determine_response_type(user_input_lower)
        
        # Generate appropriate response
        if response_type == "greeting":
            response = self._generate_greeting_response()
        elif response_type == "human_rights":
            response = self._generate_human_rights_response(user_input_lower)
        elif response_type == "advocacy":
            response = self._generate_advocacy_response(user_input_lower)
        elif response_type == "case_report":
            response = self._generate_case_response()
        elif response_type == "help":
            response = self._generate_help_response()
        else:
            response = self._generate_general_response(user_input_lower)
        
        # Add empathy and personalization
        empathy = random.choice(self.knowledge_base["conversation_patterns"]["empathy"])
        full_response = f"{empathy} {response}"
        
        # Generate follow-up questions
        follow_up = self._generate_follow_up_questions(user_input_lower, response_type)
        
        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(user_input_lower, response_type)
        
        # Update conversation memory with AI response
        self.conversation_memory.append({
            "role": "ai",
            "content": full_response,
            "time": current_time
        })
        
        return {
            "text": full_response,
            "follow_up": follow_up,
            "suggested_actions": suggested_actions,
            "time": current_time,
            "response_type": response_type
        }
    
    def _determine_response_type(self, user_input: str) -> str:
        """Determine the type of response needed"""
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings', 'start']):
            return "greeting"
        elif any(word in user_input for word in ['privacy', 'discrimination', 'bias', 'transparent', 'accountability', 'right']):
            return "human_rights"
        elif any(word in user_input for word in ['strategy', 'plan', 'action', 'advocate', 'campaign']):
            return "advocacy"
        elif any(word in user_input for word in ['report', 'violation', 'issue', 'problem', 'complaint', 'case']):
            return "case_report"
        elif any(word in user_input for word in ['help', 'assist', 'support', 'what can', 'how to']):
            return "help"
        else:
            return "general"
    
    def _generate_greeting_response(self) -> str:
        return random.choice(self.knowledge_base["greetings"])
    
    def _generate_human_rights_response(self, user_input: str) -> str:
        for right in self.knowledge_base["human_rights"]:
            if right in user_input:
                right_info = self.knowledge_base["human_rights"][right]
                return f"Regarding {right.replace('_', ' ')}: {right_info['description']} Common violations include {', '.join(right_info['violations'][:2])}. Solutions involve {', '.join(right_info['solutions'][:2])}."
        return "I understand you're concerned about human rights in AI. Could you specify which right you're most worried about?"
    
    def _generate_advocacy_response(self, user_input: str) -> str:
        strategies = []
        for strategy_type in self.knowledge_base["advocacy_strategies"]:
            if strategy_type in user_input:
                strategies.extend(self.knowledge_base["advocacy_strategies"][strategy_type][:2])
        
        if strategies:
            return f"Here are some advocacy strategies: {'; '.join(strategies)}. The most effective approach often combines multiple strategies."
        return "Effective advocacy requires a multi-pronged approach. We can consider legal actions, public campaigns, policy work, and technical solutions."
    
    def _generate_case_response(self) -> str:
        return "To document a case effectively, I'll help you gather: 1) Details about the AI system, 2) Specific human rights affected, 3) Evidence of harm, 4) People impacted, 5) Desired outcome. Let's start with the first point."
    
    def _generate_help_response(self) -> str:
        return "I can help you with: 1) Understanding AI human rights violations, 2) Developing advocacy strategies, 3) Documenting cases, 4) Connecting with resources, 5) Taking action. What do you need most right now?"
    
    def _generate_general_response(self, user_input: str) -> str:
        return "I understand you're concerned about AI and human rights. Could you tell me more about your specific situation? I'm here to listen and help you develop effective responses."
    
    def _generate_follow_up_questions(self, user_input: str, response_type: str) -> List[str]:
        """Generate relevant follow-up questions"""
        questions = []
        
        if response_type == "human_rights":
            questions = [
                "Would you like to know more about documenting this type of violation?",
                "Should we discuss specific advocacy strategies for this issue?",
                "Are there particular groups being affected that we should focus on?"
            ]
        elif response_type == "case_report":
            questions = [
                "Can you describe the AI system involved?",
                "How many people are affected by this issue?",
                "What evidence do you currently have?"
            ]
        elif response_type == "advocacy":
            questions = [
                "What resources do you have available for advocacy?",
                "Who are the key stakeholders we should engage?",
                "What's your timeline for taking action?"
            ]
        else:
            questions = [
                "What aspect of AI human rights concerns you most?",
                "Have you encountered specific AI systems causing harm?",
                "What outcome are you hoping to achieve?"
            ]
        
        return questions[:3]  # Return max 3 questions
    
    def _generate_suggested_actions(self, user_input: str, response_type: str) -> List[str]:
        """Generate suggested actions based on the conversation"""
        actions = []
        
        if "privacy" in user_input:
            actions = [
                "📝 Document the privacy violation with timestamps",
                "🔍 Review privacy policies of the AI system",
                "📋 Collect evidence of data misuse",
                "⚖️ Consider filing a data protection complaint"
            ]
        elif any(word in user_input for word in ['discrimination', 'bias']):
            actions = [
                "📊 Gather demographic data of affected groups",
                "🔍 Request bias audit from the system owner",
                "🤝 Connect with others facing similar discrimination",
                "⚖️ Explore legal options for redress"
            ]
        elif response_type == "case_report":
            actions = [
                "📅 Create a timeline of events",
                "📸 Capture screenshots or recordings",
                "👥 Identify other affected individuals",
                "📋 Organize evidence systematically"
            ]
        
        return actions[:4]  # Return max 4 actions

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
        "🎯 Accountability Concerns",
        "📋 Report a Case",
        "🚀 Advocacy Strategies",
        "💼 Right to Work",
        "🏥 Right to Health"
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
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.conversation_history = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            if st.session_state.conversation_history:
                # Create download link
                text_content = f"AI Advocate Conversation with {st.session_state.user_profile['name']}\n"
                text_content += "="*50 + "\n\n"
                
                for msg in st.session_state.conversation_history:
                    sender = "You" if msg["sender"] == "human" else "AI Advocate"
                    text_content += f"{sender} ({msg['time']}):\n{msg['text']}\n\n"
                
                b64 = base64.b64encode(text_content.encode()).decode()
                href = f'<a href="data:file/txt;base64,{b64}" download="ai_advocate_chat.txt">📥 Download Conversation</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Conversation Stats")
    
    if st.session_state.conversation_history:
        human_msgs = len([m for m in st.session_state.conversation_history if m["sender"] == "human"])
        ai_msgs = len([m for m in st.session_state.conversation_history if m["sender"] == "ai"])
        
        st.metric("Your Messages", human_msgs)
        st.metric("AI Responses", ai_msgs)
    else:
        st.info("Start a conversation to see stats!")

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
    
    # Typing indicator (simulated)
    if st.session_state.conversation_history and st.session_state.conversation_history[-1]["sender"] == "human":
        st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <span style="margin-left: 10px; color: #666;">AI Advocate is thinking...</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Input Section
    st.markdown('<div class="conversation-input">', unsafe_allow_html=True)
    st.markdown("### 📝 Continue the Conversation")
    
    # Quick action buttons
    st.markdown("**Quick actions:**")
    
    quick_cols = st.columns(4)
    quick_actions = [
        ("📋", "Start a new case"),
        ("⚖️", "Get legal advice"),
        ("🎯", "Strategy planning"),
        ("🔗", "Need resources")
    ]
    
    for idx, (icon, action) in enumerate(quick_actions):
        with quick_cols[idx]:
            if st.button(f"{icon} {action}", use_container_width=True):
                add_message("human", f"I need help with {action.lower()}")
                ai_response = ai_assistant.generate_response(action)
                add_message("ai", ai_response["text"], 
                           ai_response["follow_up"],
                           ai_response["suggested_actions"])
                st.rerun()
    
    # Text input
    text_col1, text_col2 = st.columns([4, 1])
    
    with text_col1:
        user_text = st.text_area(
            "Type your message:",
            placeholder="Describe your AI human rights concern, ask for advice, or discuss advocacy strategies...",
            height=100,
            label_visibility="collapsed"
        )
    
    with text_col2:
        send_disabled = not user_text.strip()
        if st.button("📤 Send", 
                    use_container_width=True, 
                    disabled=send_disabled,
                    type="primary"):
            add_message("human", user_text.strip())
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_text.strip())
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"])
            
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    - Accountability for AI harms
    
    ### 📚 Recent Successes:
    ✅ Helped 50+ individuals report violations  
    ✅ Contributed to 3 policy changes  
    ✅ Trained 200+ advocates  
    ✅ Published 15+ advocacy guides
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
            if "accountability" in text:
                topics_discussed.add("🎯 Accountability")
        
        st.markdown("**Topics discussed:**")
        for topic in topics_discussed:
            st.markdown(f"• {topic}")
        
        # Conversation length
        total_words = sum(len(msg["text"].split()) for msg in st.session_state.conversation_history)
        st.metric("Total Words", total_words)
        
        # Sentiment (simulated)
        st.markdown("**Conversation tone:**")
        st.progress(75)
        st.caption("75% Constructive & Solution-focused")
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
        "🔍 Bias Detection Toolkit",
        "📋 Case Documentation Form",
        "🎯 Policy Change Framework"
    ]
    
    for resource in resources:
        if st.button(resource, use_container_width=True, key=f"res_{resource}"):
            st.success(f"Opening {resource}...")
            time.sleep(1)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div style="height: 2px; background: linear-gradient(to right, #1a73e8, #0d9d58); margin: 40px 0; border-radius: 2px;"></div>', unsafe_allow_html=True)

# Conversation Examples Section
st.markdown("## 💡 Example Conversations")

example_cols = st.columns(3)

examples = [
    {
        "title": "Privacy Violation",
        "scenario": "Reporting unauthorized facial recognition use",
        "human": "My employer is using facial recognition without our consent",
        "ai": "Let's document this. First, gather evidence of the system and its use..."
    },
    {
        "title": "Algorithmic Bias",
        "scenario": "Discrimination in hiring algorithm",
        "human": "The AI hiring tool is rejecting qualified female candidates",
        "ai": "We need to request a bias audit and document specific cases..."
    },
    {
        "title": "Transparency Issue",
        "scenario": "Black box algorithm denying loans",
        "human": "The bank's AI won't explain why my loan was denied",
        "ai": "You have a right to explanation. Let's draft a formal request..."
    }
]

for idx, example in enumerate(examples):
    with example_cols[idx]:
        st.markdown(f'''
        <div class="stats-card">
            <h4>{example["title"]}</h4>
            <p><em>{example["scenario"]}</em></p>
            <hr style="margin: 10px 0;">
            <p><strong>Human:</strong> "{example["human"]}"</p>
            <p><strong>AI:</strong> "{example["ai"]}"</p>
        </div>
        ''', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 15px; margin-top: 40px;">
    <h3 style="color: #1a73e8 !important; margin-bottom: 20px;">🤖💬 Human AI Advocate Assistant</h3>
    
    <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin: 30px 0;">
        <div>
            <div style="font-size: 2rem;">💬</div>
            <div><strong>Real-time Chat</strong></div>
            <div style="font-size: 0.9rem; color: #666;">Natural conversation</div>
        </div>
        <div>
            <div style="font-size: 2rem;">🎯</div>
            <div><strong>Actionable Advice</strong></div>
            <div style="font-size: 0.9rem; color: #666;">Practical strategies</div>
        </div>
        <div>
            <div style="font-size: 2rem;">⚖️</div>
            <div><strong>Legal Guidance</strong></div>
            <div style="font-size: 0.9rem; color: #666;">Rights protection</div>
        </div>
        <div>
            <div style="font-size: 2rem;">🔗</div>
            <div><strong>Resources</strong></div>
            <div style="font-size: 0.9rem; color: #666;">Tools & templates</div>
        </div>
    </div>
    
    <div style="border-top: 1px solid #ddd; padding-top: 20px; margin-top: 20px;">
