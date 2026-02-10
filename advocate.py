import streamlit as st
import pandas as pd
import datetime
import random
import time
import json
import base64
from typing import List, Dict, Optional
import speech_recognition as sr
import pyttsx3
import threading
import queue

# Note: For voice features, you'll need to install:
# pip install SpeechRecognition pyttsx3 pyaudio

# Initialize session state for conversation
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'ai_voice' not in st.session_state:
    st.session_state.ai_voice = None
if 'advocacy_cases' not in st.session_state:
    st.session_state.advocacy_cases = []

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
        border-radius: 10px;
        margin: 20px 0;
    }
    
    .message-human {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        padding: 15px;
        border-radius: 18px 18px 0 18px;
        margin: 10px 0 10px auto;
        max-width: 70%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .message-human:before {
        content: "👤";
        position: absolute;
        left: -35px;
        top: 10px;
        font-size: 1.2rem;
    }
    
    .message-ai {
        background: linear-gradient(135deg, #0d9d58, #0a8043);
        color: white;
        padding: 15px;
        border-radius: 18px 18px 18px 0;
        margin: 10px auto 10px 0;
        max-width: 70%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
    }
    
    .message-ai:before {
        content: "🤖";
        position: absolute;
        right: -35px;
        top: 10px;
        font-size: 1.2rem;
    }
    
    .message-time {
        font-size: 0.8rem;
        opacity: 0.8;
        text-align: right;
        margin-top: 5px;
    }
    
    /* Voice controls */
    .voice-controls {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .listening-indicator {
        animation: pulse 1.5s infinite;
        background: #ff3b30;
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        display: inline-flex;
        align-items: center;
        gap: 10px;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .voice-btn {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s;
    }
    
    .voice-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    
    .voice-btn:active {
        transform: translateY(0);
    }
    
    /* Conversation topics */
    .topic-bubble {
        display: inline-block;
        background: #e3f2fd;
        color: #1a73e8;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .topic-bubble:hover {
        background: #1a73e8;
        color: white;
        border-color: #1a73e8;
        transform: scale(1.05);
    }
    
    /* Main containers */
    .main-container {
        background: white;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white !important;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Text-to-Speech engine
def init_tts():
    try:
        engine = pyttsx3.init()
        # Set properties
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level
        # Get available voices
        voices = engine.getProperty('voices')
        # Set voice (try to get a natural sounding voice)
        for voice in voices:
            if 'english' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        return engine
    except Exception as e:
        st.warning(f"Text-to-Speech initialization failed: {e}")
        return None

# Initialize Speech Recognition
def init_speech_recognition():
    try:
        return sr.Recognizer()
    except Exception as e:
        st.warning(f"Speech recognition initialization failed: {e}")
        return None

# AI Response Generator
class AIAdvocateAssistant:
    def __init__(self):
        self.name = "Alex"
        self.role = "Human AI Advocate"
        self.knowledge_base = self.load_knowledge_base()
        
    def load_knowledge_base(self):
        return {
            "greetings": [
                "Hello! I'm your Human AI Advocate. How can I assist you today in protecting human dignity in the age of AI?",
                "Welcome! I'm here to help you navigate AI ethics and human rights concerns. What's on your mind?",
                "Hi there! As your AI advocate, I'm ready to discuss how we can ensure AI respects human rights."
            ],
            "human_rights": {
                "privacy": "The right to privacy in AI includes data protection, informed consent, and control over personal information. AI systems must respect boundaries and provide transparency about data usage.",
                "non_discrimination": "AI must not discriminate based on protected characteristics. This requires bias testing, diverse training data, and regular audits to ensure fairness.",
                "transparency": "Humans have the right to understand AI decisions affecting them. This means explainable AI, clear documentation, and accessible information about how systems work.",
                "accountability": "When AI causes harm, there must be clear accountability. This includes human oversight, grievance mechanisms, and legal recourse options.",
                "autonomy": "AI should enhance, not replace, human decision-making. People must retain meaningful control over decisions affecting their lives."
            },
            "advocacy_strategies": {
                "legal": ["File human rights complaints", "Initiate class action lawsuits", "Lobby for legislation", "Engage with regulatory bodies"],
                "technical": ["Demand algorithmic audits", "Request source code reviews", "Propose ethical design frameworks", "Develop oversight mechanisms"],
                "community": ["Organize awareness campaigns", "Build coalitions with affected groups", "Create educational resources", "Host public forums"],
                "corporate": ["Demand transparency reports", "Request impact assessments", "Propose ethics committees", "Advocate for user consent"]
            },
            "case_examples": [
                "A facial recognition system used without consent violates privacy rights. We can demand its removal and require public consultation.",
                "An automated hiring tool that discriminates against women requires immediate suspension, bias remediation, and compensation for affected individuals.",
                "Healthcare AI making diagnostic errors without human review violates the right to health. We need oversight and accountability measures.",
                "Social media algorithms promoting harmful content to minors violates child protection rights. We can demand age-appropriate safeguards."
            ]
        }
    
    def generate_response(self, user_input: str, context: List[Dict] = None) -> Dict:
        """Generate AI response based on user input"""
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        # Analyze user input
        user_input_lower = user_input.lower()
        
        # Check for greetings
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            response = random.choice(self.knowledge_base["greetings"])
            
        # Check for human rights topics
        elif 'privacy' in user_input_lower:
            response = self.knowledge_base["human_rights"]["privacy"]
            
        elif any(word in user_input_lower for word in ['discrimination', 'bias', 'fair', 'unfair']):
            response = self.knowledge_base["human_rights"]["non_discrimination"]
            
        elif any(word in user_input_lower for word in ['transparent', 'explain', 'understand', 'black box']):
            response = self.knowledge_base["human_rights"]["transparency"]
            
        elif any(word in user_input_lower for word in ['accountable', 'responsible', 'liable', 'blame']):
            response = self.knowledge_base["human_rights"]["accountability"]
            
        # Check for help requests
        elif any(word in user_input_lower for word in ['help', 'assist', 'support', 'what can']):
            response = "I can help you with: 1) Understanding AI human rights violations 2) Developing advocacy strategies 3) Documenting cases 4) Connecting with resources 5) Taking legal/policy action. What specific help do you need?"
            
        # Check for case reports
        elif any(word in user_input_lower for word in ['report', 'violation', 'issue', 'problem', 'complaint']):
            response = "I can help you report an AI human rights violation. Please provide details about: 1) What AI system is involved 2) Which human right is affected 3) Who is being harmed 4) What evidence you have 5) What outcome you're seeking."
            
        # Check for strategy requests
        elif any(word in user_input_lower for word in ['strategy', 'plan', 'action', 'what should']):
            response = "Based on your situation, I recommend: 1) Document all evidence 2) Identify affected stakeholders 3) Choose appropriate advocacy channels (legal, media, policy) 4) Build coalitions 5) Set clear demands 6) Monitor impact. Would you like me to elaborate on any specific strategy?"
            
        # Default response
        else:
            response = "I understand you're concerned about AI and human rights. Could you tell me more about your specific situation? I can help with advocacy strategies, legal options, or connecting you with relevant resources."
        
        # Add follow-up questions
        follow_up = self._generate_follow_up(user_input_lower)
        
        return {
            "text": response,
            "follow_up": follow_up,
            "time": current_time,
            "suggested_actions": self._get_suggested_actions(user_input_lower),
            "resources": self._get_relevant_resources(user_input_lower)
        }
    
    def _generate_follow_up(self, user_input: str) -> List[str]:
        """Generate follow-up questions based on user input"""
        follow_ups = []
        
        if 'privacy' in user_input:
            follow_ups = [
                "Would you like to know about data protection regulations?",
                "Should we discuss consent mechanisms for AI systems?",
                "Are you interested in privacy-preserving AI techniques?"
            ]
        elif any(word in user_input for word in ['discrimination', 'bias']):
            follow_ups = [
                "Would you like guidance on conducting bias audits?",
                "Should we discuss diversity in AI development teams?",
                "Are you interested in fairness metrics and evaluation?"
            ]
        elif 'help' in user_input:
            follow_ups = [
                "What specific human right is being affected?",
                "Can you tell me more about the AI system involved?",
                "Who are the affected individuals or groups?"
            ]
        
        return follow_ups
    
    def _get_suggested_actions(self, user_input: str) -> List[str]:
        """Get suggested actions based on user input"""
        actions = []
        
        if any(word in user_input for word in ['report', 'violation']):
            actions = [
                "Document the incident with timestamps",
                "Gather evidence (screenshots, data)",
                "Identify affected individuals",
                "Consult legal resources",
                "Contact relevant authorities"
            ]
        elif any(word in user_input for word in ['strategy', 'plan']):
            actions = [
                "Assess the severity of the violation",
                "Identify key stakeholders",
                "Choose advocacy channels",
                "Set realistic goals",
                "Develop timeline"
            ]
        
        return actions
    
    def _get_relevant_resources(self, user_input: str) -> List[str]:
        """Get relevant resources based on user input"""
        resources = []
        
        if 'privacy' in user_input:
            resources = ["GDPR guidelines", "CCPA regulations", "Privacy by Design framework"]
        elif any(word in user_input for word in ['discrimination', 'bias']):
            resources = ["Algorithmic fairness toolkit", "Bias assessment framework", "Diversity in AI guidelines"]
        
        return resources

# Initialize AI Assistant
ai_assistant = AIAdvocateAssistant()

# Initialize TTS engine
if st.session_state.ai_voice is None:
    st.session_state.ai_voice = init_tts()

# Voice Processing Functions
def start_listening():
    """Start voice recognition"""
    st.session_state.is_listening = True
    st.rerun()

def stop_listening():
    """Stop voice recognition"""
    st.session_state.is_listening = False
    st.rerun()

def process_voice_input():
    """Process voice input using speech recognition"""
    if not st.session_state.is_listening:
        return None
    
    recognizer = init_speech_recognition()
    if not recognizer:
        return "Voice recognition not available"
    
    try:
        with sr.Microphone() as source:
            st.info("Listening... Please speak now")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            return text
    except sr.WaitTimeoutError:
        return "No speech detected"
    except sr.UnknownValueError:
        return "Could not understand audio"
    except Exception as e:
        return f"Error: {str(e)}"

def speak_text(text: str):
    """Convert text to speech"""
    if st.session_state.ai_voice and st.session_state.voice_enabled:
        try:
            engine = st.session_state.ai_voice
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.error(f"Speech synthesis failed: {e}")

# Add message to conversation
def add_message(sender: str, text: str, follow_up: List[str] = None, 
                actions: List[str] = None, resources: List[str] = None):
    """Add a message to the conversation history"""
    message = {
        "sender": sender,
        "text": text,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "follow_up": follow_up or [],
        "suggested_actions": actions or [],
        "resources": resources or []
    }
    
    st.session_state.conversation_history.append(message)
    
    # If AI is speaking and voice is enabled, speak the response
    if sender == "ai" and st.session_state.voice_enabled:
        # Run speech in separate thread to avoid blocking
        threading.Thread(target=speak_text, args=(text,)).start()

# Sidebar
with st.sidebar:
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("## 🤖💬 AI Advocate Assistant")
    st.markdown("Voice-enabled conversation for human rights advocacy")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Voice Controls
    st.markdown("### 🎤 Voice Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        voice_on = st.toggle("Enable Voice", value=st.session_state.voice_enabled)
        if voice_on != st.session_state.voice_enabled:
            st.session_state.voice_enabled = voice_on
            if voice_on and st.session_state.ai_voice is None:
                st.session_state.ai_voice = init_tts()
    
    with col2:
        if st.button("🔊 Test Voice", use_container_width=True):
            if st.session_state.voice_enabled:
                test_text = "Hello! I am your Human AI Advocate assistant."
                speak_text(test_text)
                st.success("Voice test complete!")
            else:
                st.warning("Enable voice first")
    
    st.markdown("---")
    
    # Conversation Topics
    st.markdown("### 💡 Quick Topics")
    
    topics = [
        "AI Privacy Violation",
        "Algorithmic Discrimination", 
        "Transparency Issues",
        "Accountability Concerns",
        "Report a Case",
        "Advocacy Strategies"
    ]
    
    for topic in topics:
        if st.button(f"💬 {topic}", use_container_width=True, key=f"topic_{topic}"):
            user_msg = f"I want to discuss {topic.lower()}"
            add_message("human", user_msg)
            
            # Generate AI response
            ai_response = ai_assistant.generate_response(user_msg)
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"],
                       ai_response["resources"])
            
            st.rerun()
    
    st.markdown("---")
    
    # Conversation Management
    st.markdown("### ⚙️ Conversation")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.conversation_history = []
        st.rerun()
    
    if st.button("💾 Save Conversation", use_container_width=True):
        if st.session_state.conversation_history:
            # Save conversation to JSON
            filename = f"ai_advocate_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(st.session_state.conversation_history, f, indent=2)
            st.success(f"Conversation saved as {filename}")

# Main Content
st.markdown("""
<div class="highlight-box">
    <h1 style="text-align: center; color: white !important;">🤖💬 Human AI Advocate Assistant</h1>
    <p style="text-align: center; color: white !important; font-size: 1.2rem;">
        Voice-enabled conversation for protecting human dignity in AI systems
    </p>
</div>
""", unsafe_allow_html=True)

# Two main columns
col_main1, col_main2 = st.columns([2, 1])

with col_main1:
    # Conversation Interface
    st.markdown("## 💬 Live Conversation")
    
    # Voice Controls
    st.markdown('<div class="voice-controls">', unsafe_allow_html=True)
    
    voice_col1, voice_col2, voice_col3 = st.columns([1, 1, 2])
    
    with voice_col1:
        if st.button("🎤 Start Listening", use_container_width=True, 
                    type="primary" if not st.session_state.is_listening else "secondary"):
            start_listening()
    
    with voice_col2:
        if st.button("⏹️ Stop Listening", use_container_width=True,
                    type="primary" if st.session_state.is_listening else "secondary"):
            stop_listening()
    
    with voice_col3:
        if st.session_state.is_listening:
            st.markdown('<div class="listening-indicator">🔴 Listening... Speak now</div>', unsafe_allow_html=True)
            
            # Process voice input
            voice_text = process_voice_input()
            if voice_text and "Error" not in voice_text and "No speech" not in voice_text:
                add_message("human", voice_text)
                
                # Generate AI response
                ai_response = ai_assistant.generate_response(voice_text)
                add_message("ai", ai_response["text"], 
                           ai_response["follow_up"],
                           ai_response["suggested_actions"],
                           ai_response["resources"])
                
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation Display
    st.markdown('<div class="conversation-container">', unsafe_allow_html=True)
    
    if not st.session_state.conversation_history:
        # Initial greeting
        initial_greeting = ai_assistant.generate_response("hello")
        add_message("ai", initial_greeting["text"], 
                   initial_greeting["follow_up"],
                   initial_greeting["suggested_actions"],
                   initial_greeting["resources"])
    
    # Display conversation
    for message in st.session_state.conversation_history:
        if message["sender"] == "human":
            st.markdown(f'''
            <div class="message-human">
                {message["text"]}
                <div class="message-time">{message["time"]}</div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="message-ai">
                {message["text"]}
                <div class="message-time">{message["time"]}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Show follow-up questions if any
            if message.get("follow_up"):
                st.markdown("**Follow-up questions:**")
                for question in message["follow_up"]:
                    if st.button(f"💭 {question}", key=f"follow_{hash(question)}"):
                        add_message("human", question)
                        ai_response = ai_assistant.generate_response(question)
                        add_message("ai", ai_response["text"], 
                                   ai_response["follow_up"],
                                   ai_response["suggested_actions"],
                                   ai_response["resources"])
                        st.rerun()
            
            # Show suggested actions if any
            if message.get("suggested_actions"):
                st.markdown("**Suggested actions:**")
                for action in message["suggested_actions"]:
                    st.write(f"• {action}")
            
            # Show resources if any
            if message.get("resources"):
                st.markdown("**Resources:**")
                for resource in message["resources"]:
                    st.write(f"📚 {resource}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Text Input for typing
    st.markdown("### 📝 Type Your Message")
    
    text_col1, text_col2 = st.columns([4, 1])
    
    with text_col1:
        user_text = st.text_input("Type your message here:", 
                                 placeholder="Ask about AI human rights, advocacy strategies, or report issues...",
                                 label_visibility="collapsed")
    
    with text_col2:
        if st.button("Send", use_container_width=True):
            if user_text.strip():
                add_message("human", user_text.strip())
                
                # Generate AI response
                ai_response = ai_assistant.generate_response(user_text.strip())
                add_message("ai", ai_response["text"], 
                           ai_response["follow_up"],
                           ai_response["suggested_actions"],
                           ai_response["resources"])
                
                st.rerun()

with col_main2:
    # AI Advocate Profile
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🤖 Your AI Advocate")
    
    st.markdown("""
    **Name:** Alex  
    **Role:** Human AI Advocate  
    **Specialization:** AI Ethics & Human Rights  
    **Experience:** 5+ years in advocacy  
    
    ### Capabilities:
    ✅ Voice conversation  
    ✅ Text-based chat  
    ✅ Human rights guidance  
    ✅ Advocacy strategy  
    ✅ Case documentation  
    ✅ Legal/policy advice  
    """)
    
    # Stats
    st.markdown("### 📊 Conversation Stats")
    st.metric("Messages", len(st.session_state.conversation_history))
    st.metric("Topics Discussed", len(set([msg["text"] for msg in st.session_state.conversation_history])))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## ⚡ Quick Actions")
    
    if st.button("📋 Start New Case", use_container_width=True):
        add_message("human", "I want to start documenting a new AI human rights case")
        ai_response = ai_assistant.generate_response("start new case")
        add_message("ai", ai_response["text"], 
                   ai_response["follow_up"],
                   ai_response["suggested_actions"],
                   ai_response["resources"])
        st.rerun()
    
    if st.button("⚖️ Legal Advice", use_container_width=True):
        add_message("human", "I need legal advice for an AI human rights violation")
        ai_response = ai_assistant.generate_response("legal advice")
        add_message("ai", ai_response["text"], 
                   ai_response["follow_up"],
                   ai_response["suggested_actions"],
                   ai_response["resources"])
        st.rerun()
    
    if st.button("📢 Advocacy Strategy", use_container_width=True):
        add_message("human", "Help me develop an advocacy strategy")
        ai_response = ai_assistant.generate_response("advocacy strategy")
        add_message("ai", ai_response["text"], 
                   ai_response["follow_up"],
                   ai_response["suggested_actions"],
                   ai_response["resources"])
        st.rerun()
    
    if st.button("🔗 Connect Resources", use_container_width=True):
        add_message("human", "Connect me with human rights resources")
        ai_response = ai_assistant.generate_response("resources")
        add_message("ai", ai_response["text"], 
                   ai_response["follow_up"],
                   ai_response["suggested_actions"],
                   ai_response["resources"])
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation Topics Quick Select
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("## 🎯 Common Topics")
    
    common_topics = [
        "AI privacy concerns",
        "Algorithmic bias",
        "Transparency issues", 
        "Accountability",
        "Consent in AI",
        "Data protection",
        "Fairness metrics",
        "Human oversight"
    ]
    
    for topic in common_topics:
        if st.button(f"💬 {topic}", key=f"quick_{topic}", use_container_width=True):
            add_message("human", f"Discuss {topic}")
            ai_response = ai_assistant.generate_response(topic)
            add_message("ai", ai_response["text"], 
                       ai_response["follow_up"],
                       ai_response["suggested_actions"],
                       ai_response["resources"])
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown('<div style="height: 2px; background: linear-gradient(to right, #1a73e8, transparent); margin: 30px 0;"></div>', unsafe_allow_html=True)

# Additional Features Section
st.markdown("## 🔧 Advanced Features")

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### 🎙️ Voice Settings")
    
    # Voice speed
    if st.session_state.voice_enabled:
        voice_speed = st.slider("Voice Speed", 100, 300, 150, 10)
        if st.session_state.ai_voice:
            st.session_state.ai_voice.setProperty('rate', voice_speed)
        
        # Voice volume
        voice_volume = st.slider("Voice Volume", 0.0, 1.0, 0.9, 0.1)
        if st.session_state.ai_voice:
            st.session_state.ai_voice.setProperty('volume', voice_volume)
    
    st.markdown('</div>', unsafe_allow_html=True)

with feat_col2:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### 💾 Export Options")
    
    if st.button("Export as Text", use_container_width=True):
        if st.session_state.conversation_history:
            text_content = "Human AI Advocate Conversation\n" + "="*40 + "\n\n"
            for msg in st.session_state.conversation_history:
                text_content += f"{msg['sender'].upper()} ({msg['time']}):\n{msg['text']}\n\n"
            
            # Create download button
            b64 = base64.b64encode(text_content.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="ai_advocate_conversation.txt">Download Text File</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    if st.button("Export as JSON", use_container_width=True):
        if st.session_state.conversation_history:
            json_content = json.dumps(st.session_state.conversation_history, indent=2)
            b64 = base64.b64encode(json_content.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="ai_advocate_conversation.json">Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with feat_col3:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    
    # Auto-play voice
    auto_voice = st.toggle("Auto-play AI responses", value=True)
    
    # Conversation style
    style = st.selectbox("Conversation Style", 
                        ["Professional", "Supportive", "Direct", "Detailed"])
    
    # Clear on start
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.conversation_history = []
        st.session_state.is_listening = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 10px; margin-top: 30px;">
    <h3 style="color: #1a73e8 !important;">🤖💬 Human AI Advocate Assistant</h3>
    <p><strong>Voice-enabled conversation for human rights protection in AI systems</strong></p>
    
    <div style="margin: 20px 0; display: flex; justify-content: center; gap: 20px;">
        <div>🎤 <strong>Voice Input</strong></div>
        <div>🔊 <strong>Voice Output</strong></div>
        <div>💬 <strong>Text Chat</strong></div>
        <div>⚖️ <strong>Legal Guidance</strong></div>
    </div>
    
    <div style="border-top: 1px solid #ddd; padding-top: 20px; margin-top: 20px;">
        <p style="color: #666; font-size: 0.9rem;">
            Built for ethical AI advocacy • Supports multiple languages • Privacy-focused • {timestamp}
        </p>
    </div>
</div>
""".format(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

# Real-time updates for conversation
if st.checkbox("🔄 Enable real-time conversation updates", value=True):
    time.sleep(2)
    st.rerun()
