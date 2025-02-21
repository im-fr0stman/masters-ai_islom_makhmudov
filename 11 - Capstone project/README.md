# 📊 AI-Powered Database Assistant

## 📖 Project Overview

The **AI-Powered Database Assistant** is a Streamlit-based application that integrates **OpenAI's GPT-4o** API with a **SQL database** to answer both general and data-specific questions. 

- **Database Queries:** When a user's question is related to the database, the app dynamically generates and executes SQL queries to fetch accurate results.
- **General Knowledge:** For non-database-related questions, the app directly leverages GPT-4o to generate informative responses.

This capstone project showcases the integration of **LLM (Large Language Models)** with structured data sources, enhancing the user experience by combining the power of AI with real-time data querying.

---

## ⚙️ Features

- ✅ **Dynamic SQL Query Generation:** Automatically generates and executes SQL queries based on user prompts.
- ✅ **GPT-4o Integration:** Leverages OpenAI's powerful language model to handle non-database queries.
- ✅ **Function Calling:** Implements function calling to decide when to use the database vs. the LLM for answering queries.
- ✅ **Streamlit UI:** Interactive and user-friendly interface with real-time responses.
- ✅ **Logging System:** Detailed logs for all API calls, database queries, and system events.
- ✅ **SQL Injection Prevention:** Filters and blocks harmful SQL queries to secure the database.

---

## 🔒 Security Measures

1. **SQL Injection Prevention:**
   - Queries are validated to block harmful SQL commands like `DROP`, `DELETE`, and `UPDATE`.
   - Any unsafe query is logged and rejected.

2. **Enhanced API Response Handling:**
   - Validates and sanitizes API responses.
   - Prevents the app from breaking due to malformed or unexpected API outputs.

3. **Environment Variable Protection:**
   - Sensitive keys (like **OpenAI API Key**) are managed through environment variables and **`.env`** files.

4. **Detailed Logging:**
   - Tracks all major events, including:
     - User queries
     - API requests & responses
     - SQL queries
     - Errors and warnings

---

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.8+
- [OpenAI API Key](https://platform.openai.com/signup)
- SQLite (used for the countries database)
- Streamlit

