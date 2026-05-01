<div align="center">
  <h1 align="center">AI Learning Assistant</h1>
  <p align="center">
    An intelligent, interactive study companion built on Snowflake Cortex and Streamlit.
  </p>
</div>

<br />

## 📖 Overview

The **AI Learning Assistant** is a production-ready educational tool that transforms raw study material into interactive, engaging, and highly effective learning modules. Designed to run securely within the Snowflake ecosystem, it leverages the power of **Snowflake Cortex** large language models (LLMs) to automatically generate summaries, intelligent flashcards, and multiple-choice quizzes from any provided text. 

This project demonstrates professional engineering practices, including strict typing, robust error handling, modular architecture, and optimized state management, making it an excellent showcase for competitive open-source programs like GSoC and MLH Fellowship.

## ✨ Key Features

- **🧠 Auto-Summarization:** Uses `SNOWFLAKE.CORTEX.SUMMARIZE` to distill long chapters, articles, or notes into concise, readable summaries.
- **📇 Interactive Flashcards:** Employs the `snowflake-arctic` LLM to dynamically generate Q&A flashcards.
- **🤖 Intelligent Grading:** Evaluates student flashcard responses using a custom Cortex prompt, providing a normalized score (0-1) along with granular feedback on what was correct and what was missing.
- **📝 Automated Quizzes:** Generates comprehensive multiple-choice quizzes and automatically grades them.
- **⚡ Performance Optimized:** Implements robust Streamlit session state caching to minimize costly LLM API calls during UI interactions.
- **🛡️ Production-Grade Code:** Built with PEP 8 compliance, strict PEP 484 type hinting, Google-style docstrings, and comprehensive error logging.

## 🏗️ Architecture & Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) - Provides a responsive, fast, and interactive user interface.
- **Backend & Data Platform:** [Snowflake Snowpark](https://docs.snowflake.com/en/developer-guide/snowpark/index) - Executes Python logic securely inside Snowflake.
- **AI/LLM Engine:** [Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions) - Powers all natural language processing, summarization, and generative tasks using the `snowflake-arctic` model.
- **Language:** Python 3.9+

## 🚀 Getting Started

### Prerequisites

1. A **Snowflake** account with Cortex AI enabled.
2. A Snowpark development environment or Snowflake Streamlit Integration configured.
3. Python 3.9 or higher.

### Local Installation (if running outside of Snowflake UI)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-learning-assistant.git
   cd ai-learning-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit snowflake-snowpark-python pandas
   ```

4. **Configure Snowflake Credentials:**
   Ensure your Snowflake connection parameters (account, user, password, role, warehouse, database, schema) are configured. If running locally, you may need to configure Streamlit secrets (`.streamlit/secrets.toml`) to securely establish the Snowpark session. 

5. **Run the Application:**
   ```bash
   streamlit run streamlit_app.py
   ```

*(Note: If deploying directly as a Streamlit App in Snowflake (SiS), simply upload the `streamlit_app.py` to your Snowflake stage and run it via the Snowsight UI).*

## 💡 Usage

1. Open the **"Create Study Pack"** tab.
2. Paste your learning material into the input area.
3. Click **"Generate study pack"**.
4. Read the generated **Summary** to grasp the core concepts.
5. Test your knowledge using the **Interactive Flashcards** and receive AI-driven feedback on your typed answers.
6. Complete the **Multiple-Choice Quiz** to assess your overall retention.

## 🗺️ Roadmap & Future Scope

While the current prototype focuses on instantaneous study material generation, the architecture is designed to scale into a full-fledged Learning Management Platform:

- **Instructor Insights Dashboard:** Store quiz scores and flashcard evaluation metrics back into Snowflake tables to build analytics dashboards.
- **Weak-Topic Analysis:** Identify which concepts users struggle with most to dynamically adjust future flashcard generation.
- **Multi-Modal Input:** Support uploading PDF documents or linking URLs as source material instead of just raw text.

## 🤝 Contributing

Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`). Ensure your code adheres to PEP 8 and includes type hints.
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
