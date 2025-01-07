import streamlit as st
import os
import sys
from pathlib import Path

# Add the browser-use package to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_openai import ChatOpenAI
from browser_use import Agent

# Set page config
st.set_page_config(
    page_title="Browser Use UI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        max-width: 100%;
    }
    .main {
        padding: 0;
    }
    .viewport-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        background-color: white;
    }
    .log-container {
        font-family: monospace;
        font-size: 14px;
        background-color: #1e1e1e;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        height: 300px;
        overflow-y: auto;
    }
    .status-container {
        border-left: 3px solid #31c48d;
        padding-left: 10px;
        margin: 5px 0;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

def create_output_container():
    """Create a container for real-time output"""
    if 'output' not in st.session_state:
        st.session_state.output = []
    
    output_container = st.empty()
    status_container = st.empty()
    return output_container, status_container

def update_output(message, output_container):
    """Update the output container with new messages"""
    st.session_state.output.append(message)
    output_container.markdown(
        '<div class="output-container">' + 
        '<br>'.join(st.session_state.output) + 
        '</div>',
        unsafe_allow_html=True
    )

# Featured examples that best demonstrate Browser Use capabilities
FEATURED_EXAMPLES = {
    "Amazon Search": {
        "file": "amazon_search.py",
        "description": "Search and sort products on Amazon",
        "task": "Go to amazon.com, search for laptop, sort by best rating, and give me the price of the first result"
    },
    "Google Docs Letter": {
        "file": "real_browser.py",
        "description": "Write and save a document in Google Docs",
        "task": "In docs.google.com write my Papa a quick thank you for everything letter and save the document as pdf"
    },
    "Multi-Tab Search": {
        "file": "multi-tab_handling.py",
        "description": "Handle multiple browser tabs",
        "task": "open 3 tabs with elon musk, trump, and steve jobs, then go back to the first and stop"
    },
    "Parallel Tasks": {
        "file": "parallel_agents.py",
        "description": "Run multiple browser tasks in parallel",
        "task": "Search Google for weather in Tokyo, Check Reddit front page title, Look up Bitcoin price on Coinbase, Find NASA image of the day"
    },
    "Hugging Face Search": {
        "file": "save_to_file_hugging_face.py",
        "description": "Search and save ML models from Hugging Face",
        "task": "Look up models with a license of cc-by-sa-4.0 and sort by most likes on Hugging face, save top 5 to file"
    }
}

def load_examples():
    """Load selected examples that best demonstrate Browser Use capabilities"""
    examples = {}
    for name, info in FEATURED_EXAMPLES.items():
        examples[name] = info["task"]
    return examples

def main():
    # Create two columns for layout
    col1, col2 = st.columns([1, 3])
    
    # Sidebar (col1)
    with col1:
        st.title("Browser Use UI")
        st.markdown("""
        Browser Use enables AI agents to interact with web browsers, automating tasks like:
        - Web navigation and search
        - Form filling and submission
        - Multi-tab operations
        - Content extraction
        - Document creation
        - Parallel browsing tasks
        """)
        st.markdown("---")
        
        # Examples section
        st.subheader("Featured Examples")
        examples = load_examples()
        
        for name, task in examples.items():
            with st.expander(name):
                # Get description from featured_examples
                description = FEATURED_EXAMPLES[name]["description"]
                st.markdown(f"**{description}**")
                st.markdown("---")
                st.markdown("**Task:**")
                st.write(task)
                if st.button("Run", key=f"run_{name}"):
                    st.session_state.current_task = task
        
        # Custom task section
        st.markdown("---")
        st.subheader("Custom Task")
        custom_task = st.text_area("Enter your task:")
        if st.button("Run Custom Task"):
            st.session_state.current_task = custom_task

    # Main content area (col2)
    with col2:
        if "current_task" in st.session_state and st.session_state.current_task:
            st.subheader("Current Task")
            st.write(st.session_state.current_task)
            
            # Create containers for viewport, logs, and status
            viewport_container = st.empty()
            with st.expander("Logs", expanded=True):
                log_container = st.empty()
            status_container = st.empty()
            
            # Browser settings
            st.markdown("### Settings")
            
            # Browser viewport and mode
            st.markdown("**Browser Settings**")
            col_w, col_h, col_mode = st.columns(3)
            with col_w:
                viewport_width = st.number_input("Viewport Width", min_value=400, max_value=1920, value=1280)
            with col_h:
                viewport_height = st.number_input("Viewport Height", min_value=300, max_value=1080, value=720)
            with col_mode:
                headless = st.checkbox("Headless Mode", value=False, help="Run browser in background without UI")
            
            # Agent settings
            st.markdown("**Agent Settings**")
            col_steps, col_clear = st.columns(2)
            with col_steps:
                max_steps = st.number_input("Max Steps", min_value=5, max_value=50, value=25, 
                                          help="Maximum number of steps the agent can take")
            with col_clear:
                if st.button("Clear History") and Path("agent_history.gif").exists():
                    Path("agent_history.gif").unlink()
                    st.experimental_rerun()
            
            # Example source code
            if "current_task" in st.session_state:
                for name, info in FEATURED_EXAMPLES.items():
                    if info["task"] == st.session_state.current_task:
                        st.markdown("**Example Source Code**")
                        with st.expander("View Source", expanded=False):
                            with open(f"examples/{info['file']}", "r") as f:
                                st.code(f.read(), language="python")
                        break
            
            # Initialize agent with browser config
            from browser_use.browser.browser import Browser, BrowserConfig
            from browser_use.browser.context import BrowserContextConfig
            
            browser = Browser(
                config=BrowserConfig(
                    headless=headless,
                    new_context_config=BrowserContextConfig(
                        browser_window_size={
                            'width': viewport_width,
                            'height': viewport_height,
                        },
                        no_viewport=False,  # Ensure viewport is enabled
                    ),
                )
            )
            
            llm = ChatOpenAI(model='gpt-4o')
            agent = Agent(
                task=st.session_state.current_task,
                llm=llm,
                browser=browser,
            )
            
            async def run_task():
                try:
                    import logging
                    
                    # Clear previous output
                    st.session_state.output = []
                    
                    # Create a custom logging handler
                    class StreamlitHandler(logging.Handler):
                        def emit(self, record):
                            msg = self.format(record)
                            st.session_state.output.append(msg)
                            log_container.markdown(
                                '<div class="log-container">' + 
                                '<br>'.join(st.session_state.output[-100:]) + # Keep last 100 lines
                                '</div>',
                                unsafe_allow_html=True
                            )
                    
                    # Configure logging
                    logger = logging.getLogger('browser_use')
                    handler = StreamlitHandler()
                    formatter = logging.Formatter('%(levelname)s: %(message)s')
                    handler.setFormatter(formatter)
                    logger.addHandler(handler)
                    
                    # Update status with progress
                    def update_status(step=0):
                        status_container.markdown(
                            f'<div class="status-container">'
                            f'Task is running... (Step {step}/{max_steps})'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    
                    update_status(0)
                    
                    # Set up step tracking through logging
                    current_step = 0
                    def step_tracker(record):
                        nonlocal current_step
                        if "Step" in record.msg:
                            current_step += 1
                            update_status(current_step)
                    
                    # Add step tracking to handler
                    handler.emit = lambda record: (
                        step_tracker(record),
                        StreamlitHandler.emit(handler, record)
                    )
                    
                    # Run the agent
                    await agent.run(max_steps=max_steps)
                    
                    # Update status
                    status_container.markdown(
                        '<div class="status-container">Task completed successfully!</div>',
                        unsafe_allow_html=True
                    )
                    
                    # Display the generated GIF if it exists
                    if Path("agent_history.gif").exists():
                        import base64
                        gif_path = Path("agent_history.gif")
                        with open(gif_path, "rb") as f:
                            gif_data = base64.b64encode(f.read()).decode()
                        
                        viewport_container.markdown(
                            f'<div class="viewport-container" style="height: {viewport_height}px;">' +
                            f'<img src="data:image/gif;base64,{gif_data}" ' +
                            f'style="width: {viewport_width}px; height: {viewport_height}px; object-fit: contain;">' +
                            '</div>',
                            unsafe_allow_html=True
                        )
                    
                    # Remove the custom handler but don't close browser
                    logger.removeHandler(handler)
                        
                except Exception as e:
                    status_container.markdown(
                        f'<div class="status-container" style="border-left-color: #ff4b4b">Error: {str(e)}</div>',
                        unsafe_allow_html=True
                    )
                    pass
            
            # Run the agent
            if st.button("Start Task"):
                import asyncio
                asyncio.run(run_task())

if __name__ == "__main__":
    main()
