# AI Data Assistant

## 📌 What Kind of Project is This?
AI Data Assistant is a **Streamlit-based AI-powered application** that allows users to query a **Countries Database** and receive intelligent responses using OpenAI's API. The assistant also supports general queries and can send responses via email.

## 🤖 What Can the Agent Do?
- Answer **general user queries**.
- Generate **SQL queries** to extract relevant data from the database.
- Fetch and analyze data from the **Countries Database**.
- Process **external API requests** for additional information.
- Allow users to **receive responses via email**.
- Provide a **customizable UI** with dark and light themes.

---

## 🔐 Security Measures & Their Implementation
To ensure the security of the application, multiple protection layers were added:

| **Security Measure** | **Implemented In** |
|----------------------|----------------------|
| **Secure API Key Handling** (Environment variables) | `config.py` |
| **SQL Injection Prevention** (Parameterized Queries) | `database.py` |
| **Logging Security** (Ensures logs directory exists) | `config.py` |
| **Input Validation & Rate Limiting** (Restricts query length, filters invalid input) | `assistant.py` |
| **Secure API Requests** (Timeouts & Error Handling) | `functions.py` |
| **Secure Email Sending** (Environment variables for email credentials) | `config.py` |

---

## 🚀 How to Use This Program?
### **1️⃣ Installation & Setup**
#### **Clone the Repository**
```bash
git clone https://github.com/your-repo/ai-data-assistant.git
cd ai-data-assistant
```

#### **Create & Activate Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate
```

#### **Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Running the Application**
To start the Streamlit UI:
```bash
streamlit run main.py
```

### **3️⃣ Using the Application**
1. **Enter your name and email** (optional for receiving responses via email).
2. **Type a question** related to the Countries Database or general queries.
3. **Click “Submit”** to get a response.
4. **Enable “Send response to email”** if you want the response to be emailed.
5. **Use the sidebar** to switch between Chat, External Data, and Settings.

---

## 📬 Contact & Contributions
Feel free to contribute or suggest improvements!
