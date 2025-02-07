import os
import logging
from openai import OpenAI
from config import OPENAI_API_KEY, LOG_FILE

# ✅ Configure Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Create Assistant
my_assistant = client.beta.assistants.create(
    instructions="""
    You are an intelligent database analysis assistant.
    - You answer general user questions.
    - If a question requires data, generate a secure SQL query and analyze the result.
    - Ensure all responses include full details, such as numbers and names.
    """,
    name="Database Analyst",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
)

logging.info(f"Assistant Created: {my_assistant.name} (ID: {my_assistant.id})")

def analyze_question(user_question):
    """Sends user input to the assistant and retrieves responses."""
    try:
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_question
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=my_assistant.id
        )
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages.data[0].content[0].text.value
    except Exception as e:
        logging.error(f"Error analyzing question: {e}")
        return "An error occurred while processing your request."

# ✅ Example Usage
if __name__ == "__main__":
    user_input = input("Ask a database or analysis question: ")
    response = analyze_question(user_input)
    print(f"\nAssistant:\n{response}")
