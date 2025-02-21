import os

import streamlit as st
import datetime
import logging
from main import chat_completion_with_function_execution, functions, ask_database, conn

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Streamlit UI started successfully.")

def main():
    """Streamlit Enhanced UI"""
    st.set_page_config(page_title="AI Data Assistant", page_icon="🌍", layout="wide")

    # Custom Styling
    st.markdown(
        """
        <style>
            .title-text {
                font-size: 36px;
                font-weight: bold;
                color: white;
            }
            .subtitle-text {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            .description-text {
                font-size: 18px;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""<h1 class='title-text'>🌍 AI Data Assistant</h1>""", unsafe_allow_html=True)
    st.markdown(
        """<p class='description-text'>This AI Assistant can answer questions related to the Countries database and general queries.</p>""",
        unsafe_allow_html=True)

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "External Data", "Settings"])

    if page == "Chat":
        st.header("Chat with AI Assistant")
        user_name = st.text_input("Enter your name:")
        user_email = st.text_input("Enter your email:")
        send_email = st.checkbox("Send response to email")

        user_input = st.text_area("Enter your query:")
        if st.button("Submit"):
            if user_input:
                logging.info(f"User query submitted: {user_input}")
                # Prepare conversation
                messages = [{"role": "user", "content": user_input}]

                # Process query
                chat_response = chat_completion_with_function_execution(
                    messages, functions=functions
                )

                try:
                    assistant_message = chat_response["choices"][0]["message"]["content"]
                except Exception as e:
                    assistant_message = "Sorry, I couldn't process your request."
                    logging.error(f"Error processing chat response: {e}")

                st.subheader("Assistant's Response:")
                st.write(assistant_message)

                if send_email:
                    st.success("Response will be sent to your email (feature placeholder).")
                    logging.info(f"Response flagged to send to email: {user_email}")
            else:
                st.warning("Please enter a query.")

    elif page == "External Data":
        st.header("Fetch External Data")
        query = st.text_input("Enter search term:")
        if st.button("Fetch Data"):
            if query:
                st.subheader("API Response:")
                st.json({"data": "This is a placeholder for external API data."})
                logging.info(f"Fetched external data for query: {query}")
            else:
                st.warning("Please enter a search term.")

    elif page == "Settings":
        st.header("Settings")
        theme = st.radio("Select Theme", ["Light", "Dark"])
        st.write(f"Selected Theme: {theme}")

        # Log theme selection
        logging.info(f"User selected theme: {theme}")

if __name__ == "__main__":
    main()
