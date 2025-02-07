import logging
import streamlit as st
from ui import main as ui_main
from config import LOG_FILE

# ✅ Configure Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_app():
    """Launches the Streamlit UI."""
    logging.info("Application started.")
    ui_main()

if __name__ == "__main__":
    run_app()
