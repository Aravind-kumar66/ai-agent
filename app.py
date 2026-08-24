import streamlit as st
import time
from agent import AIAgent

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Futuristic CSS with Complete Dark Chat Input Fix
st.markdown("""
<style>
    /* Dark Theme Overall Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(9, 9, 11, 1) 90%);
        color: #ffffff;
    }
    
    /* Neon Title Glow */
    .neon-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 25px rgba(0, 242, 254, 0.4);
        margin-bottom: 0px;
    }
    
    /* Cyber Badges */
    .status-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #34d399;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 25px;
        letter-spacing: 0.5px;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(18, 24, 38, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00f2fe !important;
    }
    
    .tool-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        border-color: #00f2fe;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.2);
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        color: #ffffff !important;
    }

    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] div, 
    [data-testid="stChatMessage"] span {
        color: #ffffff !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* Darken Bottom Fixed Container */
    [data-testid="stBottom"], 
    [data-testid="stBottom"] > div {
        background-color: #090d16 !important;
    }

    /* Complete Dark Styling for Streamlit Chat Input */
    [data-testid="stChatInput"] {
        background-color: #0e131f !important;
        border-radius: 14px !important;
        padding: 4px !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #0e131f !important;
        border: 2px solid #00f2fe !important;
        border-radius: 12px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: transparent !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }

    /* Styled Action Button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar UI Panel
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("<div class='status-badge'>🟢 MODEL: GEMINI 2.5 FLASH</div>", unsafe_allow_html=True)
    
    st.markdown("### Active Capabilities")
    
    tools = [
        ("🧮 Calculator", "Evaluates mathematical expressions"),
        ("🌤️ Weather API", "Retrieves live forecast data"),
        ("🌐 Web Search", "Queries recent real-time information"),
        ("📚 Document RAG", "Searches local indexed embeddings")
    ]
    
    for title, desc in tools:
        st.markdown(f"""
        <div class="tool-card">
            <strong style="color: #00f2fe;">{title}</strong><br/>
            <span style="font-size: 0.82rem; color: #d1d5db;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("✨ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 4. App Header
st.markdown("<h1 class='neon-title'>🤖 GEMINI AI AGENT</h1>", unsafe_allow_html=True)
st.markdown("<div class='status-badge'>SYSTEM STATUS: OPERATIONAL</div>", unsafe_allow_html=True)

# 5. Session State Initialization
if "agent" not in st.session_state:
    st.session_state.agent = AIAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. User Input & Streaming Output Loop
if prompt := st.chat_input("Enter command or query..."):
    # Store user query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Process AI Agent execution
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("⚡ Executing query and retrieving context..."):
            try:
                raw_response = st.session_state.agent.run(prompt)
                
                # Simulate typewriter streaming effect
                full_response = ""
                for char in raw_response:
                    full_response += char
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.005)
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Execution Error: {e}")