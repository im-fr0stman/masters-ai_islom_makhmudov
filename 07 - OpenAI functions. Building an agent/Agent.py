from openai import OpenAI
import sqlite3
import os

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if client.api_key is None:
    raise ValueError("Missing OpenAI API key! Set OPENAI_API_KEY environment variable.")

# Define Assistant
my_assistant = client.beta.assistants.create(
    instructions="""
    You are an intelligent database analysis assistant.
    - You answer general user questions.
    - If a question requires data, generate an SQL query and analyze the result.
    - Ensure all responses include full details, such as numbers and names.
    """,
    name="Database Analyst",
    tools=[{"type": "code_interpreter"}],  # Enables Python execution
    model="gpt-4o",
)

print(f"Assistant Created: {my_assistant.name} (ID: {my_assistant.id})")

# Database Connection
DATABASE = "countries_database.sqlite"

def ask_database(query):
    """Runs an SQL query and returns the result with proper formatting."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return "No results found."

        # Convert result into readable format
        formatted_result = "\n".join([", ".join(map(str, row)) for row in rows])
        return formatted_result
    except Exception as e:
        return f"SQL Error: {e}"

# Function to process user input
def analyze_question(user_question):
    """Sends user input to the assistant for analysis and database queries."""
    thread = client.beta.threads.create()

    # Send the user's question to OpenAI
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_question
    )

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=my_assistant.id
    )

    # Wait for completion
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break

    # Get assistant response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response_content = messages.data[0].content[0].text.value

    # Check if the assistant generated an SQL query
    if "SELECT" in response_content:
        sql_query = response_content.strip("`")  # Remove any surrounding markdown code blocks
        sql_result = ask_database(sql_query)
        return f"Query Result:\n{sql_result}"

    return response_content

# Main loop for user input
while True:
    user_input = input("\nAsk a database or analysis question (or type 'exit' to quit): ")
    if user_input.lower() == "exit":
        print("\nGoodbye!")
        break

    response = analyze_question(user_input)
    print(f"\nAssistant:\n{response}")
