import streamlit as st
import time
from agent import AIAgent

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Gemini AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CLEAN WHITE UI
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #ffffff !important;
        color: #111827 !important;
    }

    .main {
        background: #ffffff !important;
    }

    .block-container {
        background: #ffffff !important;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* Remove unnecessary top/header dark background */
    [data-testid="stHeader"] {
        background: #ffffff !important;
    }

    /* ========================================================
       MAIN TITLE
       ======================================================== */

    .neon-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 4px;
        letter-spacing: -1px;
    }

    .subtitle {
        color: #6b7280 !important;
        font-size: 1rem;
        margin-bottom: 20px;
    }

    /* ========================================================
       STATUS BADGE
       ======================================================== */

    .status-badge {
        display: inline-block;
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #047857 !important;
        padding: 5px 13px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 22px;
        letter-spacing: 0.4px;
    }

    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e5e7eb !important;
    }

    [data-testid="stSidebar"] * {
        color: #111827 !important;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }

    /* ========================================================
       TOOL CARDS
       ======================================================== */

    .tool-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 13px 16px;
        margin-bottom: 10px;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .tool-card:hover {
        border-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.10);
    }

    .tool-title {
        color: #2563eb !important;
        font-weight: 700;
    }

    .tool-description {
        color: #6b7280 !important;
        font-size: 0.82rem;
    }

    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    [data-testid="stChatMessage"] {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 16px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span {
        color: #111827 !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stBottom"] {
        background: #ffffff !important;
        border-top: 1px solid #e5e7eb !important;
    }

    [data-testid="stBottom"] > div {
        background: #ffffff !important;
    }

    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border-radius: 14px !important;
        padding: 4px !important;
    }

    [data-testid="stChatInput"] > div {
        background: #ffffff !important;
        border: 2px solid #d1d5db !important;
        border-radius: 12px !important;
        transition: all 0.2s ease;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.10);
    }

    [data-testid="stChatInput"] textarea {
        color: #111827 !important;
        background: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.20);
    }

    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #e5e7eb !important;
    }

    /* ========================================================
       CODE BLOCKS
       ======================================================== */

    pre {
        background: #f8fafc !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 10px !important;
    }

    code {
        color: #111827 !important;
    }

    /* ========================================================
       ALERTS / STATUS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 12px !important;
    }

    /* ========================================================
       SPINNER
       ======================================================== */

    [data-testid="stSpinner"] {
        color: #2563eb !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. SIDEBAR UI PANEL
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Control Panel")

    st.markdown(
        "<div class='status-badge'>🟢 MODEL: GEMINI 2.5 FLASH</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Active Capabilities")

    tools = [
        ("🧮 Calculator", "Evaluates mathematical expressions"),
        ("🌤️ Weather API", "Retrieves live forecast data"),
        ("🌐 Web Search", "Queries recent real-time information"),
        ("📚 Document RAG", "Searches local indexed embeddings")
    ]

    for title, desc in tools:

        st.markdown(
            f"""
            <div class="tool-card">
                <div class="tool-title">{title}</div>
                <div class="tool-description">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    if st.button("✨ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# 4. APP HEADER
# ============================================================

st.markdown(
    "<h1 class='neon-title'>🤖 GEMINI AI AGENT</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Your intelligent AI assistant with tools, web search, weather, calculator and document RAG.</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='status-badge'>🟢 SYSTEM STATUS: OPERATIONAL</div>",
    unsafe_allow_html=True
)


# ============================================================
# 5. SESSION STATE INITIALIZATION
# ============================================================

if "agent" not in st.session_state:
    st.session_state.agent = AIAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 6. RENDER CHAT HISTORY
# ============================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ============================================================
# 7. USER INPUT & AI RESPONSE
# ============================================================

if prompt := st.chat_input("Enter command or query..."):

    # --------------------------------------------------------
    # Store user query
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    # --------------------------------------------------------
    # Process AI Agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        with st.spinner("⚡ Executing query and retrieving context..."):

            try:

                raw_response = st.session_state.agent.run(prompt)

                # ------------------------------------------------
                # Typewriter streaming effect
                # ------------------------------------------------

                full_response = ""

                for char in raw_response:

                    full_response += char

                    message_placeholder.markdown(
                        full_response + "▌"
                    )

                    time.sleep(0.005)

                message_placeholder.markdown(full_response)

                # ------------------------------------------------
                # Store assistant response
                # ------------------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": full_response
                    }
                )

            except Exception as e:

                st.error(
                    f"Execution Error: {e}"
                )