# Chat RJS
![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

An agent who retrieves board game notices from a RAG to process requests.

## 🔧 Installation

Clone the repository
```shell
git clone https://github.com/Oscaro92/chat-RJS.git
cd chat-RJS
```

Create a virtual environment
```shell
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

Install dependencies
```shell
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file with the following variables:
```
OPENAI_API_KEY=sk-proj-...
```

## 🚀 Usage

```shell
streamlit run chatBot.py
```

## 📁 Project Structure

```
mail-agent/
├── agent.py            # Agent 
├── chatBot.py          # Chat bot
├── docs.py             # Add documents in RAG
├── Chroma              # Database
│   └── ...
├── requirements.txt    # Dependencies
├── .env                # Environment variables
└── README.md           # Documentation
```

## 📝 License

This project is licensed under the MIT License.
