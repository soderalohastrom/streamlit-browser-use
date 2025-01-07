# Streamlit Browser Use UI

A Streamlit-based user interface for [browser-use](https://github.com/gregpr07/browser-use), enabling easy interaction with AI-powered web automation.

## Features

- 🌐 Web-based UI for browser-use automation
- 🤖 Run pre-built examples or create custom tasks
- 👀 Live viewport preview of browser automation
- 📊 Real-time logging with step tracking
- ⚙️ Configurable browser settings
- 🎥 Automated GIF recording of browser actions

## Installation

```bash
# Clone the repository
git clone https://github.com/soderalohastrom/streamlit-browser-use.git
cd streamlit-browser-use

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the Streamlit app
streamlit run app.py
```

## Configuration

The app requires:
1. OpenAI API key for GPT-4 Vision
2. browser-use package installed
3. Optional: Playwright browsers installed

Add your OpenAI API key to your environment:
```bash
export OPENAI_API_KEY=your_key_here
```

## Examples

The app includes several pre-built examples:
- Amazon product search and sorting
- Google Docs letter writing
- Multi-tab search and navigation
- Parallel browser tasks
- Hugging Face model search

## Development

Built with:
- Streamlit
- browser-use
- LangChain
- OpenAI GPT-4V

## License

MIT License
