import os
import openai
import requests
import sqlite3
import logging
from tenacity import retry, wait_random_exponential, stop_after_attempt
from dotenv import load_dotenv
from conversation import Conversation

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o"
DATABASE = "db/countries_database.sqlite"
USER_MESSAGE = "Top 10 countries by area"

# Initialize database connection (allow multi-threading)
conn = sqlite3.connect(DATABASE, check_same_thread=False)

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Application started successfully.")

# Retry decorator for API calls
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, model=MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    try:
        logging.info(f"Sending API request with payload: {json_data}")
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        logging.info(f"Received API response: {response.status_code}")
        return response.json()  # Ensure response is parsed
    except Exception as e:
        logging.error(f"Unable to generate ChatCompletion response: {e}")
        return {"error": str(e)}  # Return error in JSON format

# Database schema string
database_schema_string = """
Table: countries
Columns: Country, Region, Population, Area, Pop. Density, Coastline, Net migration, Infant mortality, GDP, Literacy, Phones, Arable, Crops, Climate, Birthrate, Deathrate, Agriculture, Industry,Service
"""

logging.info(f"Database schema loaded: {database_schema_string}")

# Define available functions for the agent
functions = [
    {
        "name": "ask_database",
        "description": "Use this function to answer user questions about data. Output should be a fully formed SQL query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            """,
                }
            },
            "required": ["query"],
        },
    }
]

# Function to validate SQL queries
def is_safe_sql(query):
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE"]
    for keyword in forbidden_keywords:
        if keyword in query.upper():
            return False
    return True

# Function to query SQLite database
def ask_database(conn, query):
    """Function to query SQLite database with provided SQL query."""
    if not is_safe_sql(query):
        logging.warning(f"Blocked potentially harmful SQL query: {query}")
        raise Exception("Unsafe SQL query detected.")
    try:
        logging.info(f"Executing SQL query: {query}")
        results = conn.execute(query).fetchall()
        logging.info(f"Query executed successfully. Rows fetched: {len(results)}")
        return results
    except Exception as e:
        logging.error(f"SQL error: {e}")
        raise Exception(f"SQL error: {e}")

# Function to handle chat completion and function execution
def chat_completion_with_function_execution(messages, functions=None):
    """Makes a ChatCompletion API call and executes function if requested."""
    try:
        response = chat_completion_request(messages, functions)
        full_message = response["choices"][0]
        if full_message["finish_reason"] == "function_call":
            logging.info("Function generation requested, calling function")
            return call_function(messages, full_message)
        else:
            logging.info("Function not required, responding to user")
            return response
    except Exception as e:
        logging.error(f"Unable to generate ChatCompletion response: {e}")
        return {"error": str(e)}

# Function to execute function calls based on LLM output
def call_function(messages, full_message):
    """Executes function calls using model-generated function arguments."""
    results = []  # Initialize to avoid undefined errors

    if full_message["message"]["function_call"]["name"] == "ask_database":
        query = eval(full_message["message"]["function_call"]["arguments"])
        logging.info(f"Prepped query: {query}")
        try:
            results = ask_database(conn, query["query"])
        except Exception as e:
            logging.error(f"Error executing query: {e}")

            # Try to fix query if there was an error
            messages.append(
                {
                    "role": "system",
                    "content": f"""Query: {query['query']}
The previous query received the error {e}. 
Please return a fixed SQL query in plain text.
Your response should consist of ONLY the SQL query with the separator sql_start at the beginning and sql_end at the end""",
                }
            )
            response = chat_completion_request(messages, model=MODEL)

            # Retry with fixed query
            try:
                cleaned_query = response["choices"][0]["message"][
                    "content"
                ].split("sql_start")[1].split("sql_end")[0]
                results = ask_database(conn, cleaned_query)
                logging.info("Query fixed and executed on second try")
            except Exception as e:
                logging.error(f"Second failure in executing query: {e}")

        messages.append(
            {"role": "function", "name": "ask_database", "content": str(results)}
        )

        try:
            response = chat_completion_request(messages)
            return response
        except Exception as e:
            logging.error(f"Function chat request failed: {e}")
            raise Exception("Function chat request failed")
    else:
        logging.error("Function does not exist and cannot be called")
        raise Exception("Function does not exist and cannot be called")

# System prompt for the assistant
agent_system_message = """You are DatabaseGPT, a helpful assistant who gets answers to user questions from the Database
Provide as many details as possible to your users
Begin!"""

# Initialize conversation when running as main
if __name__ == '__main__':
    sql_conversation = Conversation()
    sql_conversation.add_message("system", agent_system_message)
    sql_conversation.add_message("user", USER_MESSAGE)

    # Execute chat completion and handle assistant response
    chat_response = chat_completion_with_function_execution(
        sql_conversation.conversation_history, functions=functions
    )

    # Initialize assistant_message
    assistant_message = ""

    try:
        assistant_message = chat_response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Error extracting assistant message: {e}")
        assistant_message = "Sorry, I couldn't process your request."

    # Add assistant's response to conversation
    sql_conversation.add_message("assistant", assistant_message)
    sql_conversation.display_conversation(detailed=True)
