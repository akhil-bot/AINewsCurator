# AINewsCurator

Want to create a high-quality newsletter on any topic effortlessly? The **AI NewsCurator Agent** does it for you! This smart, multi-agent tool browses the web, gathers the latest information, summarizes key insights, and compiles a polished newsletter—so you don't have to.  

### How It Works:  
📰 **Newsletter Agent** – Searches the internet for the most relevant articles.  
✍️ **Summarizer Agent** – Extracts key points and creates easy-to-read summaries.  
📢 **Publisher Agent** – Compiles everything into a well-structured newsletter.  

Perfect for content creators, researchers, and businesses looking to stay informed without the hassle. Just input a topic, and let AI do the rest! 🎯

### ✨ Key Features

- 🔍 **Smart Search**: Utilizes Tavily API to find the most relevant and recent AI/ML news articles
- 🤖 **Intelligent Summarization**: Leverages OpenAI's advanced language models to create concise, readable summaries
- 📝 **Professional Formatting**: Automatically formats content into a well-structured newsletter
- 🎨 **Modern UI**: Clean, intuitive interface built with Streamlit
- 🔄 **Multiple LLM Support**: Designed to support various language models (OpenAI, Ollama, VLLM, Groq, Claude, Gemini)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Tavily API key ([Get it here](https://tavily.com))
- OpenAI API key ([Get it here](https://platform.openai.com))

### 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/akhil-bot/AINewsCurator.git
cd AINewsCurator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```


## 🎮 Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided URL 

3. In the application:
   - Enter your API keys of your Tavily and LLM Provider in the sidebar configuration
   - Type your query in the text area (e.g., "Latest AI agents")
   - Click "Generate News Letter" to create your newsletter
   - Copy or save the generated News Letter

### 💡 Example Queries

- "Latest developments in AI agents"
- "Recent breakthroughs in machine learning"
- "AI startup news this week"
- "New AI tools and applications"

## 🏗️ Project Structure

```
ai-newsletter-generator/
├── agents/                 # Agent implementations for different tasks
│   └── Agents.py          # Core agent classes (NewsSearcher, Summarizer, Publisher)
├── graphs/                 # Workflow definitions
│   └── graph.py           # Main workflow graph configuration
├── models/                # LLM model implementations
│   ├── openai_models.py   # OpenAI integration
│   ├── ollama_models.py   # Ollama integration
│   └── ...                # Other model integrations
├── states/                # State management
│   └── state.py          # Workflow state definitions
├── prompts/               # Prompt templates
│   └── prompts.py        # System prompts for agents
├── utils/                 # Helper utilities
├── config/               # Configuration files
├── main.py               # Main Streamlit application
└── requirements.txt      # Project dependencies
```

## 🔧 Configuration Options

- **LLM Provider**: Choose between different language model providers (currently OpenAI active)
- **Model**: Select specific model (e.g., GPT-4, GPT-3.5-turbo)
- **Temperature**: Adjust creativity level (0.0 - 1.0)
- **API Keys**: Securely store your Tavily and LLM provider API keys

## 🔜 Future Improvements

1. **Additional LLM Providers**
   - Integration with Ollama
   - Support for VLLM
   - Claude and Gemini implementations

2. **Enhanced Features**
   - Custom newsletter templates
   - Scheduled report generation
   - Email distribution capability
   - PDF export option

3. **UI Enhancements**
   - Dark/light mode toggle
   - Mobile-responsive design
   - Custom styling options
   - Report history view

4. **Advanced Configuration**
   - Custom search parameters
   - Multiple source filtering
   - Language selection
   - Category-based filtering

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.



---

Made with ❤️ by passionate AI Engineers 