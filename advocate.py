import streamlit as st
import datetime
import random
import time
import base64

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': 'Human Advocate',
        'interaction_count': 0
    }

# Page configuration
st.set_page_config(
    page_title="Human AI Advocate",
    page_icon="🤖💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    
    .quick-topic-btn {
        width: 100%;
        margin: 5px 0;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #1a73e8;
        background: #e3f2fd;
        color: #1a73e8;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .quick-topic-btn:hover {
        background: #1a73e8;
        color: white;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# AI Assistant Class
class AIAdvocateAssistant:
    def __init__(self):
        self.name = "Alex"
        self.role = "Human AI Advocate"
        
    def generate_response(self, user_input: str):
        """Generate AI response based on user input"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self._generate_greeting()
        elif any(word in user_input_lower for word in ['privacy', 'data', 'surveillance']):
            return self._generate_privacy_response()
        elif any(word in user_input_lower for word in ['discrimination', 'bias', 'fair', 'unfair']):
            return self._generate_discrimination_response()
        elif any(word in user_input_lower for word in ['help', 'assist', 'support']):
            return self._generate_help_response()
        elif any(word in user_input_lower for word in ['report', 'violation', 'issue']):
            return self._generate_report_response()
        else:
            return self._generate_general_response()
    
    def _generate_greeting(self):
        greetings = [
            "Hello! I'm Alex, your Human AI Advocate. I'm here to help protect human dignity in the age of AI. What concerns do you have today?",
            "Welcome! I'm ready to discuss how we can ensure AI systems respect human rights. How can I assist you?",
            "Hi there! I'm here to support you in navigating AI-related human rights issues. What would you like to discuss?"
        ]
        return {
            "text": random.choice(greetings),
            "follow_up": ["What aspect of AI human rights concerns you most?", "Have you encountered specific AI systems causing harm?"],
            "actions": ["📚 Research relevant laws", "🤝 Identify advocacy groups"]
        }
    
    def _generate_privacy_response(self):
        return {
            "text": "Regarding privacy rights: AI systems must respect data protection, informed consent, and personal information control. Common violations include mass surveillance and unauthorized data sharing. Solutions involve demanding transparency reports and exercising data rights.",
            "follow_up": ["Would you like to know about data protection regulations?", "Should we discuss consent mechanisms?"],
            "actions": ["📝 Document the privacy violation", "🔍 Review privacy policies", "📋 Collect evidence"]
        }
    
    def _generate_discrimination_response(self):
        return {
            "text": "Regarding non-discrimination: AI must not discriminate based on protected characteristics. Common violations include biased hiring algorithms and discriminatory loan approvals. Solutions involve requesting bias audits and demanding diverse training data.",
            "follow_up": ["Would you like guidance on conducting bias audits?", "Should we discuss diversity in AI teams?"],
            "actions": ["📊 Gather demographic data", "🔍 Request bias audit", "🤝 Connect with affected groups"]
        }
    
    def _generate_help_response(self):
        return {
            "text": "I can help you with: 1) Understanding AI human rights violations 2) Developing advocacy strategies 3) Documenting cases 4) Connecting with resources 5) Taking legal/policy action. What specific help do you need?",
            "follow_up": ["What human right is being affected?", "Can you describe the AI system involved?"],
            "actions": ["📚 Research your rights", "📝 Document the situation", "🗣️ Prepare to speak about it"]
        }
    
    def _generate_report_response(self):
        return {
            "text": "I can help you report an AI human rights violation. Please provide details about: 1) What AI system is involved 2) Which human right is affected 3) Who is being harmed 4) What evidence you have 5) What outcome you're seeking.",
            "follow_up": ["Can you describe the AI system involved?", "How many people are affected?"],
            "actions": ["📅 Create a timeline of events", "📸 Capture screenshots", "👥 Identify other affected individuals"]
        }
    
    def _generate_general_response(self):
        return {
            "text": "I understand you're concerned about AI and human rights. Could you tell me more about your specific situation? I can help with advocacy strategies, legal options, or connecting you with relevant resources.",
            "follow_up": ["What aspect of AI human rights concerns you most?", "What outcome are you hoping to achieve?"],
            "actions": ["📚 Research relevant laws", "🤝 Identify advocacy groups", "📝 Start documenting your concerns"]
        }

# Initialize AI Assistant
ai_assistant = AIAdvocateAssistant()

# Add message to conversation
def add_message(sender: str, text: str, follow_up: list = None, actions: list = None):
    """Add a message to the conversation history"""
    message = {
        "sender": sender,
        "text": text,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "follow_up": follow_up or [],
        "actions": actions or []
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
        ("🔒", "AI Privacy Violation"),
        ("⚖️", "Algorithmic Discrimination"), 
        ("🔍", "Transparency Issues"),
        ("📋", "Report a Case"),
        ("🚀", "Advocacy Strategies")
    ]
    
    for icon, topic in topics:
        if st.button(f"{icon} {topic}", key=f"sidebar_{topic.replace(' ', '_')}"):
            user_msg = f"I want to discuss {topic.lower()}"
            add_message("human", user_msg)
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_msg)
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["actions"])
            
            st.rerun()
    
    st.markdown("---")
    
    # Conversation Management
    st.markdown("### ⚙️ Conversation Tools")
    
    if st.button("🗑️ Clear Chat", key="clear_chat_button"):
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("💾 Export Chat", key="export_chat_button"):
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
    
    # Conversation Display
    st.markdown('<div class="conversation-container" id="chat-container">', unsafe_allow_html=True)
    
    if not st.session_state.conversation_history:
        # Initial greeting
        initial_greeting = ai_assistant.generate_response("hello")
        add_message("ai", initial_greeting["text"], 
                   initial_greeting["follow_up"],
                   initial_greeting["actions"])
    
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
                    unique_key = f"followup_{idx}_{q_idx}"
                    if st.button(f"💭 {question}", key=unique_key):
                        add_message("human", question)
                        ai_response = ai_assistant.generate_response(question)
                        add_message("ai", ai_response["text"], 
                                   ai_response["follow_up"],
                                   ai_response["actions"])
                        st.rerun()
            
            # Show suggested actions
            if msg.get("actions"):
                st.markdown("**🎯 Suggested actions:**")
                for action in msg["actions"]:
                    st.write(f"• {action}")
    
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
        if st.button("📤 Send Message", use_container_width=True, 
                    disabled=not user_text.strip(), key="send_message_button"):
            add_message("human", user_text.strip())
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_text.strip())
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["actions"])
            
            st.rerun()
    
    with col2:
        if st.button("💡 Quick Help", use_container_width=True, key="quick_help_button"):
            add_message("human", "I need help understanding my options")
            ai_response = ai_assistant.generate_response("help")
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["actions"])
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
        # Conversation stats
        human_msgs = len([m for m in st.session_state.conversation_history if m["sender"] == "human"])
        ai_msgs = len([m for m in st.session_state.conversation_history if m["sender"] == "ai"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Messages", human_msgs)
        with col2:
            st.metric("AI Responses", ai_msgs)
        
        # Topics discussed
        st.markdown("**Topics discussed:**")
        topics = set()
        for msg in st.session_state.conversation_history:
            text = msg["text"].lower()
            if "privacy" in text:
                topics.add("🔒 Privacy")
            if any(word in text for word in ['bias', 'discrimination']):
                topics.add("⚖️ Discrimination")
            if "transparency" in text:
                topics.add("🔍 Transparency")
        
        for topic in topics:
            st.write(f"• {topic}")
    else:
        st.info("Start a conversation to see insights!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Resources
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 📚 Quick Resources")
    
    if st.button("📖 AI Human Rights Handbook", key="res_handbook"):
        st.success("Opening AI Human Rights Handbook...")
    
    if st.button("⚖️ Legal Complaint Template", key="res_legal"):
        st.success("Opening Legal Complaint Template...")
    
    if st.button("📊 Advocacy Strategy Guide", key="res_strategy"):
        st.success("Opening Advocacy Strategy Guide...")
    
    if st.button("🔍 Bias Detection Toolkit", key="res_bias"):
        st.success("Opening Bias Detection Toolkit...")

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
if st.checkbox("🔄 Enable auto-refresh", value=False, key="auto_refresh_checkbox"):
    time.sleep(5)
    st.rerun()
