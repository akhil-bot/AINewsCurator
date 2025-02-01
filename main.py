import streamlit as st
import json
import pyperclip
import os
from graphs.graph import create_graph, compile_workflow
from states.state import AgentGraphState

# Set page configuration
st.set_page_config(
    page_title="AI News Letter Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for API key
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = ''

# Initialize session state for API key
if 'tavily_api_key' not in st.session_state:
    st.session_state.tavily_api_key = ''

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Global Theme */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        background-color: #2d2d2d;
        border-right: 1px solid #3d3d3d;
        padding: 1rem 0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Header Styles */
    .app-header {
        background: linear-gradient(90deg, #2d2d2d 0%, #1a1a1a 100%);
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #3d3d3d;
        text-align: center;
    }
    
    .app-title {
        font-size: 2em;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.3rem;
    }
    
    .app-subtitle {
        color: #a0aec0;
        font-size: 1em;
    }
    
    /* Input Area */
    .stTextArea textarea {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #3d3d3d !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-size: 1em !important;
        min-height: 100px !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 0 1px #4a9eff !important;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #3d3d3d;
        margin-bottom: 1rem;
    }
    
    .sidebar-header h3 {
        margin: 0;
        font-size: 1.1em;
    }
    
    [data-testid="stSelectbox"] {
        margin-bottom: 0.8rem !important;
    }
    
    [data-testid="stSelectbox"] > div > div {
        background-color: #2d2d2d !important;
        border: 1px solid #3d3d3d !important;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #4a9eff 0%, #3d84ff 100%) !important;
        color: white !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        transition: all 0.3s ease !important;
        margin-top: 0.5rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 158, 255, 0.2) !important;
    }
    
    /* Output Section */
    .output-container {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    
    .output-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #3d3d3d;
    }
    
    .output-title {
        color: #ffffff;
        font-size: 1.1em;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Code Block */
    .code-block {
        font-family: 'JetBrains Mono', monospace;
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #3d3d3d;
        overflow-y: auto;
        max-height: 400px;
        line-height: 1.5;
        font-size: 0.95em;
        position: relative;
        margin-bottom: 0.5rem;
    }
    
    .code-block::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    .code-block::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    .code-block::-webkit-scrollbar-thumb {
        background: #4a4a4a;
        border-radius: 3px;
    }
    
    .code-block::-webkit-scrollbar-thumb:hover {
        background: #5a5a5a;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem 0;
        color: #a0aec0;
        font-size: 0.9em;
        border-top: 1px solid #3d3d3d;
        margin-top: 2rem;
    }
    
    /* Section Headers */
    h3 {
        font-size: 1.2em !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Toast Styling */
    .stToast {
        background-color: #2d2d2d !important;
        color: white !important;
        border: 1px solid #3d3d3d !important;
        padding: 0.8rem !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom CSS for disabled options */
    .coming-soon {
        color: #666;
        font-size: 0.8em;
        background: #3d3d3d;
        padding: 2px 6px;
        border-radius: 4px;
        margin-left: 6px;
    }
    
    .disabled-option {
        color: #666 !important;
        cursor: not-allowed;
    }
    </style>
""", unsafe_allow_html=True)

def copy_to_clipboard(text):
    """Helper function to copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        st.error(f"Failed to copy: {str(e)}")
        return False

def format_prompt_text(text):
    """Format the prompt text to have consistent spacing"""
    lines = text.strip().split('\n')
    formatted_lines = []
    prev_empty = False
    for line in lines:
        is_empty = not line.strip()
        if not (is_empty and prev_empty):
            formatted_lines.append(line)
        prev_empty = is_empty
    return '\n'.join(formatted_lines)

def set_openai_api_key(api_key: str):
    """Set OpenAI API key in both session state and environment variables."""
    st.session_state.openai_api_key = api_key
    os.environ['OPENAI_API_KEY'] = api_key

def set_tavily_api_key(api_key: str):
    """Set Tavily API key in both session state and environment variables."""
    st.session_state.tavily_api_key = api_key
    os.environ['TAVILY_API_KEY'] = api_key

def main():
    # Sidebar Configuration
    with st.sidebar:
        # st.markdown("## Configuration")
        
        
        st.markdown('<div class="sidebar-header"><h3>⚙️ Model Configuration</h3></div>', unsafe_allow_html=True)
        
        # Custom CSS for disabled options
        st.markdown("""
            <style>
            .coming-soon {
                color: #666;
                font-size: 0.8em;
                background: #3d3d3d;
                padding: 2px 6px;
                border-radius: 4px;
                margin-left: 6px;
            }
            
            .disabled-option {
                color: #666 !important;
                cursor: not-allowed;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Create provider options with Coming Soon tags
        provider_options = {
            "OpenAI": "openai",
            "Ollama (Coming Soon)": "ollama",
            "VLLM (Coming Soon)": "vllm",
            "Groq (Coming Soon)": "groq",
            "Claude (Coming Soon)": "claude",
            "Gemini (Coming Soon)": "gemini"
        }

       
        
        server = st.selectbox(
            "🤖 LLM Provider",
            options=list(provider_options.keys()),
            index=0,
            disabled=False,  # Main dropdown remains enabled
            help="Currently only OpenAI models are supported"
        )
        
        # Set actual server value based on selection
        server_value = provider_options[server]

        
        # Model selection based on provider
        if server == "OpenAI":
            model = st.selectbox(
                "📚 Model",
                ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
                index=0
            )
        else:
            # Disabled model selection for other providers
            st.selectbox(
                "📚 Model",
                ["Coming Soon"],
                disabled=True
            )
            model = None  # Set to None for non-OpenAI providers
        
        llm_api_key = st.text_input(
            "LLM Provider API Key",
            type="password",
            value=st.session_state.openai_api_key,
            help="Enter your Tavily API key here. It will be stored securely in the session state."
        )
        
        if llm_api_key:
            set_openai_api_key(llm_api_key)
            if not st.session_state.openai_api_key:
                st.error("Please enter a valid LLM Provider API key!")
        else:
            st.warning("Please enter your LLM Provider API key!")
        
        temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Higher values = more creative, lower = more focused",
            disabled=server != "OpenAI"  # Disable for non-OpenAI providers
        )

        if server != "OpenAI":
            st.warning("⚠️ Only OpenAI models are currently supported. Other providers coming soon!")
        
        tavily_api_key = st.text_input(
            "Tavily API Key",
            type="password",
            value=st.session_state.tavily_api_key,
            help="Enter your Tavily API key here. It will be stored securely in the session state."
        )
        
        if tavily_api_key:
            set_tavily_api_key(tavily_api_key)
            if not st.session_state.tavily_api_key:
                st.error("Please enter a valid Tavily API key!")
        else:
            st.warning("Please enter your Tavily API key!")

    # Main Content
    st.markdown("""
        <div class="app-header">
            <div class="app-title">🤖 AI News Letter Generator</div>
            <div class="app-subtitle">Generate AI/ML news letters using Tavily and OpenAI</div>
        </div>
    """, unsafe_allow_html=True)

    # Input Section
    st.markdown("### 📝 Query Description")
    query = st.text_area(
        "",
        placeholder="Example: Latest AI agents...",
        key="query_input"
    )

    # Initialize session state
    if 'generated_report' not in st.session_state:
        st.session_state.generated_report = None

    # Generate Button
    generate_disabled = server != "OpenAI"
    if st.button(
        "✨ Generate Report", 
        type="primary", 
        key="generate_report_btn"
    ):
        if query:
            with st.spinner("🔮 Generating your report..."):
                try:
                    state = AgentGraphState(query=query)
                    graph = create_graph(
                        server=server_value,
                        temperature=temperature,
                        model=model
                    )
                    app = compile_workflow(graph)
                    final_state = app.invoke(state)
                    
                    if "report" in final_state:
                        st.session_state.generated_report = final_state["report"]
                    
                except Exception as e:
                    st.error(f"⚠️ An error occurred: {str(e)}")
        else:
            st.warning("⚠️ Please enter a query description first.")

    # Display Output
    if st.session_state.generated_report:
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown('<div class="output-title">✨ Generated Prompt</div>', unsafe_allow_html=True)
        with col2:
            if st.button("📋 Copy", key="copy_btn", help="Copy to clipboard"):
                if copy_to_clipboard(st.session_state.generated_report):
                    st.toast("✅ Copied!")
        
        st.markdown(f'<div class="code-block">{st.session_state.generated_report}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            Made with ❤️ by a passionate AI Engineer
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

